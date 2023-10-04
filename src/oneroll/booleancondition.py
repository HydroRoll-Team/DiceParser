from enum import Enum
from typing import Tuple

class CONDITION_STATE(Enum):
    UNREACHABLE = 0
    ALWAYSTRUE = 1
    REACHABLE = 2

class CompareOperator(Enum):
    Equal = 0
    GreaterThan = 1
    LesserThan = 2
    GreaterOrEqual = 3
    LesserOrEqual = 4
    Different = 5

class ExecutionNode:
    def __init__(self):
        self.result = None

    def run(self, context):
        # Run the execution node logic and set the result
        pass

    def get_result(self):
        return self.result

class BooleanCondition:
    def __init__(self):
        self.operator = CompareOperator.Equal
        self.value = None

    def test_equal(self, inside_range: bool, range: Tuple[int, int]) -> CONDITION_STATE:
        if not inside_range:
            return CONDITION_STATE.UNREACHABLE
        elif inside_range and (range[0] == range[1]):
            return CONDITION_STATE.UNREACHABLE
        elif value < min(range[0], range[1]):
            return CONDITION_STATE.ALWAYSTRUE
        else:
            return CONDITION_STATE.REACHABLE

    def test_different(self, inside: bool, range: Tuple[int, int]) -> CONDITION_STATE:
        if not inside:
            return CONDITION_STATE.UNREACHABLE
        elif inside and (range[0] == range[1]):
            return CONDITION_STATE.UNREACHABLE
        elif value > max(range[0], range[1]):
            return CONDITION_STATE.UNREACHABLE
        elif value <= min(range[0], range[1]):
            return CONDITION_STATE.ALWAYSTRUE
        else:
            return CONDITION_STATE.REACHABLE

    def has_valid(self, b, recursive, unhighlight) -> int:
        list_values = []
        if self.condition_type == OnEachValue:
            list_values.append(b.get_value())
        elif recursive:
            list_values = b.get_list_value()
        else:
            list_values.append(b.get_last_rolled_value())

        sum = 0
        value_scalar = self.value_to_scalar()
        for value in list_values:
            if self.operator == CompareOperator.Equal:
                sum += 1 if value == value_scalar else 0
            elif self.operator == CompareOperator.GreaterThan:
                sum += 1 if value > value_scalar else 0
            elif self.operator == CompareOperator.LesserThan:
                sum += 1 if value < value_scalar else 0
            elif self.operator == CompareOperator.GreaterOrEqual:
                sum += 1 if value >= value_scalar else 0
            elif self.operator == CompareOperator.LesserOrEqual:
                sum += 1 if value <= value_scalar else 0
            elif self.operator == CompareOperator.Different:
                sum += 1 if value != value_scalar else 0

        if unhighlight and sum == 0:
            b.set_highlighted(False)
        else:
            b.set_highlighted(True)

        return sum

    def set_operator(self, operator):
        self.operator = operator

    def set_value_node(self, value_node):
        self.value = value_node

    def to_string(self):
        str = ""
        if self.operator == CompareOperator.Equal:
            str += "="
        elif self.operator == CompareOperator.GreaterThan:
            str += ">"
        elif self.operator == CompareOperator.LesserThan:
            str += "<"
        elif self.operator == CompareOperator.GreaterOrEqual:
            str += ">="
        elif self.operator == CompareOperator.LesserOrEqual:
            str += "<="
        elif self.operator == CompareOperator.Different:
            str += "!="
        return "[{}{}]".format(str, self.value_to_scalar())

    def is_valid_range_size(self, range: Tuple[int, int]) -> CONDITION_STATE:
        value_scalar = self.value_to_scalar()
        bound_value = min(max(range[0], value_scalar), range[1])
        is_inside_range = bound_value == value_scalar

        if self.operator == CompareOperator.Equal:
            return self.test_equal(is_inside_range, range)
        elif self.operator == CompareOperator.GreaterThan:
            return self.test_greater_than(value_scalar, range)
        elif self.operator == CompareOperator.LesserThan:
            return self.test_lesser_than(value_scalar, range)
        elif self.operator == CompareOperator.GreaterOrEqual:
            return self.test_greater_or_equal(value_scalar, range)
        elif self.operator == CompareOperator.LesserOrEqual:
            return self.test_lesser_or_equal(value_scalar, range)
        elif self.operator == CompareOperator.Different:
            return self.test_different(is_inside_range, range)

    def get_copy(self):
        val = BooleanCondition()
        val.set_operator(self.operator)
        val.set_value_node(self.value.get_copy())
        return val

    def value_to_scalar(self):
        if self.value is None:
            return 0

        self.value.run(None)
        result = self.value.get_result()
        if result:
            return int(result.get_result(Dice.RESULT_TYPE.SCALAR))
        else:
            return 0
