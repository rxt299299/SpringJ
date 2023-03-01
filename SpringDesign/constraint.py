from .constant import *
from .constraint_utils import *
from .errors import *
import numpy as np
from .utils import match_constraintInput_fromInputBoundParameters


def constraint_firstStepCheck(
    notNone_input_parameters, bound_paras, paras_combinations, constraint_name
):
    # 得到全部目前已知的非空的input parameters
    input_paras = list(notNone_input_parameters.keys())
    existing_paras = set(input_paras + bound_paras)

    # 多种不同的可能有缺失值但是其实没关系别的变量可以补上的组合
    miss_paras_combinations = [(combo - existing_paras) for combo in paras_combinations]

    # 检查对于是否存在遗失的parameters, 乘积不为0, 也就是说没有一个组合能够全部cover的
    if np.prod([len(item) for item in miss_paras_combinations]) > 0:
        raise ConstraintPolicyError(
            "in "
            + constraint_name
            + " constraint policy, \
                                    there exist missing parameters as either input or bound"
        )

    return miss_paras_combinations, input_paras


# 最大最小内外径
def constraint_InnerOuterDiamMaxMin(
    feasible_arr,
    bound_paras,
    notNone_input_parameters,
    if_Outer,
    if_Max,
    DiamThreshold,
):
    """
    outerDiam的话有两种measure形式
    1. 'd_i'和'd_w'来measure
    2. 'd_o'直接来measure
    1和2只能存在一种，不能两种都存在

    InnerDiam的话有两种measure形式
    1. 'd_o'和'd_w'来measure
    2. 'd_i'直接来measure
    1和2只能存在一种，不能两种都存在
    """
    # 得到全部目前已知的非空的input parameters
    input_paras = list(notNone_input_parameters.keys())

    if if_Outer:
        # 如果已经知道了fixed的d_o的值了，就直接check
        if "d_o" in input_paras:
            if if_Max and notNone_input_parameters["d_o"] <= DiamThreshold:
                return feasible_arr
            elif if_Max and notNone_input_parameters["d_o"] > DiamThreshold:
                raise ConstraintFailed(
                    "the d_o is fixed, when do outerDiamMax, d_o bigger than the DiamThreshold"
                )
            elif not if_Max and notNone_input_parameters["d_o"] >= DiamThreshold:
                return feasible_arr
            elif not if_Max and notNone_input_parameters["d_o"] < DiamThreshold:
                raise ConstraintFailed(
                    "the d_o is fixed, when do outerDiamMin, d_o smaller than the DiamThreshold"
                )

        # step 1, check 是否存在对应的dimension,满足上面的两种measure形式的一种
        logic0 = "d_i" in bound_paras and "d_w" in bound_paras
        logic1 = "d_i" in bound_paras and "d_w" in input_paras
        logic2 = "d_i" in input_paras and "d_w" in bound_paras
        logic3 = "d_o" in bound_paras
    else:
        # 如果已经知道了fixed的d_i的值了，就直接check
        if "d_i" in input_paras:
            if if_Max and notNone_input_parameters["d_i"] <= DiamThreshold:
                return feasible_arr
            elif if_Max and notNone_input_parameters["d_i"] > DiamThreshold:
                raise ConstraintFailed(
                    "the d_i is fixed, when do outerDiamMax, d_i bigger than the DiamThreshold"
                )
            elif not if_Max and notNone_input_parameters["d_i"] >= DiamThreshold:
                return feasible_arr
            elif not if_Max and notNone_input_parameters["d_i"] < DiamThreshold:
                raise ConstraintFailed(
                    "the d_i is fixed, when do outerDiamMin, d_i smaller than the DiamThreshold"
                )

        # step 1, check 是否存在对应的dimension,满足上面的两种measure形式的一种
        logic0 = "d_o" in bound_paras and "d_w" in bound_paras
        logic1 = "d_o" in bound_paras and "d_w" in input_paras
        logic2 = "d_o" in input_paras and "d_w" in bound_paras
        logic3 = "d_i" in bound_paras

    logics = [logic0, logic1, logic2, logic3]

    # logic1-logic4需要且只需要存在一个
    if sum(logics) != 1:
        error_msg = (
            "in InnerOuterDiamMaxMin, the input and bound parameter have logic error"
        )
        raise ConstraintPolicyError(error_msg)

    logic_idx = logics.index(1)
    if if_Outer and if_Max:
        return np.array(
            list(
                filter(
                    lambda x: (
                        InnerOuterDiam_combos_calculation(
                            x, notNone_input_parameters, bound_paras, True, logic_idx
                        )
                        <= DiamThreshold
                    ),
                    feasible_arr,
                )
            )
        )
    elif if_Outer and not if_Max:
        return np.array(
            list(
                filter(
                    lambda x: (
                        InnerOuterDiam_combos_calculation(
                            x, notNone_input_parameters, bound_paras, True, logic_idx
                        )
                        >= DiamThreshold
                    ),
                    feasible_arr,
                )
            )
        )
    elif not if_Outer and if_Max:
        return np.array(
            list(
                filter(
                    lambda x: (
                        InnerOuterDiam_combos_calculation(
                            x, notNone_input_parameters, bound_paras, False, logic_idx
                        )
                        <= DiamThreshold
                    ),
                    feasible_arr,
                )
            )
        )
    elif not if_Outer and not if_Max:
        return np.array(
            list(
                filter(
                    lambda x: (
                        InnerOuterDiam_combos_calculation(
                            x, notNone_input_parameters, bound_paras, False, logic_idx
                        )
                        >= DiamThreshold
                    ),
                    feasible_arr,
                )
            )
        )

    return feasible_arr


# 最大剪应力 Maximum Shear Stress, 即最大剪应力最大不超过，或者最小要大于
def constraint_MaximumShearStressMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold,
):
    MaxShearStress_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        MaxShearStress_paras_combinations,
        "MaximumShearStressMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(MaxShearStress_paras_combinations)):
        if len(MaxShearStress_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(MaxShearStress_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                MaximumShearStress_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                MaximumShearStress_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    # print ("in MaximumShearStressMaxMin, the combo index is:")
    # print (combo_idx)
    return feasible_arr


# 线圈绑定间隙 Coil Binding Gap constraint 是当线圈被压缩到其最小长度（Hard Length)时候的线圈节距
def constraint_CoilBindingGapMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):
    CoilBindingGap_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        CoilBindingGap_paras_combinations,
        "CoilBindingGapMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(CoilBindingGap_paras_combinations)):
        if len(CoilBindingGap_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(CoilBindingGap_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                CoilBindingGap_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                CoilBindingGap_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# 弹性比率
def constraint_SpringRateMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    SpringRate_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        SpringRate_paras_combinations,
        "SpringRateMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(SpringRate_paras_combinations)):
        if len(SpringRate_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(SpringRate_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                SpringRate_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                SpringRate_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# 弹簧指数
def constraint_SpringIndexMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    SpringIndex_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        SpringIndex_paras_combinations,
        "SpringIndexMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(SpringIndex_paras_combinations)):
        if len(SpringIndex_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(SpringIndex_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                SpringIndex_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                SpringIndex_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# 高径比（细长比）
def constraint_BucklingSlendernessRatioMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    (
        BucklingSlendernessRatio_miss_paras_combinations,
        input_paras,
    ) = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        BucklingSlendernessRatio_paras_combinations,
        "BucklingSlendernessRatioMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(BucklingSlendernessRatio_paras_combinations)):
        if len(BucklingSlendernessRatio_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(BucklingSlendernessRatio_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                BucklingSlendernessRatio_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                BucklingSlendernessRatio_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# Diametral Expansion 直径膨胀
def constraint_DiametralExpansionMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    DiametralExpansion_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        DiametralExpansion_paras_combinations,
        "DiametralExpansionMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(DiametralExpansion_paras_combinations)):
        if len(DiametralExpansion_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(DiametralExpansion_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                DiametralExpansion_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                DiametralExpansion_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# Stress Relaxation 应力松弛
def constraint_StressRelaxationMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    StressRelaxation_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        StressRelaxation_paras_combinations,
        "StressRelaxationMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(StressRelaxation_paras_combinations)):
        if len(StressRelaxation_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(StressRelaxation_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                StressRelaxation_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                StressRelaxation_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr


# 预紧力 Preload Force
def constraint_PreloadForceMaxMin(
    feasible_arr, bound_paras, notNone_input_parameters, if_Max, Threshold
):

    PreloadForce_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        PreloadForce_paras_combinations,
        "PreloadForceMaxMin",
    )

    # 开始根据不同的combination做计算
    for combo_idx in range(len(PreloadForce_paras_combinations)):
        if len(PreloadForce_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(PreloadForce_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if if_Max:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                PreloadForce_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                <= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )
            else:
                feasible_arr = np.array(
                    list(
                        filter(
                            lambda x: (
                                PreloadForce_combos_calculation(
                                    x, matched_paras, bound_paras, combo_idx
                                )
                                >= Threshold
                            ),
                            feasible_arr,
                        )
                    )
                )

            break

    return feasible_arr
