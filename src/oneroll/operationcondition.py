from booleancondition import BooleanCondition
from node.executionnode import ExecutionNode
from validator import Validator
from typing import List, Tuple, Set

class OperationCondition(Validator):
    def __init__(self):
        super().__init__()
        self.m_operator = Dice.ConditionOperator.Modulo
        self.m_boolean = None
        self.m_value = None

    def set_operator(self, m):
        self.m_operator = m

    def set_value_node(self, node):
        self.m_value = node

    def to_string(self):
        str_ = ""
        if self.m_operator == Dice.ConditionOperator.Modulo:
            str_ += "\\%"
        return f"[{str_}{self.value_to_scalar()}{self.m_boolean.to_string()}]"

    def is_valid_range_size(self, range: Tuple[int, int]):
        valid = Dice.ConditionState.REACHABLE
        range_is_close = (range[0] == range[1])
        die = Die()
        die.insert_roll_value(range[0])

        if self.m_boolean is None:
            return Dice.ConditionState.ERROR_STATE

        if range_is_close and self.m_boolean.has_valid(die, False, False):
            valid = Dice.ConditionState.ALWAYSTRUE
        elif range_is_close and not self.m_boolean.has_valid(die, False, False):
            valid = Dice.ConditionState.UNREACHABLE

        return valid

    def get_copy(self):
        val = OperationCondition()
        val.set_operator(self.m_operator)
        val.set_value_node(self.m_value.get_copy())
        boolean = self.m_boolean.get_copy()
        val.set_boolean(boolean)
        return val

    def value_to_scalar(self):
        if self.m_value is None:
            return 0

        self.m_value.run(None)
        result = self.m_value.get_result()
        return int(result.get_result(Dice.ResultType.SCALAR))

    def get_possible_values(self, range: Tuple[int, int]):
        if self.m_boolean is None:
            return self.m_values

        for i in range(min(range[0], range[1]), max(range[0], range[1]) + 1):
            value_scalar = self.value_to_scalar()
            val = i % value_scalar
            die = Die()
            die.insert_roll_value(val)
            if self.m_boolean.has_valid(die, False, False):
                self.m_values.add(i)
        return self.m_values