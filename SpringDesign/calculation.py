import math
from scipy import integrate

# 最大剪应力计算公式
def MaximumShearStress_calculation(MaximumShearStress_paradict):
    d_i = MaximumShearStress_paradict["d_i"]  # 内径
    d_w = MaximumShearStress_paradict["d_w"]  # 线径
    N_a = MaximumShearStress_paradict["N_a"]  # 有效线圈数
    G = MaximumShearStress_paradict["G"]  # 剪力模数
    L_free = MaximumShearStress_paradict["L_free"]  # 自由长度
    L_hard = MaximumShearStress_paradict["L_hard"]  # 最小长度

    component1 = G * (L_free - L_hard)
    component2 = 4 * math.pi * N_a

    component3 = d_w * (4 * d_i ** 2 + 9.46 * d_w * d_i + 3 * d_w * d_w)
    component4 = d_i * (d_i + d_w) ** 3

    return component1 * component3 / (component2 * component4)


# 线圈绑定间隙计算公式
def CoilBindingGap_calculation(CoilBindingGap_paradict):
    L_hard = CoilBindingGap_paradict["L_hard"]  # 最小长度
    d_w = CoilBindingGap_paradict["d_w"]  # 线径
    N_t = CoilBindingGap_paradict["N_t"]  # 总线圈数

    return (L_hard - N_t * d_w) / (N_t - 1)


# 弹性比率Spring Rate公式
def SpringRate_calculation(SpringRate_paradict):
    G = SpringRate_paradict["G"]  # 剪力模数
    N_a = SpringRate_paradict["N_a"]  # 有效线圈数
    d_w = SpringRate_paradict["d_w"]  # 线径
    d_i = SpringRate_paradict["d_i"]  # 内径

    return (G * (d_w ** 4)) / (8 * N_a * (d_i + d_w) ** 3)


# 弹簧指数Spring Index公式
def SpringIndex_calculation(SpringIndex_paradict):
    d_w = SpringIndex_paradict["d_w"]  # 线径
    d_i = SpringIndex_paradict["d_i"]  # 内径

    return 1 + d_i / d_w


# Buckling Slenderness Ratio公式： 高径比（细长比） 测量弹簧在压缩下屈曲的敏感性
def BucklingSlendernessRatio_calculation(BucklingSlendernessRatio_paradict):
    L_free = BucklingSlendernessRatio_paradict["L_free"]
    d_i = BucklingSlendernessRatio_paradict["d_i"]
    d_w = BucklingSlendernessRatio_paradict["d_w"]

    return L_free / (d_i + d_w)


# Buckling Slenderness Ratio Threshold： 高径比（细长比）threshold
def BucklingSlendernessRatio_threshold(Poisson_ratio):
    return math.pi * math.sqrt(2 * (2 * Poisson_ratio + 1) / (Poisson_ratio + 2))


# Diametral Expansion 直径膨胀，当弹簧被压缩时候衡量弹簧外径增加多少的量度（仅封闭条件下弹簧的直径膨胀）
def DiametralExpansion_calculation(DiametralExpansion_paradict):
    d_w = DiametralExpansion_paradict["d_w"]
    d_i = DiametralExpansion_paradict["d_i"]
    L_free = DiametralExpansion_paradict["L_free"]
    N_a = DiametralExpansion_paradict["N_a"]
    pitch = SpringPitch_formula(True, L_free, d_w, N_a)  # 仅封闭条件下弹簧的直径膨胀

    return d_w + math.sqrt((d_i + d_w) ** 2 + (pitch ** 2 - d_w) / (math.pi) ** 2)


# Spring Pitch，弹簧间距计算公式
def SpringPitch_formula(if_closed, L_free, d_w, N_a):
    if if_closed:
        return (L_free - 3 * d_w) / N_a
    else:
        return L_free / (N_a - 1)


# Stress Relaxation 应力松弛： 应力松弛是测量弹簧力在高温且时间t的恒定压缩的条件下的衰减程度
def StressRelaxation_calculation(StressRelaxation_paradict):
    d_w = StressRelaxation_paradict["d_w"]
    d_i = StressRelaxation_paradict["d_i"]
    N_a = StressRelaxation_paradict["N_a"]
    deflection = StressRelaxation_paradict["deflection"]
    Gsr = StressRelaxation_paradict["Gsr"]
    time_stress_Relaxation = StressRelaxation_paradict["time_stress_Relaxation"]
    NB_c = StressRelaxation_paradict["NB_c"]
    NB_k = StressRelaxation_paradict["NB_k"]
    NB_n = StressRelaxation_paradict["NB_n"]

    theta_component_1 = (d_i + d_w) ** 2
    theta = (2 * deflection) / (math.pi * N_a * theta_component_1)

    component_1 = 4 / (Gsr * theta * d_w ** 4)
    component_2 = (NB_c / NB_k) * Gsr * NB_n * (time_stress_Relaxation ** NB_k)

    def integrate_com(x):
        return (x ** 2) * ((Gsr * theta * x) ** (-NB_n) + component_2) ** (-1 / NB_n)

    integrate_value = integrate.quad(lambda x: integrate_com(x), 0, d_w)[0]

    return component_1 * integrate_value


# 预紧力 Preload Force, 预紧力是弹簧处于打开位置时施加到弹簧上的力（不使用开关时施加在弹簧上的力）
def PreloadForce_calculation(PreloadForce_paradict):
    L_free = PreloadForce_paradict["L_free"]
    L_solid = PreloadForce_paradict["L_solid"]
    G = PreloadForce_paradict["G"]
    N_a = PreloadForce_paradict["N_a"]
    d_w = PreloadForce_paradict["d_w"]
    d_i = PreloadForce_paradict["d_i"]

    return (L_free - L_solid) * G * d_w ** 4 / (8 * N_a * (d_i + d_w) ** 3)
