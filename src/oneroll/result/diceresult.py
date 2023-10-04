from typing import List
from enum import Enum
from .result import Result

class DiceResultType(Enum):
    SCALAR = 0
    DICE_LIST = 1


class ArithmeticOperator(Enum):
    PLUS = "+"
    MULTIPLICATION = "*"
    MINUS = "-"
    POW = "^"
    DIVIDE = "/"
    INTEGER_DIVIDE = "//"


class Die:
    def __init__(self, value):
        self.value = value

class DiceResult(Result):
    def __init__(self):
        super().__init__()
        self.result_types = {DiceResultType.DICE_LIST, DiceResultType.SCALAR}
        self.dice_values = []
        self.homogeneous = True
        self.operator = ArithmeticOperator.PLUS

    def insert_result(self, die: Die):
        self.dice_values.append(die)

    def get_result_list(self) -> List[Die]:
        return self.dice_values

    def is_homogeneous(self) -> bool:
        return self.homogeneous

    def set_homogeneous(self, homogeneous: bool):
        self.homogeneous = homogeneous

    def set_result_list(self, dice_values: List[Die]):
        self.dice_values = dice_values

    def get_result(self, result_type: DiceResultType):
        if result_type == DiceResultType.SCALAR:
            return self.get_scalar_result()
        elif result_type == DiceResultType.DICE_LIST:
            return self.dice_values
        else:
            return None

    def contains(self, die: Die, equal_func):
        for value in self.dice_values:
            if equal_func(value, die):
                return True
        return False

    def get_scalar_result(self):
        if len(self.dice_values) == 1:
            return self.dice_values[0].value
        else:
            scalar = 0
            i = 0
            for tmp in self.dice_values:
                if i > 0:
                    if self.operator == ArithmeticOperator.PLUS:
                        scalar += tmp.value
                    elif self.operator == ArithmeticOperator.MULTIPLICATION:
                        scalar *= tmp.value
                    elif self.operator == ArithmeticOperator.MINUS:
                        scalar -= tmp.value
                    elif self.operator == ArithmeticOperator.POW:
                        scalar = int(pow(float(scalar), float(tmp.value)))
                    elif self.operator == ArithmeticOperator.DIVIDE or self.operator == ArithmeticOperator.INTEGER_DIVIDE:
                        if tmp.value != 0:
                            scalar /= tmp.value
                        else:
                            # @todo Error cant divide by 0. Must be displayed.
                            pass
                else:
                    scalar = tmp.value
                i += 1
            return scalar

    def clear(self):
        self.dice_values.clear()

    def set_operator(self, operator: ArithmeticOperator):
        self.operator = operator

    def to_string(self, wl: bool):
        scalar_sum = [str(die.value) for die in self.dice_values]
        if wl:
            return f"DiceResult Value {self.get_scalar_result()} dice {'_'.join(scalar_sum)}"
        else:
            return str(self)

    def get_copy(self):
        copy = DiceResult()
        copy.set_homogeneous(self.homogeneous)
        copy.set_operator(self.operator)
        copy.result_types = self.result_types.copy()
        copy.dice_values = [Die(die.value) for die in self.dice_values]
        copy.setPrevious(self.getPrevious())
        return copy