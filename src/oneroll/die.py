import random, uuid
from enum import Enum

class ArithmeticOperator(Enum):
    PLUS = "+"
    MULTIPLICATION = "*"
    MINUS = "-"
    INTEGER_DIVIDE = "//"
    DIVIDE = "/"
    POW = "**"

class Die:
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.value = 0
        self.roll_result = []
        self.selected = False
        self.has_value = False
        self.display_status = False
        self.highlighted = True
        self.max_value = 0
        self.base = 0
        self.color = ""
        self.op = ArithmeticOperator.PLUS

    @staticmethod
    def build_seed():
        random.seed()

    def roll(self, adding=False):
        if self.max_value != 0:
            value = random.randint(self.base, self.max_value)
            if adding or not self.roll_result:
                self.roll_result.append(value)
            else:
                self.roll_result[-1] = value

    def set_selected(self, selected):
        self.selected = selected

    def get_value(self):
        if self.has_value:
            return self.value
        else:
            value = 0
            for i, tmp in enumerate(self.roll_result):
                if i > 0:
                    if self.op == ArithmeticOperator.PLUS:
                        value += tmp
                    elif self.op == ArithmeticOperator.MULTIPLICATION:
                        value *= tmp
                    elif self.op == ArithmeticOperator.MINUS:
                        value -= tmp
                    elif self.op == ArithmeticOperator.INTEGER_DIVIDE or self.op == ArithmeticOperator.DIVIDE:
                        if tmp != 0:
                            value //= tmp
                        else:
                            # error()
                            pass
                    elif self.op == ArithmeticOperator.POW:
                        value = value ** tmp
                else:
                    value = tmp
            return value

    def get_base(self):
        return self.base

    def set_base(self, base):
        self.base = base

    def get_max_value(self):
        return self.max_value

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_uuid(self):
        return self.uuid

    def set_uuid(self, uuid):
        self.uuid = uuid

    def is_highlighted(self):
        return self.highlighted

    def set_highlighted(self, highlighted):
        self.highlighted = highlighted

    def has_been_displayed(self):
        return self.display_status

    def displayed(self):
        self.set_displayed(True)

    def set_displayed(self, display_status):
        self.display_status = display_status

    def has_children_value(self):
        return len(self.roll_result) > 1

    def insert_roll_value(self, value):
        self.roll_result.append(value)

    def replace_last_value(self, value):
        self.roll_result[-1] = value

    def get_list_value(self):
        return self.roll_result

    def get_last_rolled_value(self):
        if self.roll_result:
            return self.roll_result[-1]
        else:
            return 0

    def set_op(self, op):
        self.op = op

    def get_op(self):
        return self.op

    def set_value(self, value):
        self.value = value
        self.has_value = True

    def is_selected(self):
        return self.selected