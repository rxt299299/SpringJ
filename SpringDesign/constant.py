input_parameter_names = [
    "r",
    "end_closed",
    "N_t",
    "N_a",
    "d_w",
    "d_i",
    "d_o",
    "L_free",
    "L_open",
    "L_hard",
    "deflection",
    "Young",
    "Poisson_ratio",
    "G",
    "k",
    "c",
    "NB_c",
    "NB_n",
    "NB_k",
    "time_stress_Relaxation",
    "Gsr",
]

constraints_parameter_names = [
    "outerDiamMax",
    "outerDiamMin",
    "InnerDiamMax",
    "InnerDiamMin",
    "MaximumShearStressMax",
    "MaximumShearStressMin",
    "CoilBindingGapMax",
    "CoilBindingGapMin",
    "SpringRateMax",
    "SpringRateMin",
    "SpringIndexMax",
    "SpringIndexMin",
    "BucklingSlendernessRatioMax",
    "BucklingSlendernessRatioMin",
    "DiametralExpansionMax",
    "DiametralExpansionMin",
    "StressRelaxationMax",
    "StressRelaxationMin",
    "PreloadForceMax",
    "PreloadForceMin",
]

optimize_parameter_name = [
    "spring_rate_spring_index",  # 0.5*(k/k_max)+0.5*(c/c_max)
]

input_parameter_names_range_above0 = [
    "N_t",
    "N_a",
    "d_w",
    "d_i",
    "d_o",
    "L_free",
    "L_open",
    "L_hard",
    "deflection",
    "Young",
    "Poisson_ratio",
    "G",
    "NB_c",
    "NB_n",
    "NB_k",
    "Gsr",
]

design_measurement_parameters = [
    "N_t",
    "N_a",
    "d_i",
    "d_w",
    "d_o",
    "G",
    "L_free",
    "L_open",
    "L_hard",
]

constraint_value_must_number = [
    "outerDiamMax",
    "outerDiamMin",
    "InnerDiamMax",
    "InnerDiamMin",
    "MaximumShearStressMax",
    "MaximumShearStressMin",
    "CoilBindingGapMax",
    "CoilBindingGapMin",
    "SpringRateMax",
    "SpringRateMin",
    "SpringIndexMax",
    "SpringIndexMin",
    "DiametralExpansionMax",
    "DiametralExpansionMin",
    "StressRelaxationMax",
    "StressRelaxationMin",
    "PreloadForceMax",
    "PreloadForceMin",
]

# BucklingSlendernessRatio constraint有两个输入
# 第一个就是是否要通过别的已知参数Poisson Ratio计算Threshold,
# 第二种是直接给出一个Threshold
# 如果第一种为true那么便不需要检验第二种
constraint_BucklingSlendernessRatio = [
    "BucklingSlendernessRatioMax",
    "BucklingSlendernessRatioMin",
]

Constraint_input_dict = {
    "outerDiamMax": [True, True],  # if_Outer, if_Max
    "outerDiamMin": [True, False],
    "InnerDiamMax": [False, True],
    "InnerDiamMin": [False, False],
    "MaximumShearStressMax": True,  # if_Max
    "MaximumShearStressMin": False,
    "CoilBindingGapMax": True,  # if_Max
    "CoilBindingGapMin": False,
    "SpringRateMax": True,  # if_Max
    "SpringRateMin": False,
    "SpringIndexMax": True,  # if_Max
    "SpringIndexMin": False,
    "BucklingSlendernessRatioMax": True,  # if_Max
    "BucklingSlendernessRatioMin": False,
    "DiametralExpansionMax": True,  # if_Max
    "DiametralExpansionMin": False,
    "StressRelaxationMax": True,  # if_Max
    "StressRelaxationMin": False,
    "PreloadForceMax": True,  # if_Max
    "PreloadForceMin": False,
}

InnerOuterDiam_paras_combinations = {
    "d_o": [
        ["d_i", "d_w"],
        ["d_i", "d_w"],
        ["d_i", "d_w"],
        ["d_o"],
    ],
    "d_i": [
        ["d_o", "d_w"],
        ["d_o", "d_w"],
        ["d_o", "d_w"],
        ["d_i"],
    ],
}

MaxShearStress_paras_combinations = [
    set(
        ["d_i", "d_w", "N_a", "G", "L_free", "L_hard"]
    ),  # 最原始的MaximumShearStress_calculation需要的参数
    set(
        ["d_i", "d_w", "N_t", "end_closed", "G", "L_free", "L_hard"]
    ),  # 没有N_a, 但是有N_t和end_closed
    set(["d_w", "d_o", "N_a", "G", "L_free", "L_hard"]),  # 没有d_i,但是有d_w和d_o
    set(["d_i", "d_o", "N_a", "G", "L_free", "L_hard"]),  # 没有d_w,但是有d_i和d_o
    set(
        ["d_w", "d_o", "N_t", "end_closed", "G", "L_free", "L_hard"]
    ),  # 没有d_i,但是有d_w和d_o, 没有N_a, 但是有N_t和end_closed
    set(
        ["d_i", "d_o", "N_t", "end_closed", "G", "L_free", "L_hard"]
    ),  # 没有d_w,但是有d_i和d_o, 没有N_a, 但是有N_t和end_closed
]


CoilBindingGap_paras_combinations = [
    set(["N_t", "d_w", "L_hard"]),  # 原始参数
    set(["N_a", "end_closed", "d_w", "L_hard"]),  # 没有N_t, 但是有N_a和end_closed
    set(["N_t", "d_i", "d_o", "L_hard"]),  # 没有d_w,但是有d_i和d_o
    set(
        ["N_a", "end_closed", "d_i", "d_o", "L_hard"]
    ),  # 没有N_t, 但是有N_a和end_closed, 没有d_w,但是有d_i和d_o
]


SpringRate_paras_combinations = [
    set(["G", "N_a", "d_w", "d_i"]),  # 原始参数
    set(["G", "N_t", "end_closed", "d_w", "d_i"]),  # 没有N_a, 但是有N_t和end_closed
    set(["G", "N_a", "d_i", "d_o"]),  # 没有d_w, 但是有d_i和d_o
    set(["G", "N_a", "d_w", "d_o"]),  # 没有d_i, 但是有d_w和d_o
    set(
        ["G", "N_t", "end_closed", "d_i", "d_o"]
    ),  # 没有d_w, 但是有d_i和d_o, 没有N_a, 但是有N_t和end_closed
    set(
        ["G", "N_t", "end_closed", "d_w", "d_o"]
    ),  # 没有d_i, 但是有d_w和d_o, 没有N_a, 但是有N_t和end_closed
]

SpringIndex_paras_combinations = [
    set(["d_i", "d_w"]),  # 原始参数
    set(["d_i", "d_o"]),  # 没有d_w
    set(["d_o", "d_w"]),  # 没有d_i
]


BucklingSlendernessRatio_paras_combinations = [
    set(["L_free", "d_i", "d_w"]),  # 原始参数
    set(["L_free", "d_i", "d_o"]),  # 没有d_w
    set(["L_free", "d_o", "d_w"]),  # 没有d_i
]

# Diametral Expansion 直径膨胀，当弹簧被压缩时候衡量弹簧外径增加多少的量度
# (仅封闭条件下弹簧的直径膨胀）
# 因此end_closed必须为True
# 如果没有N_a,有N_t的话，N_a = N_t-2
DiametralExpansion_paras_combinations = [
    set(["L_free", "N_a", "d_i", "d_w"]),  # 原始参数
    set(["L_free", "N_a", "d_i", "d_o"]),  # 没有d_w
    set(["L_free", "N_a", "d_o", "d_w"]),  # 没有d_i
    set(["L_free", "N_t", "d_i", "d_w"]),  # 没有N_a, 有N_t
    set(["L_free", "N_t", "d_i", "d_o"]),  # 没有N_a, 有N_t, 没有d_w
    set(["L_free", "N_t", "d_o", "d_w"]),  # 没有N_a, 有N_t,  没有d_i
]


# Stress Relaxation 应力松弛
StressRelaxation_fixed_paras = [
    "Gsr",
    "NB_c",
    "NB_k",
    "NB_n",
    "time_stress_Relaxation",
    "deflection",
]
StressRelaxation_paras_combinations = [
    set(StressRelaxation_fixed_paras + ["d_w", "d_i", "N_a"]),  # 原始参数
    set(StressRelaxation_fixed_paras + ["d_o", "d_i", "N_a"]),  # 没有d_w
    set(StressRelaxation_fixed_paras + ["d_o", "d_w", "N_a"]),  # 没有d_i
    set(
        StressRelaxation_fixed_paras + ["d_w", "d_i", "N_t", "end_closed"]
    ),  # 没有N_a, 但是有N_t和end_closed
    set(
        StressRelaxation_fixed_paras + ["d_o", "d_i", "N_t", "end_closed"]
    ),  # 没有d_w, 没有N_a, 但是有N_t和end_closed
    set(
        StressRelaxation_fixed_paras + ["d_o", "d_w", "N_t", "end_closed"]
    ),  # 没有d_i, 没有N_a, 但是有N_t和end_closed
]


# 预紧力 Preload Force
PreloadForce_paras_combinations = [
    set(["L_free", "L_solid", "G", "N_a", "d_w", "d_i"]),  # 原始参数
    set(["L_free", "L_solid", "G", "N_a", "d_o", "d_i"]),  # 没有d_w
    set(["L_free", "L_solid", "G", "N_a", "d_o", "d_w"]),  # 没有d_i
    set(
        ["L_free", "L_solid", "G", "N_t", "end_closed", "d_w", "d_i"]
    ),  # 没有N_a, 但是有N_t和end_closed
    set(
        ["L_free", "L_solid", "G", "N_t", "end_closed", "d_o", "d_i"]
    ),  # 没有d_w, 没有N_a, 但是有N_t和end_closed
    set(
        ["L_free", "L_solid", "G", "N_t", "end_closed", "d_o", "d_w"]
    ),  # 没有d_i, 没有N_a, 但是有N_t和end_closed
]
