import sys

# setting path
sys.path.append("D:/work/GitHub/StreamlitApps/Spring/SpringDesign/")

from .constraint import *
from .constant import *
from .calculation import BucklingSlendernessRatio_threshold
from .errors import *
import math
import numpy as np
from .optimize import *
from scipy.stats import qmc
from .utils import *

"""
全部输入的参数, 单位都统一为毫米mm
"""


class Spring:
    def __init__(self, input_parameters, constraint_policy, objective):
        """
        #各个input的输入例子

        input_parameters = {
            'end_closed':True,
            'L_free':85.5,
            'L_hard':20,
            'G':77,
            'Poisson_ratio': 0.3,
        }

        constraint_policy = {
            'outerDiamMax':60,
            'MaximumShearStressMax': 0.7,
            'CoilBindingGapMin': 0.5,
            'BucklingSlendernessRatioMax': (True, 3.705), #if_use_Poisson_ratio, value if not use Poisson_ratio
            'DiametralExpansionMax': 35,
        }

        objective = {
            'spring_rate_spring_index': {'MaxorMin':'min', 'k_max': 20, 'c_max':10}
        }

        bounds_inputs = {'d_i':[20, 30], 'd_w':[1, 5], 'N_t':[9, 17]}
        """
        self.r = parameter_initial("r", "int", input_parameters)
        self.input_parameters = input_parameters
        self.constraint_policy = constraint_policy
        self.objective = objective

        #######################################
        ### Input Parameters ##################
        #######################################

        # True or False, 代表弹簧末端线圈是否闭合
        self.end_closed = parameter_initial("end_closed", "bool", input_parameters)
        # 总线圈数
        self.N_t = parameter_initial("N_t", "int", input_parameters)
        # 有效线圈数，如果弹簧末端线圈是否闭合N_t = N_a+2, 如果未闭合N_t = N_a+1
        self.N_a = parameter_initial("N_a", "int", input_parameters)

        # 线径，钢丝直径
        self.d_w = parameter_initial("d_w", "int_or_float", input_parameters)
        # 内径，弹簧内圈直径
        self.d_i = parameter_initial("d_i", "int_or_float", input_parameters)
        # 外径，弹簧外圈直径 d_o=d_i+2*d_w
        self.d_o = parameter_initial("d_o", "int_or_float", input_parameters)

        # Free Length, 自由长度，当没有任何外力作用时候的弹簧自然长度
        self.L_free = parameter_initial("L_free", "int_or_float", input_parameters)
        # Open Length, 静止长度，弹簧在其应用中的静止长度
        self.L_open = parameter_initial("L_open", "int_or_float", input_parameters)
        # Hard Length, 最小长度，弹簧在指定力下可以压缩到的最小长度
        self.L_hard = parameter_initial("L_hard", "int_or_float", input_parameters)

        # Deflection, 变形量，弹簧沿负荷方向产生的相对位移
        self.deflection = parameter_initial(
            "deflection", "int_or_float", input_parameters
        )
        # Young's Modulus (E，Elastic Modulus), 杨氏模量,又称弹性系数
        self.Young = parameter_initial("Young", "int_or_float", input_parameters)
        # Poisson Ratio, 泊松比，表示在一方向拉伸后，在其他方向收缩的比值
        self.Poisson_ratio = parameter_initial(
            "Poisson_ratio", "int_or_float", input_parameters
        )
        # Shear Modulus, 剪力模数，剪应力与剪应变的比值
        self.G = parameter_initial("G", "int_or_float", input_parameters)

        # # k spring rate, 弹性比率，测量弹簧的刚度
        # self.k = parameter_initial("k", "int_or_float", input_parameters)
        # # c spring index, 弹性指数，衡量弹簧内径与线径比
        # self.c = parameter_initial("c", "int_or_float", input_parameters)

        # 应力松弛 Stress Relaxation 是测量弹簧力在高温且时间t的恒定压缩的条件下的衰减程度
        # 该公式是使用诺顿-贝利定律推导出来的，其中 c， n 和 k 是与温度相关的材料特定常数
        # Norton Bailey c
        self.NB_c = parameter_initial("NB_c", "int_or_float", input_parameters)
        # Norton Bailey n
        self.NB_n = parameter_initial("NB_n", "int_or_float", input_parameters)
        # Norton Bailey k
        self.NB_k = parameter_initial("NB_k", "int_or_float", input_parameters)
        # time Stress Relaxation
        self.time_stress_Relaxation = parameter_initial(
            "time_stress_Relaxation", "int_or_float", input_parameters
        )
        # Stress Relaxation Gsr 应力松弛是测量弹簧力在高温且时间t的恒定压缩条件下的衰减程度
        self.Gsr = parameter_initial("Gsr", "int_or_float", input_parameters)

        #######################################
        ### Constraints #######################
        #######################################
        # 弹簧外径的最大值
        # self.inner_outer_relation = parameter_initial_constraint(
        #     "outerDiamMax", constraint_policy
        # )
        # # Coil Binding Gap, 线圈绑定间隙，当线圈被压缩到其最小长度时候的线圈截距
        # self.coil_binding_gap = parameter_initial_constraint(
        #     "coil_binding_gap", constraint_policy
        # )
        # # Maximum Shear Stress,可以施加到弹簧上的最大剪应力
        # self.shear_stress = parameter_initial_constraint(
        #     "shear_stress", constraint_policy
        # )
        # # Stress Relaxation,应力松弛，测量弹簧力在高温且时间t的恒定压缩条件下的衰减程度
        # self.stress_relaxation = parameter_initial_constraint(
        #     "stress_relaxation", constraint_policy
        # )

        ########################################
        ### Objective ##########################
        ########################################
        # 先做initialize check, 看看有没有什么输入量是不合适的
        # 有的constraint_policy比较复杂，是在自己的function里面去检验的，比如最大剪力MaximumShearStress
        self.initialize_check_input_parameters()
        self.initialize_check_constraint_policy()
        self.initialize_check_optimize_target()
        # 根据input parameters, 如果能够直接计算出来一些其他没有输入的parameters, 这里补上
        self.filling_parameters()
        # 对于已知的变量，包括被输入的或者后续被filling的变量，确定他们在其range里面
        self.parameters_range_check()

    # 先做initialize check, 看看有没有什么输入量是不合适的
    def initialize_check_input_parameters(self):
        # print ("----start check the initial of the spring parameters----")
        nonexist_parameters(input_parameter_names, self.input_parameters)

        #######################################################
        ####检查input_parameters里面是否存在逻辑漏洞#############
        # 检查 1
        # 有效线圈数，如果弹簧末端线圈是否闭合N_t = N_a+2, 如果未闭合N_t = N_a+1
        if (
            self.end_closed is not None
            and self.N_t is not None
            and self.N_a is not None
        ):
            if self.end_closed and self.N_t != self.N_a + 2:
                raise InputParametersLogicError("when end closed, N_t should be N_a+2")
            elif not self.end_closed and self.N_t != self.N_a + 1:
                raise InputParametersLogicError(
                    "when not end closed, N_t should be N_a+1"
                )
        # 如果知道N_t, N_a不知道end_closed, 但是前两者的差既不是1也不是2，则报错
        if self.end_closed is None and self.N_t is not None and self.N_a is not None:
            if self.N_t - self.N_a not in (1, 2):
                raise InputParametersLogicError(
                    "when N_t and N_a know, the Difference should be 1 or 2"
                )

        # 检查 2
        # 外径，弹簧外圈直径 d_o=d_i+2*d_w
        if self.d_o is not None and self.d_i is not None and self.d_w is not None:
            if self.d_i + 2 * self.d_w != self.d_o:
                raise InputParametersLogicError(
                    "when d_i, d_o and d_w both exists in input, d_o should be d_i+2*d_w"
                )

        # 检查 3
        #  "L_free",  "L_open",  "L_hard",如果这几个知道的话是有大小关系的
        if self.L_free is not None and self.L_open is not None:
            if not self.L_free >= self.L_open:
                raise InputParametersLogicError(
                    "when L_free and L_open both exists in input, L_free should >= L_open"
                )
        if self.L_free is not None and self.L_hard is not None:
            if not self.L_free >= self.L_hard:
                raise InputParametersLogicError(
                    "when L_free and L_hard both exists in input, L_free should >= L_hard"
                )
        if self.L_open is not None and self.L_hard is not None:
            if not self.L_open >= self.L_hard:
                raise InputParametersLogicError(
                    "when L_open and L_hard both exists in input, L_open should >= L_hard"
                )

    def initialize_check_constraint_policy(self):

        nonexist_parameters(constraints_parameter_names, self.constraint_policy)

        # constraint_policy这个还需要一些check, 比如每一个constraint只能出现一次
        if not len(self.constraint_policy.keys()) == len(
            set(self.constraint_policy.keys())
        ):
            raise UniqueConstraintPolicyError()

        ########################################################
        ########################################################
        ####这里需要修改且加上每一个的固定格式！！！
        ########################################################
        ########################################################

        def check_int_or_float(threshold):
            logic1 = not isinstance(threshold, int)
            logic2 = not isinstance(threshold, float)
            if logic1 and logic2:
                raise Error(constraint + " input must be int or float")

        # 且每一个的格式必须是固定的
        for constraint in self.constraint_policy.keys():
            if constraint in constraint_value_must_number:
                threshold = self.constraint_policy[constraint]
                check_int_or_float(threshold)

                # 如果使用DiametralExpansion constraint, 那么必须要满足弹簧闭合条件
                if constraint in ("DiametralExpansionMax", "DiametralExpansionMin"):
                    if not self.end_closed:
                        raise Error(
                            "only end_closed Spring accpet constraint DiametralExpansion, please check your end_closed parameter"
                        )
            elif constraint in constraint_BucklingSlendernessRatio:
                # BucklingSlendernessRatioMax, BucklingSlendernessRatioMin
                if len(self.constraint_policy[constraint]) != 2:
                    raise Error(
                        "input of constraint BucklingSlendernessRatio must have input of length 2"
                    )
                if_Poisson, threshold = self.constraint_policy[constraint]
                # BucklingSlendernessRatio constraint有两个输入
                # 第一个就是是否要通过别的已知参数Poisson Ratio计算Threshold,
                # 第二种是直接给出一个Threshold
                # 如果第一种为true那么便不需要检验第二种
                if not isinstance(if_Poisson, bool):
                    raise Error(
                        "1st input of constraint BucklingSlendernessRatio must be Boolean"
                    )
                if if_Poisson:
                    if self.Poisson_ratio is None:
                        raise Error(
                            "when 1st input of constraint BucklingSlendernessRatio True, we must have input parameter Poisson_ratio"
                        )
                else:
                    check_int_or_float(threshold)

    def initialize_check_optimize_target(self):
        nonexist_parameters(optimize_parameter_name, self.objective)
        # optimize_target这个还需要一些check, 比如目前只支持一个函数，因为这个输入的长度必须为1
        if not len(self.objective.keys()) == 1:
            error_msg = "there only allow one optimize target"
            raise OptimizeTargetInitialError(error_msg)

        ########################################################
        ########################################################
        ####这里需要修改且加上每一个的固定格式！！！
        ########################################################
        ########################################################
        # 注意目前我们只支持一个optimize target, 不支持combine的，之后我们会加上
        optimize_name = list(self.objective.keys())[0]

        # spring_rate_spring_index 的输入必须有'MaxorMin', 'k_max', 'c_max'这些key且，第一个的输入必须是max/min, 后两个的输入必须是int/float
        if optimize_name == "spring_rate_spring_index":
            if not set(self.objective[optimize_name].keys()) == set(
                ["MaxorMin", "k_max", "c_max"]
            ):
                error_msg = "the spring_rate_spring_index input must contains key 'MaxorMin', 'k_max', 'c_max'"
                raise OptimizeTargetInitialError(error_msg)
            elif self.objective[optimize_name]["MaxorMin"] not in ("min", "max"):
                error_msg = (
                    "the spring_rate_spring_index 'MaxorMin' must be 'min' or 'max'"
                )
                raise OptimizeTargetInitialError(error_msg)
            else:
                k_max = self.objective[optimize_name]["k_max"]
                logic1 = not isinstance(k_max, int)
                logic2 = not isinstance(k_max, float)
                if logic1 and logic2:
                    raise OptimizeTargetInitialError(
                        "the spring_rate_spring_index 'k_max' must be int or float"
                    )
                c_max = self.objective[optimize_name]["c_max"]
                logic1 = not isinstance(c_max, int)
                logic2 = not isinstance(c_max, float)
                if logic1 and logic2:
                    raise OptimizeTargetInitialError(
                        "the spring_rate_spring_index 'c_max' must be int or float"
                    )

    # 根据input parameters, 如果能够直接计算出来一些其他没有输入的parameters, 这里补上
    def filling_parameters(self):
        # 如果end_closed, N_t, N_a两个知道一个，就可以直接补齐第三个
        if self.end_closed is not None and self.N_a is None and self.N_t is not None:
            if self.end_closed:
                self.N_a = self.N_t - 2
            else:
                self.N_a = self.N_t - 1

        elif self.end_closed is not None and self.N_a is not None and self.N_t is None:
            if self.end_closed:
                self.N_t = self.N_a + 2
            else:
                self.N_t = self.N_t + 1

        elif self.end_closed is None and self.N_a is not None and self.N_t is not None:
            if self.N_t == self.N_a + 2:
                self.end_closed = True
            else:
                self.end_closed = False

        # 如果d_o, d_i, d_w两个知道一个，就可以直接补齐第三个
        if self.d_o is not None and self.d_i is not None and self.d_w is None:
            self.d_w = (self.d_o - self.d_i) / 2
        elif self.d_o is not None and self.d_i is None and self.d_w is not None:
            self.d_i = self.d_o - 2 * self.d_w
        elif self.d_o is None and self.d_i is not None and self.d_w is not None:
            self.d_o = self.d_i + 2 * self.d_w

    # 对于已知的变量，包括被输入的或者后续被filling的变量，确定他们在其range里面
    def parameters_range_check(self):
        # filling 完成之后，提取出目前可以得到的全部已知的input parameters的list
        overall_input_parameters = {
            "end_closed": self.end_closed,
            "N_t": self.N_t,
            "N_a": self.N_a,
            "d_w": self.d_w,
            "d_i": self.d_i,
            "d_o": self.d_o,
            "L_free": self.L_free,
            "L_open": self.L_open,
            "L_hard": self.L_hard,
            "deflection": self.deflection,
            "Young": self.Young,
            "Poisson_ratio": self.Poisson_ratio,
            "G": self.G,
            # "k": self.k,
            # "c": self.c,
            "NB_c": self.NB_c,
            "NB_n": self.NB_n,
            "NB_k": self.NB_k,
            "time_stress_Relaxation": self.time_stress_Relaxation,
            "Gsr": self.Gsr,
        }

        # 得到全部目前已知的非空的input parameters, self.notNone_input_parameters可能之后其他地方还要调用
        self.notNone_input_parameters = {}
        for parameter in overall_input_parameters.keys():
            if overall_input_parameters[parameter] is not None:
                self.notNone_input_parameters[parameter] = overall_input_parameters[
                    parameter
                ]

        # 检查已经知道的非空参数（包括原始输入的和后来filling的）是否在合适的range里面？
        for input_para_name in self.notNone_input_parameters.keys():
            # 这些输入参数进行大于0的检验
            if input_para_name in input_parameter_names_range_above0:
                range_check_above_zero(
                    input_para_name, overall_input_parameters[input_para_name]
                )

    # 可行性分析
    # example for one of bounds inputs, when we set bounds for d_i, d_w and N_t
    # bounds_inputs = {'d_i':[20, 30], 'd_w':[1, 5], 'N_t':[9, 17]}
    # constraint_policy =  {   'outerDiamMax': 60,
    #                          'MaximumShearStressMax': 0.7,
    #                         'CoilBindingGapMin': 0.5,
    #                         }
    def Feasibility(self, bounds_inputs):

        self.bound_paras = list(bounds_inputs.keys())
        """
        这里应该也有一个check, 就是有的paramters不能作为bounds_input输入
        即设计参数，设计变量才可以作为bounds_input的输入
        """
        bound_input_accept_policy(bounds_inputs)

        """
        这里还需要check一下，如果一个parameter已经在input parameters里面有fixed的值了，
        那么它就不应该再出现在bound inputs里面，
        """
        #############################################################################
        # 所以如果这一步不报错，那么bounds里面的parameters就不会存在于input parameters里面
        #############################################################################
        existingInputBounds_overlap_paras = [
            item for item in self.bound_paras if item in self.notNone_input_parameters
        ]
        # 如果两者还存在overlap就报错
        if len(existingInputBounds_overlap_paras) > 0:
            raise InputAndBoundsParametersOverlapError(
                existingInputBounds_overlap_paras
            )

        dimension = len(bounds_inputs)

        # Step 1: initial a cube sampler with the bounds first
        sampler = qmc.LatinHypercube(d=dimension)
        sample = sampler.random(n=3000)

        lower_bounds = [item[0] for item in bounds_inputs.values()]
        upper_bounds = [item[1] for item in bounds_inputs.values()]
        feasible_arr = qmc.scale(sample, lower_bounds, upper_bounds)
        # 这个function会save每一步的feasible_arr，并储存，用于UI画图使用
        feasible_arr_steps = []
        for constraint in self.constraint_policy.keys():
            if constraint in (
                "outerDiamMax",
                "outerDiamMin",
                "InnerDiamMax",
                "InnerDiamMin",
            ):
                feasible_arr = constraint_InnerOuterDiamMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint][0],  # if_Outer
                    Constraint_input_dict[constraint][1],  # if_Max
                    self.constraint_policy[constraint],  # DiamThreshold
                )

            elif constraint in ("MaximumShearStressMax", "MaximumShearStressMin"):

                feasible_arr = constraint_MaximumShearStressMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )

            elif constraint in ("CoilBindingGapMax", "CoilBindingGapMin"):

                feasible_arr = constraint_CoilBindingGapMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )
            elif constraint in ("SpringRateMax", "SpringRateMin"):

                feasible_arr = constraint_SpringRateMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )
            elif constraint in ("SpringIndexMax", "SpringIndexMin"):

                feasible_arr = constraint_SpringIndexMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )
            elif constraint in (
                "BucklingSlendernessRatioMax",
                "BucklingSlendernessRatioMin",
            ):

                if self.constraint_policy[constraint][0]:
                    threshold = BucklingSlendernessRatio_threshold(self.Poisson_ratio)
                else:
                    threshold = self.constraint_policy[constraint][1]

                feasible_arr = constraint_BucklingSlendernessRatioMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    threshold,  # Threshold
                )

            elif constraint in ("DiametralExpansionMax", "DiametralExpansionMin"):

                feasible_arr = constraint_DiametralExpansionMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )

            elif constraint in ("StressRelaxationMax", "StressRelaxationMin"):

                feasible_arr = constraint_StressRelaxationMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )

            elif constraint in ("PreloadForceMax", "PreloadForceMin"):

                feasible_arr = constraint_PreloadForceMaxMin(
                    feasible_arr,
                    self.bound_paras,
                    self.notNone_input_parameters,
                    Constraint_input_dict[constraint],  # if max
                    self.constraint_policy[constraint],  # Threshold
                )
            feasible_arr_steps.append([constraint, feasible_arr])
        return feasible_arr, feasible_arr_steps

    # 因为是在给定的bounds上面找最小值，所以这里的输入也是bounds_inputs
    def ConstraintsForOptimize(self, design_value):

        constraints = []
        print(design_value)
        for constraint in self.constraint_policy.keys():
            if constraint in (
                "outerDiamMax",
                "outerDiamMin",
                "InnerDiamMax",
                "InnerDiamMin",
            ):
                constraints.append(
                    optimize_InnerOuterDiamMaxMin(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint][0],  # if_Outer
                        Constraint_input_dict[constraint][1],  # if_Max
                        self.constraint_policy[constraint],  # DiamThreshold
                    )
                )
            elif constraint in ("MaximumShearStressMax", "MaximumShearStressMin"):
                constraints.append(
                    optimize_MaximumShearStress(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
            elif constraint in ("CoilBindingGapMax", "CoilBindingGapMin"):
                constraints.append(
                    optimize_CoilBindingGap(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
            elif constraint in ("SpringRateMax", "SpringRateMin"):
                constraints.append(
                    optimize_SpringRate(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
            elif constraint in ("SpringIndexMax", "SpringIndexMin"):
                constraints.append(
                    optimize_SpringIndex(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
            elif constraint in (
                "BucklingSlendernessRatioMax",
                "BucklingSlendernessRatioMin",
            ):

                if self.constraint_policy[constraint][0]:
                    threshold = BucklingSlendernessRatio_threshold(self.Poisson_ratio)
                else:
                    threshold = self.constraint_policy[constraint][1]
                constraints.append(
                    optimize_BucklingSlendernessRatio(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        threshold,  # Threshold
                        "constraint",
                    )
                )
            elif constraint in ("DiametralExpansionMax", "DiametralExpansionMin"):
                constraints.append(
                    optimize_DiametralExpansion(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
            elif constraint in ("StressRelaxationMax", "StressRelaxationMin"):
                constraints.append(
                    optimize_StressRelaxation(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )

            elif constraint in ("PreloadForceMax", "PreloadForceMin"):
                constraints.append(
                    optimize_PreloadForce(
                        design_value,
                        self.notNone_input_parameters,
                        self.bound_paras,
                        Constraint_input_dict[constraint],  # if_Max
                        self.constraint_policy[constraint],  # Threshold
                        "constraint",
                    )
                )
        target_sum = 0

        for objective_ in self.objective.keys():
            if objective_ == "spring_rate_spring_index":
                #self.objective[objective_]
                #{'MaxorMin':'min', 'k_max': 20, 'c_max':10}
                spring_rate = optimize_SpringRate(
                    design_value,
                    self.notNone_input_parameters,
                    self.bound_paras,
                    True,  # 这个值不用，随便输入一个
                    0,  # 这个值不用，随便输入一个
                    "target",
                )
                sping_index = optimize_SpringIndex(
                    design_value,
                    self.notNone_input_parameters,
                    self.bound_paras,
                    True,  # 这个值不用，随便输入一个
                    0,  # 这个值不用，随便输入一个
                    "target",
                )
                target_sum += spring_rate/self.objective[objective_]['k_max'] + sping_index//self.objective[objective_]['c_max']
            elif objective_ == "spring_rate":
                spring_rate = optimize_SpringRate(
                    design_value,
                    self.notNone_input_parameters,
                    self.bound_paras,
                    True,  # 这个值不用，随便输入一个
                    0,  # 这个值不用，随便输入一个
                    "target",
                )
                target_sum += spring_rate
            elif objective_ == "spring_index":
                spring_index = optimize_SpringIndex(
                    design_value,
                    self.notNone_input_parameters,
                    self.bound_paras,
                    True,  # 这个值不用，随便输入一个
                    0,  # 这个值不用，随便输入一个
                    "target",
                )
                target_sum += spring_index

        for constraint_ in constraints:
            if constraint_ < 0:
                target_sum += self.r * constraint_ * constraint_

        return target_sum
