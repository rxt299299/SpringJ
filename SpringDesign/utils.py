from .constant import *
from .errors import *

# initializes the parameters
# and check if the input type is correct, if not, raise error: InputParametersTypeError
def parameter_initial(parameter_name, type_category, inputs):

    if parameter_name in inputs.keys():
        res = inputs[parameter_name]
        if type_category == "bool" and isinstance(res, bool):
            return res
        if type_category == "int" and isinstance(res, int):
            return res
        if type_category == "int_or_float" and (
            isinstance(res, int) or isinstance(res, float)
        ):
            return res
        else:
            raise InputParametersTypeError(parameter_name, type_category)
    elif parameter_name == "r":
        return 50
    else:
        return None


# initializes the parameters
def parameter_initial_constraint(parameter_name, inputs):
    if parameter_name in inputs.keys():
        return inputs[parameter_name]
    else:
        return None


# check if there is nonexisted parameters in the input dictionary
def nonexist_parameters(parameter_names_list, inputs):
    nonexist_list = []
    for item in inputs.keys():
        if item not in parameter_names_list:
            nonexist_list.append(item)

    if len(nonexist_list) > 0:
        raise NonexistParameterInInput(" ".join(nonexist_list))
    pass


# used in parameters_range_check, to check is a parameter value is above 0
def range_check_above_zero(input_para_name, para_value):
    if para_value > 0:
        pass
    else:
        raise ParametersRangeError(input_para_name, "should be above 0")


# 写一个函数，input是MaximumShearStress_calculation（也可以用在别的地方）
# 需要的变量，已知的input_paras的名字List, 已知的bound_paras的名字List
# 需要返回每个变量对应的地方
# 因为InputAndBoundsParametersOverlapError, 所以这里的input_paras和bound_paras是没有overlap的
def match_constraintInput_fromInputBoundParameters(
    constraintInput, input_paras, bound_paras, notNone_input_parameters
):

    res = {}
    for parameter in constraintInput:
        if parameter in input_paras:
            res[parameter] = ("input", notNone_input_parameters[parameter])
        elif parameter in bound_paras:
            res[parameter] = ("bound", bound_paras.index(parameter))

    return res


# check有的paramters不能作为bounds_input输入
def bound_input_accept_policy(bounds_inputs):
    # 不能有除了这些之外的参数作为bounds输入
    wrong_bounds_parameter_list = []
    for item in bounds_inputs.keys():
        if item not in design_measurement_parameters:
            wrong_bounds_parameter_list.append(item)

    if len(wrong_bounds_parameter_list) > 0:
        error_msg = (
            ", ".join(wrong_bounds_parameter_list)
            + " should not appears in bounds(design) parameter inputs"
        )
        raise DesignBoundsInputError(error_msg)

    # 有的参数不能一起作为bounds比如不能同时N_t和N_a, 不能同时d_i,d_w,d_o
    if "N_t" in bounds_inputs.keys() and "N_a" in bounds_inputs.keys():
        raise DesignBoundsInputError("N_t and N_a cannot both exist in bounds_input")

    if (
        "d_i" in bounds_inputs.keys()
        and "d_o" in bounds_inputs.keys()
        and "d_w" in bounds_inputs.keys()
    ):
        raise DesignBoundsInputError(
            "d_i, d_o and d_w cannot both exist in bounds_input"
        )
