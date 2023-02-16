from .errors import *
from .constant import *
from .constraint import constraint_firstStepCheck
from .constraint_utils import (
    InnerOuterDiam_combos_calculation,
    MaximumShearStress_combos_calculation,
    CoilBindingGap_combos_calculation,
    SpringRate_combos_calculation,
    SpringIndex_combos_calculation,
    BucklingSlendernessRatio_combos_calculation,
    DiametralExpansion_combos_calculation,
    StressRelaxation_combos_calculation,
    PreloadForce_combos_calculation,
)
from .utils import *
import numpy as np


def optimize_InnerOuterDiamMaxMin(
    design_value, notNone_input_parameters, bound_paras, if_Outer, if_Max, DiamThreshold
):

    # 得到全部目前已知的非空的input parameters
    input_paras = list(notNone_input_parameters.keys())

    if if_Outer:
        # 如果已经知道了fixed的d_o的值了，就直接check
        if "d_o" in input_paras:
            if if_Max and notNone_input_parameters["d_o"] <= DiamThreshold:
                return 1  # 因为在mininze时候constraints只对小于0的做处理，直接赋值1等于不需要处理这个constraint
            elif not if_Max and notNone_input_parameters["d_o"] >= DiamThreshold:
                return 1

        # step 1, check 是否存在对应的dimension,满足上面的两种measure形式的一种
        logic0 = "d_i" in bound_paras and "d_w" in bound_paras
        logic1 = "d_i" in bound_paras and "d_w" in input_paras
        logic2 = "d_i" in input_paras and "d_w" in bound_paras
        logic3 = "d_o" in bound_paras

    else:
        # 如果已经知道了fixed的d_i的值了，就直接check
        if "d_i" in input_paras:
            if if_Max and notNone_input_parameters["d_i"] <= DiamThreshold:
                return 1
            elif not if_Max and notNone_input_parameters["d_i"] >= DiamThreshold:
                return 1

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
        # return的这个值是<0的时候需要受惩罚，当if_Max=True时候，如果max值减去真实值小于0则说明超出了max，故需要惩罚
        return DiamThreshold - InnerOuterDiam_combos_calculation(
            design_value, notNone_input_parameters, bound_paras, True, logic_idx
        )
    elif if_Outer and not if_Max:
        # return的这个值是<0的时候需要受惩罚，当if_Max=False时候，如果真实值减去min值小于0则说明真实值比min还小，故需要惩罚
        return (
            InnerOuterDiam_combos_calculation(
                design_value, notNone_input_parameters, bound_paras, True, logic_idx
            )
            - DiamThreshold
        )
    elif not if_Outer and if_Max:
        return DiamThreshold - InnerOuterDiam_combos_calculation(
            design_value, notNone_input_parameters, bound_paras, False, logic_idx
        )
    elif not if_Outer and not if_Max:
        # return的这个值是<0的时候需要受惩罚，当if_Max=False时候，如果真实值减去min值小于0则说明真实值比min还小，故需要惩罚
        return (
            InnerOuterDiam_combos_calculation(
                design_value, notNone_input_parameters, bound_paras, False, logic_idx
            )
            - DiamThreshold
        )

    return 1


def optimize_MaximumShearStress(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):

    MaxShearStress_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        MaxShearStress_paras_combinations,
        "MaximumShearStressMaxMin",
    )

    for combo_idx in range(len(MaxShearStress_paras_combinations)):
        if len(MaxShearStress_miss_paras_combinations[combo_idx]) == 0:
            # 返回每个变量具体对应在input还是bound parameters里，且具体对应在哪个地方，什么值？
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(MaxShearStress_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )

            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - MaximumShearStress_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        MaximumShearStress_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return MaximumShearStress_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


def optimize_CoilBindingGap(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):

    CoilBindingGap_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        CoilBindingGap_paras_combinations,
        "CoilBindingGapMaxMin",
    )

    for combo_idx in range(len(CoilBindingGap_paras_combinations)):
        if len(CoilBindingGap_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(CoilBindingGap_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - CoilBindingGap_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        CoilBindingGap_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return CoilBindingGap_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


# 弹性比率
def optimize_SpringRate(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):
    SpringRate_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        SpringRate_paras_combinations,
        "SpringRateMaxMin",
    )

    for combo_idx in range(len(SpringRate_paras_combinations)):
        if len(SpringRate_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(SpringRate_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - SpringRate_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        SpringRate_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return SpringRate_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


# 弹簧指数
def optimize_SpringIndex(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):
    SpringIndex_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        SpringIndex_paras_combinations,
        "SpringIndexMaxMin",
    )

    for combo_idx in range(len(SpringIndex_paras_combinations)):
        if len(SpringIndex_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(SpringIndex_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - SpringIndex_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        SpringIndex_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return SpringIndex_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


#  高径比（细长比）
def optimize_BucklingSlendernessRatio(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
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

    for combo_idx in range(len(BucklingSlendernessRatio_paras_combinations)):
        if len(BucklingSlendernessRatio_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(BucklingSlendernessRatio_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - BucklingSlendernessRatio_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        BucklingSlendernessRatio_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return BucklingSlendernessRatio_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


#  Diametral Expansion 直径膨胀
def optimize_DiametralExpansion(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):
    DiametralExpansion_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        DiametralExpansion_paras_combinations,
        "DiametralExpansionMaxMin",
    )

    for combo_idx in range(len(DiametralExpansion_paras_combinations)):
        if len(DiametralExpansion_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(DiametralExpansion_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - DiametralExpansion_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        DiametralExpansion_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return DiametralExpansion_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


# Stress Relaxation 应力松弛
def optimize_StressRelaxation(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):
    StressRelaxation_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        StressRelaxation_paras_combinations,
        "StressRelaxationMaxMin",
    )

    for combo_idx in range(len(StressRelaxation_paras_combinations)):
        if len(StressRelaxation_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(StressRelaxation_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - StressRelaxation_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        StressRelaxation_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return StressRelaxation_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1


# Stress Relaxation 应力松弛
def optimize_PreloadForce(
    design_value,
    notNone_input_parameters,
    bound_paras,
    if_Max,
    Threshold,
    constraintOrtarget,
):
    PreloadForce_miss_paras_combinations, input_paras = constraint_firstStepCheck(
        notNone_input_parameters,
        bound_paras,
        PreloadForce_paras_combinations,
        "PreloadForceMaxMin",
    )

    for combo_idx in range(len(PreloadForce_paras_combinations)):
        if len(PreloadForce_miss_paras_combinations[combo_idx]) == 0:
            matched_paras = match_constraintInput_fromInputBoundParameters(
                list(PreloadForce_paras_combinations[combo_idx]),
                input_paras,
                bound_paras,
                notNone_input_parameters,
            )
            if constraintOrtarget == "constraint":
                if if_Max:
                    return Threshold - PreloadForce_combos_calculation(
                        design_value, matched_paras, bound_paras, combo_idx
                    )
                else:
                    return (
                        PreloadForce_combos_calculation(
                            design_value, matched_paras, bound_paras, combo_idx
                        )
                        - Threshold
                    )
            elif constraintOrtarget == "target":
                return PreloadForce_combos_calculation(
                    design_value, matched_paras, bound_paras, combo_idx
                )

    return 1
