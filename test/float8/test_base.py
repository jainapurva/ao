# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
import copy
import itertools
import random
import re
import unittest
import warnings

import pytest
import torch
import torch.nn as nn

from torchao.testing.utils import skip_if_rocm
from torchao.utils import (
    TORCH_VERSION_AT_LEAST_2_5,
    is_sm_at_least_89,
    is_sm_at_least_90,
)

if not TORCH_VERSION_AT_LEAST_2_5:
    pytest.skip("Unsupported PyTorch version", allow_module_level=True)


from torchao.float8.config import (
    Float8LinearConfig,
    Float8LinearRecipeName,
    ScalingGranularity,
    ScalingType,
    e4m3_dtype,
    e5m2_dtype,
)
from torchao.float8.float8_linear import Float8Linear
from torchao.float8.float8_linear_utils import convert_to_float8_training
from torchao.float8.float8_ops import addmm_float8_unwrapped
from torchao.float8.float8_scaling_utils import (
    get_maybe_axiswise_dim,
    hp_tensor_to_float8_dynamic,
)
from torchao.float8.float8_training_tensor import (
    Float8TrainingTensor,
    GemmInputRole,
    LinearMMConfig,
    ScaledMMConfig,
    hp_tensor_and_scale_to_float8,
)
from torchao.float8.float8_utils import (
    FP8_TYPES,
    compute_error,
    fp8_tensor_statistics,
    tensor_to_scale,
)
from torchao.testing.training.test_utils import get_test_float8_linear_config
from torchao.utils import is_MI300, is_ROCM

random.seed(0)
torch.manual_seed(0)


def bitwise_identical(a: Float8TrainingTensor, b: Float8TrainingTensor) -> bool:
    assert torch.all(a._scale == b._scale).item(), "scales are not identical"
    assert torch.all(a._data == b._data).item(), "data is not identical"
    return True


class TestFloat8TrainingTensor:
    def test_preserves_dtype(self) -> None:
        # hp means high precision, lp means low precision
        hp_dtypes = (torch.float32, torch.float16, torch.bfloat16)
        lp_dtypes = FP8_TYPES
        for hp_dtype, lp_dtype in itertools.product(hp_dtypes, lp_dtypes):
            x1_hp = torch.randn(4, 4, dtype=hp_dtype)
            x1_s = tensor_to_scale(x1_hp, lp_dtype)
            x2_lp = hp_tensor_and_scale_to_float8(x1_hp, x1_s, lp_dtype)
            x3_hp = x2_lp.to_original_precision()
            assert x3_hp.dtype == hp_dtype

    def test_differentiable_casts(self) -> None:
        lp_dtypes = (e4m3_dtype, e5m2_dtype)
        for f8_dtype in lp_dtypes:
            x = torch.randn(1).requires_grad_()
            grad = torch.randn(1)
            x_s = tensor_to_scale(x, f8_dtype)
            x_f8 = hp_tensor_and_scale_to_float8(x, x_s, f8_dtype)
            x_f8_hp = x_f8.to_original_precision()
            x_f8_hp.backward(grad)
            # the gradient should be unchanged through both casts
            torch.testing.assert_close(grad, x.grad, rtol=0, atol=0)

    def test_split_cat(self):
        a = torch.rand(16, 16, dtype=torch.bfloat16)
        scale = tensor_to_scale(a, e4m3_dtype)
        fp8_a = hp_tensor_and_scale_to_float8(a, scale, e4m3_dtype)

        splits = torch.split(fp8_a, 16)
        catted = torch.cat(splits, dim=0)
        assert bitwise_identical(fp8_a, catted)

    def test_index_put(self):
        a = torch.rand(16, dtype=torch.bfloat16)
        scale_a = tensor_to_scale(a, e4m3_dtype)
        fp8_a = hp_tensor_and_scale_to_float8(a, scale_a, e4m3_dtype)

        index = torch.randint(0, 15, (16,), dtype=torch.long)

        b = torch.rand(16, 16, dtype=torch.bfloat16)
        scale_b = tensor_to_scale(b, e4m3_dtype)
        fp8_b = hp_tensor_and_scale_to_float8(b, scale_a, e4m3_dtype)
        fp8_b_bad = hp_tensor_and_scale_to_float8(b, scale_b, e4m3_dtype)

        with pytest.raises(AssertionError):
            b[index] = fp8_a
            fp8_b[index] = a
            fp8_b_bad[index] = fp8_a
        fp8_b[index] = fp8_a

    def test_copy_(self):
        a = torch.rand(16, dtype=torch.bfloat16)
        scale_a = tensor_to_scale(a, e4m3_dtype)
        fp8_a = hp_tensor_and_scale_to_float8(a, scale_a, e4m3_dtype)

        b = torch.empty(16, dtype=torch.bfloat16)
        b.copy_(fp8_a)  # Should work
        torch.testing.assert_close(b, fp8_a.to_original_precision())
        with pytest.raises(RuntimeError):
            fp8_a.copy_(b)  # Should fail

        fp8_b = Float8TrainingTensor(
            torch.empty(16, dtype=e4m3_dtype),
            scale_a,
            torch.bfloat16,
            fp8_a._linear_mm_config,
        )
        fp8_b.copy_(fp8_a)
        torch.testing.assert_close(fp8_a._data, fp8_b._data)

    def test_transpose(self):
        a = torch.rand((16, 16), dtype=torch.bfloat16)
        for axiswise_dim in (None, 0, -1):
            scale_a = tensor_to_scale(a, e4m3_dtype)
            fp8_a = hp_tensor_and_scale_to_float8(
                a, scale_a, e4m3_dtype, axiswise_dim=axiswise_dim
            )
            fp8_b = hp_tensor_and_scale_to_float8(
                a, scale_a, e4m3_dtype, axiswise_dim=axiswise_dim
            )

            fp8_a_transposed = fp8_a.transpose(0, 1)
            fp8_b_t = fp8_b.t()

            torch.testing.assert_close(
                (fp8_a_transposed._data, fp8_a_transposed._scale),
                (fp8_b_t._data, fp8_b_t._scale),
            )

    @pytest.mark.parametrize("shape", [(8, 16), (4, 8, 16), (2, 4, 8, 16)])
    @pytest.mark.parametrize("axiswise_dim", [0, -1])
    @pytest.mark.parametrize("round_scales_to_power_of_2", [True, False])
    def test_axiswise_dynamic_cast(
        self, shape, axiswise_dim, round_scales_to_power_of_2
    ):
        a = torch.randn(*shape, dtype=torch.bfloat16)
        linear_mm_config = LinearMMConfig()
        a_fp8 = hp_tensor_to_float8_dynamic(
            a,
            e4m3_dtype,
            linear_mm_config,
            scaling_granularity=ScalingGranularity.AXISWISE,
            axiswise_dim=axiswise_dim,
            round_scales_to_power_of_2=round_scales_to_power_of_2,
        )
        a_dq = a_fp8.to_original_precision()
        sqnr = compute_error(a, a_dq)
        assert sqnr >= 25.0

    def test_axiswise_reshape(self):
        a = torch.randn(3, 5, 7, dtype=torch.bfloat16)
        linear_mm_config = LinearMMConfig()

        # if we scale across dim0, we can only reshape to [3, -1]
        a_fp8_d0 = hp_tensor_to_float8_dynamic(
            a,
            e4m3_dtype,
            linear_mm_config,
            scaling_granularity=ScalingGranularity.AXISWISE,
            axiswise_dim=0,
        )
        assert list(a_fp8_d0._data.shape) == [3, 5, 7]
        assert list(a_fp8_d0._scale.shape) == [1, 5, 7]

        a_fp8_d0_r = a_fp8_d0.reshape(3, -1)
        assert list(a_fp8_d0_r.shape) == [3, 5 * 7]
        assert list(a_fp8_d0_r._scale.shape) == [1, 5 * 7]
        # verify numerics did not change
        assert torch.allclose(
            a_fp8_d0.to_original_precision(),
            a_fp8_d0_r.to_original_precision().reshape(3, 5, 7),
            atol=0,
            rtol=0,
        )
        with pytest.raises(RuntimeError):
            a_fp8_d0.reshape(-1, 7)

        # if we scale across dim2, we can only reshape to [-1, 7]
        a_fp8_d2 = hp_tensor_to_float8_dynamic(
            a,
            e4m3_dtype,
            linear_mm_config,
            scaling_granularity=ScalingGranularity.AXISWISE,
            axiswise_dim=-1,
        )
        assert list(a_fp8_d2._data.shape) == [3, 5, 7]
        assert list(a_fp8_d2._scale.shape) == [3, 5, 1]

        a_fp8_d2_r = a_fp8_d2.reshape(-1, 7)
        assert list(a_fp8_d2_r.shape) == [3 * 5, 7]
        assert list(a_fp8_d2_r._scale.shape) == [3 * 5, 1]
        # verify numerics did not change
        assert torch.allclose(
            a_fp8_d2.to_original_precision(),
            a_fp8_d2_r.to_original_precision().reshape(3, 5, 7),
            atol=0,
            rtol=0,
        )
        with pytest.raises(RuntimeError):
            a_fp8_d2.reshape(3, -1)

    @pytest.mark.parametrize("a_shape", [(16, 32), (2, 16, 32), (1, 2, 16, 32)])
    @pytest.mark.parametrize(
        "a_granularity,b_granularity",
        [
            (ScalingGranularity.AXISWISE, ScalingGranularity.AXISWISE),
            (ScalingGranularity.AXISWISE, ScalingGranularity.TENSORWISE),
            (ScalingGranularity.TENSORWISE, ScalingGranularity.AXISWISE),
        ],
    )
    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    @unittest.skipIf(not is_sm_at_least_90(), "Requires CUDA capability >= 9.0")
    def test_axiswise_gemm(self, a_shape, a_granularity, b_granularity):
        a = torch.randn(*a_shape, dtype=torch.bfloat16, device="cuda")
        b = torch.randn(64, 32, dtype=torch.bfloat16, device="cuda")

        linear_mm_config = LinearMMConfig()

        a_fp8 = hp_tensor_to_float8_dynamic(
            a,
            e4m3_dtype,
            linear_mm_config,
            gemm_input_role=GemmInputRole.INPUT,
            scaling_granularity=a_granularity,
            axiswise_dim=get_maybe_axiswise_dim(-1, a_granularity),
        )
        a_fp8 = a_fp8.reshape(-1, a_shape[-1])

        b_fp8 = hp_tensor_to_float8_dynamic(
            b,
            e4m3_dtype,
            linear_mm_config,
            gemm_input_role=GemmInputRole.WEIGHT,
            scaling_granularity=b_granularity,
            axiswise_dim=get_maybe_axiswise_dim(-1, b_granularity),
        )

        c_fp8_compute = torch.mm(a_fp8, b_fp8.t())
        a = a.reshape(-1, a_shape[-1])
        c_ref = torch.mm(a, b.t())
        sqnr = compute_error(c_ref, c_fp8_compute)
        assert sqnr >= 25.0

    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_fp8_dtype(
        self,
    ):
        if is_ROCM() and is_MI300():
            assert e4m3_dtype == torch.float8_e4m3fnuz
        else:
            assert e4m3_dtype == torch.float8_e4m3fn


class TestFloat8Linear:
    def _test_linear_impl(
        self,
        x,
        m_ref,
        config: Float8LinearConfig,
        use_ac: bool = False,
    ):
        m_fp8 = Float8Linear.from_float(
            copy.deepcopy(m_ref),
            config,
        )

        for _ in range(2):
            if use_ac:
                y_fp8 = torch.utils.checkpoint.checkpoint(m_fp8, x, use_reentrant=False)
            else:
                y_fp8 = m_fp8(x)
            y_fp8.sum().backward()

            if use_ac:
                y_ref = torch.utils.checkpoint.checkpoint(m_ref, x, use_reentrant=False)
            else:
                y_ref = m_ref(x)
            y_ref.sum().backward()

        assert y_ref.shape == y_fp8.shape

        y_sqnr = compute_error(y_ref, y_fp8)
        g_sqnr = compute_error(m_ref.weight.grad, m_fp8.weight.grad)
        # verify sqnr is reasonable
        assert y_sqnr >= 18.0, f"{y_sqnr} is too low"
        assert g_sqnr >= 17.0, f"{g_sqnr} is too low"
        if m_ref.bias is not None:
            torch.testing.assert_close(m_ref.bias.grad, m_fp8.bias.grad)

    @pytest.mark.parametrize(
        "emulate", [True, False] if is_sm_at_least_89() else [True]
    )
    @pytest.mark.parametrize("x_shape", [(16, 16), (2, 16, 16), (3, 2, 16, 16)])
    @pytest.mark.parametrize(
        "scaling_type_input",
        [ScalingType.DYNAMIC],
    )
    @pytest.mark.parametrize(
        "scaling_type_weight",
        [ScalingType.DYNAMIC],
    )
    @pytest.mark.parametrize(
        "scaling_type_grad_output",
        [ScalingType.DYNAMIC],
    )
    @pytest.mark.parametrize("linear_dtype", [torch.bfloat16, torch.float32])
    @pytest.mark.parametrize("linear_bias", [False, True])
    @pytest.mark.parametrize("use_ac", [False, True])
    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_linear_from_config_params(
        self,
        x_shape,
        emulate: bool,
        scaling_type_input: ScalingType,
        scaling_type_weight: ScalingType,
        scaling_type_grad_output: ScalingType,
        linear_dtype: torch.dtype,
        linear_bias: bool,
        use_ac: bool,
    ):
        x = torch.randn(*x_shape, device="cuda", dtype=linear_dtype)
        m_ref = nn.Linear(16, 32, bias=linear_bias, device="cuda", dtype=linear_dtype)

        config = get_test_float8_linear_config(
            scaling_type_input,
            scaling_type_weight,
            scaling_type_grad_output,
            emulate,
        )

        self._test_linear_impl(
            x,
            m_ref,
            config,
            use_ac,
        )

    # Note: there are now too many config combinations to test all of
    # them, so this function factors out some of the recipes which are annoying
    # to combine with the main testing function.
    # TODO(future PR): make this cleaner.
    @pytest.mark.parametrize(
        "recipe_name",
        [
            Float8LinearRecipeName.ROWWISE,
            Float8LinearRecipeName.ROWWISE_WITH_GW_HP,
        ],
    )
    @pytest.mark.parametrize("x_shape", [(16, 16), (2, 16, 16), (3, 2, 16, 16)])
    @pytest.mark.parametrize("linear_bias", [True, False])
    @pytest.mark.parametrize(
        "linear_dtype", [torch.bfloat16, torch.float16, torch.float32]
    )
    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    @skip_if_rocm("ROCm enablement in progress")
    def test_linear_from_recipe(
        self,
        recipe_name,
        x_shape,
        linear_dtype: torch.dtype,
        linear_bias: bool,
    ):
        if torch.cuda.get_device_capability() < (9, 0):
            warnings.warn(
                f"CUDA capability {torch.cuda.get_device_capability()} < (9.0)"
            )
            pytest.skip()

        x = torch.randn(*x_shape, device="cuda", dtype=linear_dtype)
        m_ref = nn.Linear(16, 32, bias=linear_bias, device="cuda", dtype=linear_dtype)
        config = Float8LinearConfig.from_recipe_name(recipe_name)
        self._test_linear_impl(
            x,
            m_ref,
            config,
        )

    @pytest.mark.parametrize(
        "emulate", [True, False] if is_sm_at_least_89() else [True]
    )
    @pytest.mark.parametrize(
        "linear_dtype", [torch.float16, torch.bfloat16, torch.float32]
    )
    @pytest.mark.parametrize(
        "recipe_name",
        [
            Float8LinearRecipeName.TENSORWISE,
            Float8LinearRecipeName.ROWWISE,
            Float8LinearRecipeName.ROWWISE_WITH_GW_HP,
        ],
    )
    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_autocast_outputs(
        self,
        emulate: bool,
        linear_dtype: torch.dtype,
        recipe_name: Float8LinearRecipeName,
    ):
        m_ref = nn.Sequential(
            nn.Linear(32, 32, device="cuda", dtype=linear_dtype),
            nn.Linear(32, 32, device="cuda", dtype=linear_dtype),
        )
        config = Float8LinearConfig.from_recipe_name(recipe_name)
        # work around config being frozen
        object.__setattr__(config, "emulate", emulate)

        m = convert_to_float8_training(copy.deepcopy(m_ref), config=config)

        # autocast off
        x = torch.randn(16, 32, device="cuda", dtype=linear_dtype)
        y = m(x)
        assert y.dtype == linear_dtype, f"y.dtype is {y.dtype}, expected {linear_dtype}"

        # autocast on
        with torch.autocast("cuda"):
            y = m(x)
        assert y.dtype == torch.half, f"y.dtype is {y.dtype}, expected {torch.half}"

        with torch.autocast("cuda", dtype=torch.bfloat16):
            y = m(x)
        assert y.dtype == torch.bfloat16, (
            f"y.dtype is {y.dtype}, expected {torch.bfloat16}"
        )

    def test_repr(self):
        m = nn.Linear(32, 16)
        config = Float8LinearConfig(
            emulate=True,
        )
        m = Float8Linear.from_float(
            copy.deepcopy(m),
            config=config,
        )
        s = m.__repr__()
        assert "i:dyn_ten_e4m3,w:dyn_ten_e4m3,go:dyn_ten_e5m2" in s

    @unittest.skipIf(not is_sm_at_least_89(), "CUDA 8.9 not available")
    def test_inference_mode(self):
        x = torch.randn(32, 32, device="cuda")
        m = nn.Sequential(nn.Linear(32, 32)).cuda()
        m = convert_to_float8_training(m)
        with torch.inference_mode(mode=True):
            m(x)

    @unittest.skipIf(not is_sm_at_least_89(), "CUDA arch 8.9 not available")
    def test_quantize(self):
        x = torch.randn(32, 32, device="cuda")
        m = nn.Sequential(nn.Linear(32, 32)).cuda()
        m = convert_to_float8_training(m)
        assert isinstance(m[0], Float8Linear), "Module is not a Float8Linear"
        from torchao.quantization.quant_api import float8_weight_only, quantize_

        quantize_(m, float8_weight_only())
        assert m[0].weight.tensor_impl.float8_data.dtype == torch.float8_e4m3fn, (
            "Post quantization dtype should be torch.float8_e4m3fn"
        )
        with torch.no_grad():
            m(x)


class TestScaledMM:
    @unittest.skipIf(
        not is_sm_at_least_89(),
        "CUDA not available",
    )
    @pytest.mark.parametrize(
        "base_dtype", [torch.float16, torch.bfloat16, torch.float32]
    )
    @pytest.mark.parametrize("use_fast_accum", [True, False])
    def test_scaled_mm_vs_emulated(self, base_dtype, use_fast_accum):
        torch.manual_seed(42)
        input_dtype = e4m3_dtype
        output_dtype = base_dtype
        compare_type = torch.float32

        a = torch.randn(16, 16, device="cuda", dtype=base_dtype)
        b = torch.randn(32, 16, device="cuda", dtype=base_dtype).t()

        a_scale = tensor_to_scale(a, input_dtype).float()
        b_scale = tensor_to_scale(b, input_dtype).float()

        a_fp8 = hp_tensor_and_scale_to_float8(a, a_scale, input_dtype)
        b_fp8 = hp_tensor_and_scale_to_float8(b, b_scale, input_dtype)

        out_scaled_mm = addmm_float8_unwrapped(
            a_fp8._data,
            a_fp8._scale,
            b_fp8._data,
            b_fp8._scale,
            output_dtype=output_dtype,
            use_fast_accum=use_fast_accum,
        )
        out_emulated = torch.mm(
            a_fp8._data.float() / a_fp8._scale,
            b_fp8._data.float() / b_fp8._scale,
        ).to(output_dtype)

        if output_dtype != base_dtype:
            out_scaled_mm = out_scaled_mm.to(compare_type)
            out_emulated = out_emulated.to(compare_type)

        if base_dtype in {torch.bfloat16, torch.float16}:
            atol, rtol = 7e-2, 7e-2
        else:
            atol, rtol = 3e-3, 3e-3
        torch.testing.assert_close(out_scaled_mm, out_emulated, atol=atol, rtol=rtol)

    @unittest.skipIf(not is_sm_at_least_89(), "CUDA not available")
    def test_different_configs_error(self):
        x_fp32 = torch.randn(16, 16, device="cuda")
        x_scale = torch.tensor(1.0, device="cuda")
        fp8_dtype = e4m3_dtype
        linear_config_a = LinearMMConfig(
            ScaledMMConfig(False, True, False, False),
            ScaledMMConfig(False, False, False, False),
            ScaledMMConfig(False, False, False, False),
        )
        linear_config_b = LinearMMConfig(
            ScaledMMConfig(True, True, False, False),
            ScaledMMConfig(True, False, False, False),
            ScaledMMConfig(True, False, False, False),
        )
        a = hp_tensor_and_scale_to_float8(
            x_fp32,
            x_scale,
            fp8_dtype,
            linear_config_a,
            GemmInputRole.INPUT,
        )
        b = hp_tensor_and_scale_to_float8(
            x_fp32,
            x_scale,
            fp8_dtype,
            linear_config_b,
            GemmInputRole.WEIGHT,
        )
        with pytest.raises(
            AssertionError,
            match="linear_mm_config.output mismatch",
        ):
            a @ b

    @unittest.skipIf(
        not is_sm_at_least_89(),
        "CUDA not available",
    )
    @pytest.mark.parametrize(
        "base_dtype", [torch.float16, torch.bfloat16, torch.float32]
    )
    @pytest.mark.parametrize("use_fast_accum", [True, False])
    def test_pad_inner_dim(self, base_dtype, use_fast_accum):
        torch.manual_seed(42)
        input_dtype = e4m3_dtype
        compare_type = torch.float32

        a = torch.randn(16, 41, device="cuda", dtype=base_dtype)
        b = torch.randn(41, 128, device="cuda", dtype=base_dtype)

        a_scale = tensor_to_scale(a, input_dtype).float()
        b_scale = tensor_to_scale(b, input_dtype).float()

        a_fp8 = hp_tensor_and_scale_to_float8(
            a, a_scale, input_dtype, None, GemmInputRole.INPUT
        )
        b_fp8 = hp_tensor_and_scale_to_float8(
            b, b_scale, input_dtype, None, GemmInputRole.WEIGHT
        )

        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Expected trailing dimension of mat1 to be divisible by 16 but got mat1 shape: (16x41"
            ),
        ):
            a_fp8 @ b_fp8

        scaled_mm_config = ScaledMMConfig(False, use_fast_accum, False, True)
        pad_config = LinearMMConfig(
            scaled_mm_config, scaled_mm_config, scaled_mm_config
        )

        a_fp8 = hp_tensor_and_scale_to_float8(
            a,
            a_scale,
            input_dtype,
            pad_config,
            GemmInputRole.INPUT,
        )
        b_fp8 = hp_tensor_and_scale_to_float8(
            b,
            b_scale,
            input_dtype,
            pad_config,
            GemmInputRole.WEIGHT,
        )
        out_padded = a_fp8 @ b_fp8
        out_padded.to(compare_type)

        emulated_scaled_mm_config = ScaledMMConfig(True, use_fast_accum, False, False)
        emulated_config = LinearMMConfig(
            emulated_scaled_mm_config,
            emulated_scaled_mm_config,
            emulated_scaled_mm_config,
        )
        a_fp8 = hp_tensor_and_scale_to_float8(
            a,
            a_scale,
            input_dtype,
            emulated_config,
            GemmInputRole.INPUT,
        )
        b_fp8 = hp_tensor_and_scale_to_float8(
            b,
            b_scale,
            input_dtype,
            emulated_config,
            GemmInputRole.WEIGHT,
        )
        out_emulated = a_fp8 @ b_fp8
        out_emulated.to(compare_type)
        sqnr = compute_error(out_padded, out_emulated)
        assert sqnr > 50.0


class TestNumerics:
    @pytest.mark.parametrize(
        "float8_dtype",
        [
            torch.float8_e4m3fn,
            torch.float8_e5m2,
            torch.float8_e4m3fnuz,
            torch.float8_e5m2fnuz,
        ],
    )
    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_small_amax_float16(self, float8_dtype):
        # If we calculate scale naively with FP8_MAX_POS / amax,
        # the result may not be representable in fp16. Verify that
        # the way we calculate scales actually works for tensors with
        # small values.
        #
        #   naive_s = fp8_max_pos / (amax + eps)
        #
        # failing case:
        #
        #   fp8_max_pos / (amax + eps) >= fp16_max_pos, or
        #
        #   amax + eps >= fp8_max_pos / fp16_max_pos

        float8_max_pos = torch.finfo(float8_dtype).max
        FP16_MAX_POS = torch.finfo(torch.float16).max

        target_amax = float8_max_pos / (FP16_MAX_POS + 1e-12)
        x = torch.tensor([target_amax], dtype=torch.float16, device="cuda")
        scale = tensor_to_scale(x, float8_dtype)
        assert not torch.any(torch.isinf(scale))


class TestFloat8LinearUtils(unittest.TestCase):
    def test_swap_root_linear(self):
        for emulate in [True, False]:
            module = nn.Linear(3, 3)
            config = Float8LinearConfig(emulate=emulate)
            module = convert_to_float8_training(module, config=config)
            self.assertIsInstance(module, Float8Linear)
            self.assertEqual(module.linear_mm_config.output.emulate, emulate)
            self.assertEqual(module.linear_mm_config.output.emulate, emulate)

    def test_swap_root_linear_with_children_raises(self):
        for emulate in [True, False]:
            module = nn.Linear(3, 3)
            module.child = nn.Sequential(nn.Linear(3, 3))
            config = Float8LinearConfig(emulate=emulate)
            with self.assertRaisesRegex(
                AssertionError,
                "Does not support a root nn.Linear with children",
            ):
                convert_to_float8_training(module, config=config)

    def test_swap_submodule_linears(self):
        class MLP(nn.Module):
            def __init__(self, dim: int):
                super().__init__()
                self.lin1 = nn.Linear(dim, 4 * dim)
                self.lin2 = nn.Linear(4 * dim, dim)

        for emulate in [True, False]:
            model = nn.Sequential(MLP(3), nn.Linear(3, 3), MLP(3))
            config = Float8LinearConfig(emulate=emulate)
            model = convert_to_float8_training(model, config=config)
            self.assertIsInstance(model[0].lin1, Float8Linear)
            self.assertIsInstance(model[0].lin2, Float8Linear)
            self.assertIsInstance(model[1], Float8Linear)
            self.assertIsInstance(model[2].lin1, Float8Linear)
            self.assertIsInstance(model[2].lin2, Float8Linear)

    def test_swap_linears_with_filters(self):
        class MLP(nn.Module):
            def __init__(self, dim: int):
                super().__init__()
                self.lin1 = nn.Linear(dim, 4 * dim)
                self.lin2 = nn.Linear(4 * dim, 4 * dim)

        model = nn.Sequential(MLP(8), nn.Linear(32, 32), MLP(40))
        # filter out the linear layers whose shape is smaller than 32 or non-divisible by 16.

        size_limit = 32

        def module_filter_fn(mod, fqn):
            return (
                mod.in_features >= size_limit
                and mod.out_features >= size_limit
                and mod.in_features % 16 == 0
                and mod.out_features % 16 == 0
            )

        config = Float8LinearConfig(emulate=True)
        model = convert_to_float8_training(
            model,
            config=config,
            module_filter_fn=module_filter_fn,
        )
        # in_features=8, out_features=32, 8 is less than 32.
        self.assertNotIsInstance(model[0].lin1, Float8Linear)
        # in_features=32, out_features=32,
        self.assertIsInstance(model[0].lin2, Float8Linear)
        # in_features=32, out_features=32,
        self.assertIsInstance(model[1], Float8Linear)
        # in_features=40, out_features=160, 40 is not divisible by 16.
        self.assertNotIsInstance(model[2].lin1, Float8Linear)
        # in_features=160, out_features=160,
        self.assertIsInstance(model[2].lin2, Float8Linear)

    def test_swap_submodule_linears_with_skip(self):
        class MLP(nn.Module):
            def __init__(self, dim: int):
                super().__init__()
                self.lin1 = nn.Linear(dim, 4 * dim)
                self.lin2 = nn.Linear(4 * dim, dim)

        model = nn.Sequential(MLP(3), nn.Linear(3, 3), MLP(3))
        module_filter_fn = lambda mod, fqn: fqn not in [
            "0.lin2",
            "2.lin1",
        ]
        config = Float8LinearConfig(emulate=True)
        model = convert_to_float8_training(
            model,
            config=config,
            module_filter_fn=module_filter_fn,
        )
        self.assertTrue(type(model[0].lin1) is Float8Linear)
        self.assertTrue(type(model[0].lin2) is nn.Linear)
        self.assertTrue(type(model[1]) is Float8Linear)
        self.assertTrue(type(model[2].lin1) is nn.Linear)
        self.assertTrue(type(model[2].lin2) is Float8Linear)

    def test_fp8_tensor_statistics(self):
        hp_dtypes = (torch.float32, torch.float16, torch.bfloat16)
        lp_dtypes = (e4m3_dtype, e5m2_dtype)
        for hp_dtype, lp_dtype in itertools.product(hp_dtypes, lp_dtypes):
            x1_hp = torch.ones(4, 4, dtype=hp_dtype)
            tensor_len = x1_hp.numel()

            # Overflow caused by a too large scaling factor
            s_overflow = torch.tensor(1e9)
            fp8_overflow = hp_tensor_and_scale_to_float8(x1_hp, s_overflow, lp_dtype)
            (zero_cnt, max_cnt) = fp8_tensor_statistics(fp8_overflow, lp_dtype)
            self.assertEqual((zero_cnt, max_cnt), (0, tensor_len))

            # Underflow caused by a too small scaling factor
            s_underflow = torch.tensor(1e-9)
            fp8_underflow = hp_tensor_and_scale_to_float8(x1_hp, s_underflow, lp_dtype)
            (zero_cnt, max_cnt) = fp8_tensor_statistics(fp8_underflow, lp_dtype)
            self.assertEqual((zero_cnt, max_cnt), (tensor_len, 0))

            # Both overflow and underflow
            x2_hp = torch.cat((x1_hp * 1e9, x1_hp * 1.0, x1_hp * 1e-9), 0)
            fp8_over_underflow = hp_tensor_and_scale_to_float8(
                x2_hp, torch.tensor(1.0), lp_dtype
            )
            (zero_cnt, max_cnt) = fp8_tensor_statistics(fp8_over_underflow, lp_dtype)
            self.assertEqual((zero_cnt, max_cnt), (tensor_len, tensor_len))


if __name__ == "__main__":
    pytest.main([__file__])
