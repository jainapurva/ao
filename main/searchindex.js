Search.setIndex({"docnames": ["api_ref_dtypes", "api_ref_intro", "api_ref_kernel", "api_ref_quantization", "api_ref_sparsity", "dtypes", "generated/torchao.dtypes.AffineQuantizedTensor", "generated/torchao.dtypes.to_affine_quantized_floatx", "generated/torchao.dtypes.to_affine_quantized_floatx_static", "generated/torchao.dtypes.to_affine_quantized_intx", "generated/torchao.dtypes.to_affine_quantized_intx_static", "generated/torchao.dtypes.to_nf4", "generated/torchao.quantization.Int4WeightOnlyGPTQQuantizer", "generated/torchao.quantization.Int4WeightOnlyQuantizer", "generated/torchao.quantization.SmoothFakeDynQuantMixin", "generated/torchao.quantization.SmoothFakeDynamicallyQuantizedLinear", "generated/torchao.quantization.int4_weight_only", "generated/torchao.quantization.int8_dynamic_activation_int4_weight", "generated/torchao.quantization.int8_dynamic_activation_int8_weight", "generated/torchao.quantization.int8_weight_only", "generated/torchao.quantization.quantize_", "generated/torchao.quantization.smooth_fq_linear_to_inference", "generated/torchao.quantization.swap_linear_with_smooth_fq_linear", "generated/torchao.sparsity.PerChannelNormObserver", "generated/torchao.sparsity.WandaSparsifier", "generated/torchao.sparsity.apply_fake_sparsity", "getting-started", "index", "overview", "performant_kernels", "quantization", "serialization", "sg_execution_times", "sparsity", "tutorials/index", "tutorials/sg_execution_times", "tutorials/template_tutorial"], "filenames": ["api_ref_dtypes.rst", "api_ref_intro.rst", "api_ref_kernel.rst", "api_ref_quantization.rst", "api_ref_sparsity.rst", "dtypes.rst", "generated/torchao.dtypes.AffineQuantizedTensor.rst", "generated/torchao.dtypes.to_affine_quantized_floatx.rst", "generated/torchao.dtypes.to_affine_quantized_floatx_static.rst", "generated/torchao.dtypes.to_affine_quantized_intx.rst", "generated/torchao.dtypes.to_affine_quantized_intx_static.rst", "generated/torchao.dtypes.to_nf4.rst", "generated/torchao.quantization.Int4WeightOnlyGPTQQuantizer.rst", "generated/torchao.quantization.Int4WeightOnlyQuantizer.rst", "generated/torchao.quantization.SmoothFakeDynQuantMixin.rst", "generated/torchao.quantization.SmoothFakeDynamicallyQuantizedLinear.rst", "generated/torchao.quantization.int4_weight_only.rst", "generated/torchao.quantization.int8_dynamic_activation_int4_weight.rst", "generated/torchao.quantization.int8_dynamic_activation_int8_weight.rst", "generated/torchao.quantization.int8_weight_only.rst", "generated/torchao.quantization.quantize_.rst", "generated/torchao.quantization.smooth_fq_linear_to_inference.rst", "generated/torchao.quantization.swap_linear_with_smooth_fq_linear.rst", "generated/torchao.sparsity.PerChannelNormObserver.rst", "generated/torchao.sparsity.WandaSparsifier.rst", "generated/torchao.sparsity.apply_fake_sparsity.rst", "getting-started.rst", "index.rst", "overview.rst", "performant_kernels.rst", "quantization.rst", "serialization.rst", "sg_execution_times.rst", "sparsity.rst", "tutorials/index.rst", "tutorials/sg_execution_times.rst", "tutorials/template_tutorial.rst"], "titles": ["torchao.dtypes", "<code class=\"docutils literal notranslate\"><span class=\"pre\">torchao</span></code> API Reference", "torchao.kernel", "torchao.quantization", "torchao.sparsity", "Dtypes", "AffineQuantizedTensor", "to_affine_quantized_floatx", "to_affine_quantized_floatx_static", "to_affine_quantized_intx", "to_affine_quantized_intx_static", "to_nf4", "Int4WeightOnlyGPTQQuantizer", "Int4WeightOnlyQuantizer", "SmoothFakeDynQuantMixin", "SmoothFakeDynamicallyQuantizedLinear", "int4_weight_only", "int8_dynamic_activation_int4_weight", "int8_dynamic_activation_int8_weight", "int8_weight_only", "quantize", "smooth_fq_linear_to_inference", "swap_linear_with_smooth_fq_linear", "PerChannelNormObserver", "WandaSparsifier", "apply_fake_sparsity", "Getting Started", "Welcome to the torchao Documentation", "Overview", "Performant Kernels", "Quantization", "Serialization", "Computation times", "Sparsity", "&lt;no title&gt;", "Computation times", "Template Tutorial"], "terms": {"thi": [1, 6, 15, 16, 17, 20, 23, 24, 25, 31, 36], "section": 1, "introduc": 1, "dive": 1, "detail": 1, "how": [1, 6, 16, 31], "integr": [1, 31], "pytorch": [1, 6, 27, 36], "optim": [1, 20], "your": [1, 20, 27], "machin": 1, "learn": [1, 16, 36], "model": [1, 17, 20, 21, 22, 24, 25, 27], "sparsiti": [1, 23, 24, 25, 27, 31], "quantiz": [1, 6, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 27, 31], "dtype": [1, 6, 7, 8, 9, 10, 11, 13, 20, 27, 31], "kernel": [1, 6, 16, 20], "tba": [2, 5, 26, 28, 29, 30, 33], "class": [6, 12, 13, 14, 15, 23, 24, 31], "torchao": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 31], "tensor_impl": 6, "aqttensorimpl": 6, "block_siz": [6, 7, 8, 9, 10, 11], "tupl": [6, 7, 8, 9, 10, 24], "int": [6, 7, 8, 9, 10, 11, 13, 20, 24], "shape": 6, "size": [6, 16, 17, 31], "quant_min": [6, 9, 10], "option": [6, 7, 9, 10, 13, 20, 21, 22, 24], "union": [6, 20], "float": [6, 9, 16, 20, 22, 24, 31], "none": [6, 7, 9, 10, 20, 21, 22, 24], "quant_max": [6, 9, 10], "zero_point_domain": [6, 9, 10, 16, 20], "zeropointdomain": [6, 9, 10, 16], "stride": 6, "sourc": [6, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 34, 36], "affin": [6, 20], "tensor": [6, 7, 8, 9, 10, 11, 16, 20, 24, 31, 36], "subclass": [6, 15, 20, 23, 31], "mean": 6, "we": [6, 20, 31], "point": [6, 16, 31], "an": [6, 24, 27], "transform": 6, "quantized_tensor": 6, "float_tensor": 6, "scale": [6, 8, 10, 14, 15, 21, 22], "zero_point": [6, 10, 16], "To": [6, 31], "see": [6, 31], "what": [6, 36], "happen": 6, "dure": [6, 22], "choose_qparam": 6, "dequant": [6, 16], "pleas": [6, 16], "checkout": 6, "http": [6, 24], "github": 6, "com": 6, "ao": 6, "blob": 6, "main": [6, 16], "quant_primit": 6, "py": [6, 32, 35, 36], "check": [6, 31], "three": [6, 24], "quant": 6, "primit": 6, "op": [6, 16, 20], "choose_qparams_affin": [6, 16], "quantize_affin": [6, 16], "qand": 6, "dequantize_affin": [6, 16], "The": [6, 20, 21, 22, 24, 31], "repres": [6, 24, 31], "look": 6, "extern": 6, "regardless": 6, "intern": 6, "represent": [6, 16], "s": 6, "type": [6, 12, 13, 16, 31], "orient": 6, "field": 6, "serv": 6, "gener": [6, 34, 36], "impl": 6, "storag": 6, "data": [6, 31], "e": [6, 20, 31], "g": [6, 20, 31], "store": [6, 23], "plain": 6, "int_data": 6, "pack": 6, "format": 6, "depend": [6, 31], "devic": [6, 12, 13, 20, 31], "oper": 6, "granular": [6, 16, 17], "element": 6, "share": 6, "same": 6, "qparam": 6, "when": 6, "input": [6, 20, 24], "dimens": 6, "ar": [6, 16, 20, 24, 31], "us": [6, 16, 17, 20, 24, 27, 31], "per": [6, 15, 16, 17, 18, 19, 24], "torch": [6, 13, 15, 16, 20, 21, 22, 31, 36], "origin": [6, 24, 31], "high": 6, "precis": [6, 13], "minimum": 6, "valu": [6, 14, 15, 21, 24], "specifi": [6, 20, 24], "deriv": 6, "from": [6, 17, 20, 31, 32, 35, 36], "maximum": [6, 21], "domain": [6, 16], "should": [6, 15, 23, 24], "either": [6, 24], "integ": [6, 16], "zero": [6, 16, 24], "ad": [6, 24], "subtract": 6, "unquant": 6, "default": [6, 16, 20, 21, 22], "float32": [6, 31], "given": 6, "return": [6, 20, 21, 22, 31], "arg": [6, 14, 15, 24], "kwarg": [6, 14, 15, 23, 24, 25], "perform": [6, 14, 15, 21, 23], "convers": [6, 20], "A": [6, 23], "infer": [6, 15, 21, 31], "argument": [6, 20], "self": [6, 14, 15, 31], "If": [6, 21, 24], "alreadi": 6, "ha": 6, "correct": 6, "otherwis": 6, "copi": [6, 24, 31], "desir": 6, "here": [6, 31], "wai": 6, "call": [6, 15, 20, 23, 31], "non_block": 6, "fals": [6, 9, 16, 20, 21, 24, 31], "memory_format": 6, "preserve_format": 6, "memori": 6, "tri": 6, "convert": [6, 15, 20], "asynchron": 6, "respect": 6, "host": 6, "possibl": 6, "cpu": [6, 31], "pin": 6, "cuda": [6, 12, 13, 20, 31], "set": [6, 14, 15, 20, 21, 24], "new": [6, 20], "creat": 6, "even": 6, "match": 6, "other": [6, 24, 31, 36], "exampl": [6, 20, 24, 31, 32, 34, 35, 36], "randn": [6, 31], "2": [6, 16, 20, 25, 36], "initi": [6, 31], "float64": 6, "0": [6, 12, 14, 15, 20, 22, 24, 31, 32, 35, 36], "5044": 6, "0005": 6, "3310": 6, "0584": 6, "cuda0": 6, "true": [6, 9, 12, 13, 20, 21, 31], "input_float": [7, 8, 9, 10], "target_dtyp": [7, 8, 9, 10], "_layout": [7, 8, 9, 10], "layout": [7, 8, 9, 10, 16, 18], "scale_dtyp": [7, 9], "mapping_typ": [9, 17], "mappingtyp": [9, 17], "ep": 9, "zero_point_dtyp": [9, 20], "preserve_zero": [9, 16, 20], "bool": [9, 13, 20, 21], "plainlayout": [9, 10, 18], "use_hqq": [9, 16], "64": [11, 12, 16, 31], "scaler_block_s": 11, "256": [11, 13, 16], "blocksiz": 12, "128": [12, 16], "percdamp": 12, "01": 12, "groupsiz": [12, 13, 20], "inner_k_til": [12, 13, 16], "8": [12, 13, 16], "padding_allow": [12, 13], "bfloat16": [13, 20, 31], "set_debug_x_absmax": [14, 15], "x_running_abs_max": [14, 15], "which": [14, 15, 31], "lead": [14, 15], "smooth": [14, 15], "all": [14, 15, 23, 24, 25, 31, 32, 34], "ones": [14, 15, 24], "alpha": [14, 15, 22], "5": [14, 15, 22, 24, 36], "enabl": [14, 15], "benchmark": [14, 15, 21], "without": [14, 15], "calibr": [14, 15], "replac": [15, 22], "nn": [15, 20, 21, 22, 31], "linear": [15, 16, 17, 18, 19, 20, 22, 25, 31], "implement": [15, 31], "dynam": [15, 17, 18], "token": [15, 17, 18], "activ": [15, 17, 18, 21, 24], "channel": [15, 18, 19, 23], "weight": [15, 16, 17, 18, 19, 20, 24, 31], "base": [15, 24], "smoothquant": [15, 21, 22], "forward": [15, 23, 31], "x": [15, 20, 31, 36], "defin": [15, 23, 24], "comput": [15, 23, 24], "everi": [15, 23], "overridden": [15, 23], "although": [15, 23], "recip": [15, 23], "pass": [15, 23], "need": [15, 23, 24, 31], "within": [15, 23], "function": [15, 20, 23, 24, 25, 27, 31], "one": [15, 23], "modul": [15, 20, 21, 22, 23, 24, 31], "instanc": [15, 20, 23, 31], "afterward": [15, 23], "instead": [15, 16, 23], "sinc": [15, 23, 31], "former": [15, 23], "take": [15, 20, 23], "care": [15, 23, 31], "run": [15, 20, 21, 23, 36], "regist": [15, 23], "hook": [15, 23], "while": [15, 23, 24], "latter": [15, 23], "silent": [15, 23], "ignor": [15, 23], "them": [15, 23], "classmethod": 15, "from_float": 15, "mod": 15, "fake": 15, "version": 15, "note": [15, 24], "requir": 15, "to_infer": 15, "calcul": [15, 21], "prepar": [15, 21, 24], "group_siz": [16, 17, 20], "tensorcoretiledlayout": 16, "appli": [16, 17, 18, 19, 20], "uint4": [16, 20], "onli": [16, 19, 20, 31], "asymmetr": [16, 17, 20], "group": [16, 17], "layer": [16, 18, 19, 21, 22, 24, 25], "tensor_core_til": 16, "speedup": 16, "tinygemm": [16, 20], "target": [16, 24], "int4mm": 16, "aten": 16, "_weight_int4pack_mm": 16, "differ": [16, 31], "algorithm": 16, "compar": [16, 24], "more": [16, 17, 27], "tradit": 16, "follow": 16, "1": [16, 20, 24, 31, 32, 35, 36], "doe": 16, "have": [16, 24], "exactli": 16, "relev": [16, 36], "code": [16, 34, 36], "about": [16, 31], "paramet": [16, 17, 20, 21, 22, 24, 31], "chosen": 16, "control": [16, 17, 24], "smaller": [16, 17, 31], "fine": [16, 17], "grain": [16, 17], "choic": 16, "32": [16, 17, 20, 31], "whether": [16, 20], "hqq": 16, "mode": 16, "symmetr": [17, 18, 19], "int8": [17, 18, 19, 20], "int4": [17, 20, 31], "produc": 17, "executorch": [17, 20], "backend": 17, "current": [17, 20, 22, 24], "did": 17, "support": [17, 31], "lower": 17, "flow": 17, "yet": 17, "quantize_": [20, 31], "apply_tensor_subclass": 20, "callabl": 20, "filter_fn": 20, "str": [20, 22, 24], "set_inductor_config": 20, "modifi": [20, 24], "inplac": [20, 24], "fulli": [20, 22], "qualifi": [20, 22], "name": [20, 22, 24], "want": [20, 31], "automat": [20, 36], "recommend": 20, "inductor": 20, "config": [20, 24], "move": 20, "befor": [20, 31], "can": [20, 31], "speed": 20, "up": 20, "final": 20, "do": 20, "chang": [20, 31], "import": [20, 31, 36], "some": [20, 24], "predefin": 20, "method": [20, 24], "correspond": [20, 31], "execut": [20, 32, 35], "path": 20, "also": [20, 31], "customiz": 20, "int8_dynamic_activation_int4_weight": 20, "int8_dynamic_activation_int8_weight": 20, "mm": 20, "compil": 20, "int4_weight_onli": [20, 31], "int8_weight_onli": 20, "quant_api": [20, 31], "m": [20, 31], "sequenti": 20, "1024": [20, 31], "write": 20, "own": 20, "you": [20, 24, 31, 36], "add": [20, 36], "manual": 20, "constructor": 20, "to_affine_quantized_intx": 20, "groupwis": 20, "apply_weight_qu": 20, "lambda": 20, "int32": 20, "15": 20, "1e": 20, "6": 20, "def": [20, 31], "apply_weight_quant_to_linear": 20, "requires_grad": 20, "under": [20, 27], "block0": 20, "submodul": 20, "fqn": [20, 24], "isinst": 20, "debug_skip_calibr": 21, "each": [21, 23], "smoothfakedynamicallyquantizedlinear": [21, 22], "contain": [21, 22], "debug": 21, "skip_fqn_list": 22, "cur_fqn": 22, "equival": 22, "list": [22, 24], "skip": [22, 24], "being": 22, "process": [22, 36], "factor": 22, "custom": 23, "observ": 23, "l2": 23, "norm": [23, 24], "buffer": 23, "x_orig": 23, "sparsity_level": 24, "semi_structured_block_s": 24, "wanda": 24, "sparsifi": [24, 31], "prune": [24, 27], "propos": 24, "arxiv": 24, "org": 24, "ab": 24, "2306": 24, "11695": 24, "awar": 24, "remov": 24, "product": 24, "magnitud": 24, "variabl": 24, "number": 24, "spars": 24, "block": 24, "out": 24, "level": 24, "dict": 24, "parametr": 24, "preserv": 24, "deepcopi": 24, "squash_mask": 24, "params_to_keep": 24, "params_to_keep_per_lay": 24, "squash": 24, "mask": 24, "appropri": 24, "sparse_param": 24, "attach": 24, "kei": [24, 36], "save": [24, 31], "param": 24, "specif": [24, 31], "string": 24, "xdoctest": 24, "local": 24, "undefin": 24, "don": 24, "t": 24, "ani": 24, "hasattr": 24, "submodule1": 24, "keep": 24, "linear1": [24, 31], "foo": 24, "bar": 24, "submodule2": 24, "linear42": 24, "baz": 24, "print": [24, 31, 36], "42": 24, "24": 24, "update_mask": 24, "tensor_nam": 24, "statist": 24, "retriev": 24, "first": 24, "act_per_input": 24, "Then": 24, "metric": 24, "matrix": 24, "across": 24, "whole": 24, "simul": 25, "4": [25, 31], "open": 27, "librari": [27, 31], "provid": 27, "nativ": 27, "our": 27, "develop": 27, "content": 27, "come": 27, "soon": 27, "question": 31, "peopl": 31, "especi": 31, "describ": [31, 36], "work": 31, "tempfil": 31, "util": 31, "get_model_size_in_byt": 31, "toylinearmodel": 31, "__init__": 31, "n": 31, "k": 31, "super": 31, "bia": 31, "linear2": 31, "example_input": 31, "batch_siz": 31, "in_featur": 31, "eval": 31, "f": 31, "mb": [31, 32, 35], "ref": 31, "namedtemporaryfil": 31, "state_dict": 31, "seek": 31, "load": 31, "meta": 31, "m_load": 31, "so": 31, "load_state_dict": 31, "assign": 31, "after": 31, "re": 31, "assert": 31, "equal": 31, "just": 31, "becaus": 31, "techniqu": 31, "like": 31, "thing": 31, "structur": 31, "For": 31, "float_weight1": 31, "float_weight2": 31, "quantized_weight1": 31, "quantized_weight2": 31, "typic": 31, "go": [31, 36], "techinqu": 31, "abov": 31, "reduct": 31, "around": 31, "4x": 31, "0625": 31, "reason": 31, "avoid": 31, "mai": 31, "fit": 31, "updat": 31, "affinequantizedtensor": 31, "No": 31, "verifi": 31, "properli": 31, "affine_quantized_tensor": 31, "00": [32, 35], "004": [32, 35, 36], "total": [32, 35, 36], "file": [32, 35], "galleri": [32, 34, 36], "mem": [32, 35], "templat": [32, 34, 35], "tutori": [32, 34, 35], "tutorials_sourc": 32, "template_tutori": [32, 35, 36], "download": [34, 36], "python": [34, 36], "tutorials_python": 34, "zip": [34, 36], "jupyt": [34, 36], "notebook": [34, 36], "tutorials_jupyt": 34, "sphinx": [34, 36], "end": 36, "full": 36, "author": 36, "firstnam": 36, "lastnam": 36, "item": 36, "3": 36, "prerequisit": 36, "v2": 36, "gpu": 36, "why": 36, "topic": 36, "link": 36, "research": 36, "paper": 36, "walk": 36, "through": 36, "output": 36, "below": 36, "rand": 36, "9694": 36, "6249": 36, "4587": 36, "7015": 36, "7846": 36, "0758": 36, "4445": 36, "9733": 36, "9658": 36, "0364": 36, "8117": 36, "3812": 36, "0800": 36, "2392": 36, "6165": 36, "practic": 36, "user": 36, "test": 36, "knowledg": 36, "nlp": 36, "scratch": 36, "summar": 36, "concept": 36, "cover": 36, "highlight": 36, "takeawai": 36, "link1": 36, "link2": 36, "time": 36, "script": 36, "minut": 36, "second": 36, "ipynb": 36}, "objects": {"torchao.dtypes": [[6, 0, 1, "", "AffineQuantizedTensor"], [7, 2, 1, "", "to_affine_quantized_floatx"], [8, 2, 1, "", "to_affine_quantized_floatx_static"], [9, 2, 1, "", "to_affine_quantized_intx"], [10, 2, 1, "", "to_affine_quantized_intx_static"], [11, 2, 1, "", "to_nf4"]], "torchao.dtypes.AffineQuantizedTensor": [[6, 1, 1, "", "dequantize"], [6, 1, 1, "", "to"]], "torchao.quantization": [[12, 0, 1, "", "Int4WeightOnlyGPTQQuantizer"], [13, 0, 1, "", "Int4WeightOnlyQuantizer"], [14, 0, 1, "", "SmoothFakeDynQuantMixin"], [15, 0, 1, "", "SmoothFakeDynamicallyQuantizedLinear"], [16, 2, 1, "", "int4_weight_only"], [17, 2, 1, "", "int8_dynamic_activation_int4_weight"], [18, 2, 1, "", "int8_dynamic_activation_int8_weight"], [19, 2, 1, "", "int8_weight_only"], [20, 2, 1, "", "quantize_"], [21, 2, 1, "", "smooth_fq_linear_to_inference"], [22, 2, 1, "", "swap_linear_with_smooth_fq_linear"]], "torchao.quantization.SmoothFakeDynQuantMixin": [[14, 1, 1, "", "set_debug_x_absmax"]], "torchao.quantization.SmoothFakeDynamicallyQuantizedLinear": [[15, 1, 1, "", "forward"], [15, 1, 1, "", "from_float"], [15, 1, 1, "", "set_debug_x_absmax"], [15, 1, 1, "", "to_inference"]], "torchao": [[4, 3, 0, "-", "sparsity"]], "torchao.sparsity": [[23, 0, 1, "", "PerChannelNormObserver"], [24, 0, 1, "", "WandaSparsifier"], [25, 2, 1, "", "apply_fake_sparsity"]], "torchao.sparsity.PerChannelNormObserver": [[23, 1, 1, "", "forward"]], "torchao.sparsity.WandaSparsifier": [[24, 1, 1, "", "prepare"], [24, 1, 1, "", "squash_mask"], [24, 1, 1, "", "update_mask"]]}, "objtypes": {"0": "py:class", "1": "py:method", "2": "py:function", "3": "py:module"}, "objnames": {"0": ["py", "class", "Python class"], "1": ["py", "method", "Python method"], "2": ["py", "function", "Python function"], "3": ["py", "module", "Python module"]}, "titleterms": {"torchao": [0, 1, 2, 3, 4, 27], "dtype": [0, 5], "api": [1, 27], "refer": [1, 27], "python": 1, "kernel": [2, 29], "quantiz": [3, 20, 30], "sparsiti": [4, 33], "affinequantizedtensor": 6, "to_affine_quantized_floatx": 7, "to_affine_quantized_floatx_stat": 8, "to_affine_quantized_intx": 9, "to_affine_quantized_intx_stat": 10, "to_nf4": 11, "int4weightonlygptqquant": 12, "int4weightonlyquant": 13, "smoothfakedynquantmixin": 14, "smoothfakedynamicallyquantizedlinear": 15, "int4_weight_onli": 16, "int8_dynamic_activation_int4_weight": 17, "int8_dynamic_activation_int8_weight": 18, "int8_weight_onli": 19, "smooth_fq_linear_to_infer": 21, "swap_linear_with_smooth_fq_linear": 22, "perchannelnormobserv": 23, "wandasparsifi": 24, "apply_fake_spars": 25, "get": 26, "start": 26, "welcom": 27, "document": 27, "overview": [28, 36], "perform": 29, "serial": 31, "deseri": 31, "flow": 31, "what": 31, "happen": 31, "when": 31, "an": 31, "optim": 31, "model": 31, "comput": [32, 35], "time": [32, 35], "templat": 36, "tutori": 36, "step": 36, "option": 36, "addit": 36, "exercis": 36, "conclus": 36, "further": 36, "read": 36}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx.ext.todo": 2, "sphinx.ext.viewcode": 1, "sphinx": 56}})