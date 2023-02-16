class Error(Exception):
    def __init__(self, input_str):
        print(input_str)


class NonexistParameterInInput(Error):
    def __init__(self, input_str):
        print("there is no parameters named: [" + input_str + "]")


class ConstraintPolicyError(Error):
    def __init__(self, input_str):
        print("there is ConstraintPolicyError: [" + input_str + "]")


class UniqueConstraintPolicyError(Error):
    def __init__(self):
        print("each ConstraintPolicy can only exist once")


class OptimizeTargetInitialError(Error):
    def __init__(self, input_str):
        print(input_str)


class InputParametersLogicError(Error):
    def __init__(self, input_str):
        print("there is logic error from input parameters: [" + input_str + "]")


class InputParametersTypeError(Error):
    def __init__(self, input_parameter_name, type_):
        print(
            "the input parameters: ["
            + input_parameter_name
            + "] should in ["
            + type_
            + "]"
        )


class ParametersRangeError(Error):
    def __init__(self, input_parameter_name, input_str):
        print(
            "the input parameters: ["
            + input_parameter_name
            + "] should be ["
            + input_str
            + "]"
        )


class DesignBoundsInputError(Error):
    def __init__(self, input_str):
        print(input_str)


class InputAndBoundsParametersOverlapError(Error):
    def __init__(self, overlap_list):
        print(
            ", ".join(overlap_list)
            + " should not appears as both input parameters and bounds parameters"
        )


class ConstraintMissingParas(Error):
    def __init__(self, constraint_name):
        print("missing parameters in: " + constraint_name)


class ConstraintFailed(Error):
    def __init__(self, input_str):
        print(input_str)
