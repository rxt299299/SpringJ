from .constant import *
from .calculation import *
from .errors import *
import math


def missParas(matched_paras, combo_parameters, constraint_name):
    # matched_paras必须要全部包含这些参数
    if not (all(x in matched_paras.keys() for x in combo_parameters)):
        raise ConstraintMissingParas(constraint_name)


# 普通的match, 没有任何附加条件的时候，因为这个经常重复出现，故写成一个function
def general_match_input_bound(para, matched_paras, bound_paras, x):
    if matched_paras[para][0] == "input":
        return matched_paras[para][1]
    else:
        # 如果是bound input, 先用bound_paras找到其对应的index,然后x是一行，
        # 因此把index填到x上
        return x[bound_paras.index(para)]


# N_t和end_closed对N_a的逻辑
def N_a_end_closed_to_N_t(input_or_bound, end_closed_value, N_a_value, bound_paras, x):
    # return MaximumShearStress_paradict["N_a"]
    if input_or_bound == "input":
        if end_closed_value:
            return N_a_value + 2
        else:
            return N_a_value + 1
    else:  # input_or_bound == "bound"
        if end_closed_value:
            return x[bound_paras.index("N_a")] + 2
        else:
            return x[bound_paras.index("N_a")] + 1


# N_t和end_closed对N_a的逻辑
def N_t_end_closed_to_N_a(input_or_bound, end_closed_value, N_t_value, bound_paras, x):
    # return MaximumShearStress_paradict["N_a"]
    if input_or_bound == "input":
        if end_closed_value:
            return N_t_value - 2
        else:
            return N_t_value - 1
    else:  # input_or_bound == "bound"
        if end_closed_value:
            return x[bound_paras.index("N_t")] - 2
        else:
            return x[bound_paras.index("N_t")] - 1


# 最大最小内外径输入filter函数参数
def InnerOuterDiam_combos_calculation(
    x, notNone_input_parameters, bound_paras, if_Outer, logic_idx
):
    if if_Outer:
        if logic_idx == 0:
            return x[bound_paras.index("d_i")] + 2 * x[bound_paras.index("d_w")]
        elif logic_idx == 1:
            return x[bound_paras.index("d_i")] + 2 * notNone_input_parameters["d_w"]
        elif logic_idx == 2:
            return notNone_input_parameters["d_i"] + 2 * x[bound_paras.index("d_w")]
        elif logic_idx == 3:
            return x[bound_paras.index("d_o")]
    else:
        if logic_idx == 0:
            return x[bound_paras.index("d_o")] - 2 * x[bound_paras.index("d_w")]
        elif logic_idx == 1:
            return x[bound_paras.index("d_o")] - 2 * notNone_input_parameters["d_w"]
        elif logic_idx == 2:
            return notNone_input_parameters["d_o"] - 2 * x[bound_paras.index("d_w")]
        elif logic_idx == 3:
            return x[bound_paras.index("d_i")]


# 最大剪应力输入filter函数参数
def MaximumShearStress_combos_calculation(
    x, matched_paras, bound_paras, combo_idx  # x为feasible_arr的一行
):

    # print ("matched_paras")
    # print (matched_paras)
    # print ("combo_idx")
    # print (combo_idx)

    MaximumShearStress_paradict = {}
    # 先Match x 和bound_paras
    if combo_idx == 0:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_i", "d_w", "N_a", "G", "L_free", "L_hard"]

        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        # general match with no condition
        for para in combo_parameters:
            MaximumShearStress_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_i", "d_w", "N_t", "end_closed", "G", "L_free", "L_hard"] 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                MaximumShearStress_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                MaximumShearStress_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

    elif combo_idx == 2:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_w", "d_o", "N_a", "G", "L_free", "L_hard"] 没有d_i,但是有d_w和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        # general match with no condition
        for para in combo_parameters:
            MaximumShearStress_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_i的值补上
        MaximumShearStress_paradict["d_i"] = (
            MaximumShearStress_paradict["d_o"] - 2 * MaximumShearStress_paradict["d_w"]
        )

    elif combo_idx == 3:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_i", "d_o", "N_a", "G", "L_free", "L_hard"] 没有d_w,但是有d_i和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        # general match with no condition
        for para in combo_parameters:
            MaximumShearStress_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        MaximumShearStress_paradict["d_w"] = (
            MaximumShearStress_paradict["d_o"] - MaximumShearStress_paradict["d_i"]
        ) / 2

    elif combo_idx == 4:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_w", "d_o","N_t", "end_closed", "G", "L_free", "L_hard"] 没有d_i,但是有d_w和d_o, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                MaximumShearStress_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                MaximumShearStress_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_i的值补上
        MaximumShearStress_paradict["d_i"] = (
            MaximumShearStress_paradict["d_o"] - 2 * MaximumShearStress_paradict["d_w"]
        )

    elif combo_idx == 5:
        combo_parameters = MaxShearStress_paras_combinations[
            combo_idx
        ]  # ["d_i", "d_o","N_t", "end_closed", "G", "L_free", "L_hard"] 没有d_w,但是有d_i和d_o, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "MaximumShearStress")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                MaximumShearStress_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                MaximumShearStress_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_i的值补上
        MaximumShearStress_paradict["d_w"] = (
            MaximumShearStress_paradict["d_o"] - MaximumShearStress_paradict["d_i"]
        ) / 2

    # print (MaximumShearStress_paradict)
    return MaximumShearStress_calculation(MaximumShearStress_paradict)


# 线圈绑定间隙输入filter函数参数
def CoilBindingGap_combos_calculation(
    x, matched_paras, bound_paras, combo_idx
):  # x为feasible_arr的一行

    CoilBindingGap_paradict = {}

    if combo_idx == 0:
        combo_parameters = CoilBindingGap_paras_combinations[
            combo_idx
        ]  # ["N_t", "d_w", "L_hard"], #原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "CoilBindingGap")

        # general match with no condition
        for para in combo_parameters:
            CoilBindingGap_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = CoilBindingGap_paras_combinations[
            combo_idx
        ]  # ["N_a", "end_closed", "d_w", "L_hard"], #没有N_t, 但是有N_a和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "CoilBindingGap")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_a":
                CoilBindingGap_paradict["N_t"] = N_a_end_closed_to_N_t(
                    matched_paras["N_a"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_a"][1],
                    bound_paras,
                    x,
                )
            else:
                CoilBindingGap_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

    elif combo_idx == 2:
        combo_parameters = CoilBindingGap_paras_combinations[
            combo_idx
        ]  # ["N_t", "d_i", "d_o", "L_hard"], # 没有d_w,但是有d_i和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "CoilBindingGap")

        # general match with no condition
        for para in combo_parameters:
            CoilBindingGap_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        CoilBindingGap_paradict["d_w"] = (
            CoilBindingGap_paradict["d_o"] - CoilBindingGap_paradict["d_i"]
        ) / 2

    elif combo_idx == 3:
        combo_parameters = CoilBindingGap_paras_combinations[
            combo_idx
        ]  # ["N_a", "end_closed", "d_i", "d_o", "L_hard"], #没有N_t, 但是有N_a和end_closed, 没有d_w,但是有d_i和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "CoilBindingGap")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_a":
                CoilBindingGap_paradict["N_t"] = N_a_end_closed_to_N_t(
                    matched_paras["N_a"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_a"][1],
                    bound_paras,
                    x,
                )
            else:
                CoilBindingGap_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_w的值补上
        CoilBindingGap_paradict["d_w"] = (
            CoilBindingGap_paradict["d_o"] - 2 * CoilBindingGap_paradict["d_i"]
        ) / 2

    return CoilBindingGap_calculation(CoilBindingGap_paradict)


# 弹性比率
def SpringRate_combos_calculation(x, matched_paras, bound_paras, combo_idx):

    SpringRate_paradict = {}

    if combo_idx == 0:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # ["G", "N_a", "d_w", "d_i"], #原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        # general match with no condition
        for para in combo_parameters:
            SpringRate_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )
    elif combo_idx == 1:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # ["G", "N_t", "end_closed", "d_w", "d_i"]), # 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                SpringRate_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                SpringRate_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )
    elif combo_idx == 2:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # ["G", "N_a", "d_i", "d_o"], # 没有d_w,但是有d_i和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        # general match with no condition
        for para in combo_parameters:
            SpringRate_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        SpringRate_paradict["d_w"] = (
            SpringRate_paradict["d_o"] - SpringRate_paradict["d_i"]
        ) / 2

    elif combo_idx == 3:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # ["G", "N_a", "d_w", "d_o"], # 没有d_i, 但是有d_w和d_o
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        # general match with no condition
        for para in combo_parameters:
            SpringRate_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        SpringRate_paradict["d_i"] = (
            SpringRate_paradict["d_o"] - 2 * SpringRate_paradict["d_w"]
        )

    elif combo_idx == 4:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # (["G", "N_t", "end_closed", "d_i", "d_o"], # 没有d_w, 但是有d_i和d_o, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                SpringRate_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                SpringRate_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_w的值补上
        SpringRate_paradict["d_w"] = (
            SpringRate_paradict["d_o"] - SpringRate_paradict["d_i"]
        ) / 2

    elif combo_idx == 5:
        combo_parameters = SpringRate_paras_combinations[
            combo_idx
        ]  # (["G", "N_t", "end_closed", "d_w", "d_o"]), # 没有d_i, 但是有d_w和d_o, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringRate")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                SpringRate_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                SpringRate_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_w的值补上
        SpringRate_paradict["d_i"] = (
            SpringRate_paradict["d_o"] - 2 * SpringRate_paradict["d_w"]
        )

    return SpringRate_calculation(SpringRate_paradict)


# 弹性比率
def SpringIndex_combos_calculation(x, matched_paras, bound_paras, combo_idx):

    SpringIndex_paradict = {}

    if combo_idx == 0:
        combo_parameters = SpringIndex_paras_combinations[
            combo_idx
        ]  # ['d_i', 'd_w'],  # 原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringIndex")

        # general match with no condition
        for para in combo_parameters:
            SpringIndex_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = SpringIndex_paras_combinations[
            combo_idx
        ]  # ['d_i', 'd_o']),  # 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringIndex")

        # general match with no condition
        for para in combo_parameters:
            SpringIndex_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        SpringIndex_paradict["d_w"] = (
            SpringIndex_paradict["d_o"] - SpringIndex_paradict["d_i"]
        ) / 2

    elif combo_idx == 2:
        combo_parameters = SpringIndex_paras_combinations[
            combo_idx
        ]  # ['d_o', 'd_w']),  # 没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "SpringIndex")

        # general match with no condition
        for para in combo_parameters:
            SpringIndex_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        SpringIndex_paradict["d_i"] = (
            SpringIndex_paradict["d_o"] - 2 * SpringIndex_paradict["d_w"]
        )

    return SpringIndex_calculation(SpringIndex_paradict)


# 高径比（细长比）
def BucklingSlendernessRatio_combos_calculation(
    x, matched_paras, bound_paras, combo_idx
):

    BucklingSlendernessRatio_paradict = {}

    if combo_idx == 0:
        combo_parameters = BucklingSlendernessRatio_paras_combinations[
            combo_idx
        ]  # ['L_free', 'd_i', 'd_w'],  # 原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "BucklingSlendernessRatio")

        # general match with no condition
        for para in combo_parameters:
            BucklingSlendernessRatio_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = BucklingSlendernessRatio_paras_combinations[
            combo_idx
        ]  # ['L_free','d_i', 'd_o']),  # 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "BucklingSlendernessRatio")

        # general match with no condition
        for para in combo_parameters:
            BucklingSlendernessRatio_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        BucklingSlendernessRatio_paradict["d_w"] = (
            BucklingSlendernessRatio_paradict["d_o"]
            - BucklingSlendernessRatio_paradict["d_i"]
        ) / 2

    elif combo_idx == 2:
        combo_parameters = BucklingSlendernessRatio_paras_combinations[
            combo_idx
        ]  # ['L_free','d_o', 'd_w']),  # 没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "BucklingSlendernessRatio")

        # general match with no condition
        for para in combo_parameters:
            BucklingSlendernessRatio_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        BucklingSlendernessRatio_paradict["d_i"] = (
            BucklingSlendernessRatio_paradict["d_o"]
            - 2 * BucklingSlendernessRatio_paradict["d_w"]
        )

    return BucklingSlendernessRatio_calculation(BucklingSlendernessRatio_paradict)


# Diametral Expansion 直径膨胀
def DiametralExpansion_combos_calculation(x, matched_paras, bound_paras, combo_idx):

    DiametralExpansion_paradict = {}

    if combo_idx == 0:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ['L_free', "N_a", "d_i", "d_w"],  # 原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ['L_free', "N_a", "d_i", "d_o"]),  # 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        DiametralExpansion_paradict["d_w"] = (
            DiametralExpansion_paradict["d_o"] - DiametralExpansion_paradict["d_i"]
        ) / 2

    elif combo_idx == 2:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ['L_free', "N_a", "d_o", "d_w"]),  # 没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        DiametralExpansion_paradict["d_i"] = (
            DiametralExpansion_paradict["d_o"] - 2 * DiametralExpansion_paradict["d_w"]
        )

    elif combo_idx == 3:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ["L_free", "N_t", "d_i", "d_w"]),  # 没有N_a, 有N_t
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把N_a的值补上
        DiametralExpansion_paradict["N_a"] = DiametralExpansion_paradict["N_t"] - 2

    elif combo_idx == 4:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ["L_free", "N_t", "d_i", "d_o"]),  # 没有N_a, 有N_t, 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        DiametralExpansion_paradict["d_w"] = (
            DiametralExpansion_paradict["d_o"] - DiametralExpansion_paradict["d_i"]
        ) / 2

        # 把N_a的值补上
        DiametralExpansion_paradict["N_a"] = DiametralExpansion_paradict["N_t"] - 2

    elif combo_idx == 5:
        combo_parameters = DiametralExpansion_paras_combinations[
            combo_idx
        ]  # ["L_free", "N_t", "d_o", "d_w"]),  # 没有N_a, 有N_t,  没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "DiametralExpansion")

        # general match with no condition
        for para in combo_parameters:
            DiametralExpansion_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        DiametralExpansion_paradict["d_i"] = (
            DiametralExpansion_paradict["d_o"] - 2 * DiametralExpansion_paradict["d_w"]
        )

        # 把N_a的值补上
        DiametralExpansion_paradict["N_a"] = DiametralExpansion_paradict["N_t"] - 2

    return DiametralExpansion_calculation(DiametralExpansion_paradict)


# Stress Relaxation 应力松弛
def StressRelaxation_combos_calculation(x, matched_paras, bound_paras, combo_idx):

    StressRelaxation_paradict = {}

    if combo_idx == 0:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_w", "d_i", "N_a"], #原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        # general match with no condition
        for para in combo_parameters:
            StressRelaxation_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_o", "d_i", "N_a"]), # 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        # general match with no condition
        for para in combo_parameters:
            StressRelaxation_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        StressRelaxation_paradict["d_w"] = (
            StressRelaxation_paradict["d_o"] - StressRelaxation_paradict["d_i"]
        ) / 2

    elif combo_idx == 2:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_o", "d_w", "N_a"]), # 没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        # general match with no condition
        for para in combo_parameters:
            StressRelaxation_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_i的值补上
        StressRelaxation_paradict["d_i"] = (
            StressRelaxation_paradict["d_o"] - 2 * StressRelaxation_paradict["d_w"]
        )

    elif combo_idx == 3:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_w", "d_i", "N_t", "end_closed"]), # 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                StressRelaxation_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                StressRelaxation_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

    elif combo_idx == 4:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_o", "d_i", "N_t", "end_closed"]), # 没有d_w, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                StressRelaxation_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                StressRelaxation_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_w的值补上
        StressRelaxation_paradict["d_w"] = (
            StressRelaxation_paradict["d_o"] - StressRelaxation_paradict["d_i"]
        ) / 2

    elif combo_idx == 5:
        combo_parameters = StressRelaxation_paras_combinations[
            combo_idx
        ]  # StressRelaxation_fixed_paras+["d_o", "d_w", "N_t", "end_closed"]), # 没有d_i, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "StressRelaxation")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                StressRelaxation_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                StressRelaxation_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_i的值补上
        StressRelaxation_paradict["d_i"] = (
            StressRelaxation_paradict["d_o"] - 2 * StressRelaxation_paradict["d_w"]
        )

    return StressRelaxation_calculation(StressRelaxation_paradict)


# 预紧力 Preload Force
def PreloadForce_combos_calculation(x, matched_paras, bound_paras, combo_idx):

    PreloadForce_paradict = {}

    if combo_idx == 0:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_a", "d_w", "d_i", # 原始参数
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        # general match with no condition
        for para in combo_parameters:
            PreloadForce_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

    elif combo_idx == 1:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_a", "d_o", "d_i", # 没有d_w
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        # general match with no condition
        for para in combo_parameters:
            PreloadForce_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_w的值补上
        PreloadForce_paradict["d_w"] = (
            PreloadForce_paradict["d_o"] - PreloadForce_paradict["d_i"]
        ) / 2

    elif combo_idx == 2:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_a", "d_o", "d_w", # 没有d_i
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        # general match with no condition
        for para in combo_parameters:
            PreloadForce_paradict[para] = general_match_input_bound(
                para, matched_paras, bound_paras, x
            )

        # 把d_i的值补上
        PreloadForce_paradict["d_i"] = (
            PreloadForce_paradict["d_o"] - 2 * PreloadForce_paradict["d_w"]
        )

    elif combo_idx == 3:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_t", "end_closed", "d_w", "d_i", # 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                PreloadForce_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                PreloadForce_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

    elif combo_idx == 4:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_t", "end_closed", "d_o", "d_i"]), # 没有d_w, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                PreloadForce_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                PreloadForce_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_w的值补上
        PreloadForce_paradict["d_w"] = (
            PreloadForce_paradict["d_o"] - PreloadForce_paradict["d_i"]
        ) / 2

    elif combo_idx == 5:
        combo_parameters = PreloadForce_paras_combinations[
            combo_idx
        ]  # "L_free", "L_solid", "G", "N_t", "end_closed", "d_o", "d_w"]), # 没有d_i, 没有N_a, 但是有N_t和end_closed
        # matched_paras必须要全部包含这些参数
        missParas(matched_paras, combo_parameters, "PreloadForce")

        for para in combo_parameters:
            if para == "end_closed":
                continue
            elif para == "N_t":
                PreloadForce_paradict["N_a"] = N_t_end_closed_to_N_a(
                    matched_paras["N_t"][0],
                    matched_paras["end_closed"][1],
                    matched_paras["N_t"][1],
                    bound_paras,
                    x,
                )
            else:
                PreloadForce_paradict[para] = general_match_input_bound(
                    para, matched_paras, bound_paras, x
                )

        # 把d_i的值补上
        PreloadForce_paradict["d_i"] = (
            PreloadForce_paradict["d_o"] - 2 * PreloadForce_paradict["d_w"]
        )

    return PreloadForce_calculation(PreloadForce_paradict)
