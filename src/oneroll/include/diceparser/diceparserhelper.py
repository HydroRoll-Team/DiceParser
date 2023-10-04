from enum import Enum

class Dice:
    class CONDITION_STATE(Enum):
        ERROR_STATE = 0
        ALWAYSTRUE = 1
        UNREACHABLE = 2
        REACHABLE = 3

    class ERROR_CODE(Enum):
        NO_DICE_ERROR = 0
        DIE_RESULT_EXPECTED = 1
        BAD_SYNTAXE = 2
        ENDLESS_LOOP_ERROR = 3
        DIVIDE_BY_ZERO = 4
        NOTHING_UNDERSTOOD = 5
        NO_DICE_TO_ROLL = 6
        TOO_MANY_DICE = 7
        NO_VARIBALE = 8
        INVALID_INDEX = 9
        UNEXPECTED_CHARACTER = 10
        NO_PREVIOUS_ERROR = 11
        NO_VALID_RESULT = 12
        SCALAR_RESULT_EXPECTED = 13

    class RESULT_TYPE(Enum):
        NONE = 0
        SCALAR = 1
        STRING = 2
        DICE_LIST = 4

    class ConditionType(Enum):
        OnEach = 0
        OnEachValue = 1
        OneOfThem = 2
        AllOfThem = 3
        OnScalar = 4

    class CompareOperator(Enum):
        Equal = 0
        GreaterThan = 1
        LesserThan = 2
        GreaterOrEqual = 3
        LesserOrEqual = 4
        Different = 5

    class ArithmeticOperator(Enum):
        # Add your arithmetic operators here
        pass
