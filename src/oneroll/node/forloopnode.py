from .explodedicenode import ExecutionNode
from ..result.diceresult import DiceResult

class MockNode(ExecutionNode):
    def __init__(self):
        super().__init__()

    def run(self, node):
        pass

    def set_result(self, result):
        self.result = result

    def to_string(self, with_label):
        return ""

    def get_priority(self):
        return 0

    def get_copy(self):
        return MockNode()


class ForLoopNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.internal = None
        self.dice_result = DiceResult()

    def set_internal(self, internal):
        self.internal = internal

    def run(self, previous):
        if previous is not None:
            prev_result = isinstance(previous.get_result(), DiceResult)
            if prev_result:
                self.dice_result.set_previous(prev_result)
                dice_list = prev_result.get_result_list()
                for dice in dice_list:
                    node = MockNode()
                    dice_result = DiceResult()
                    dice_result.insert_result(dice)
                    node.set_result(dice_result)
                    self.internal.run(node)

                    tmp = self.internal
                    while tmp.get_next_node() is not None:
                        tmp = tmp.get_next_node()
                    internal_result = tmp.get_result()
                    value = internal_result.get_result(Dice.RESULT_TYPE.SCALAR)

                    neodie = Die()
                    neodie.copy(dice)
                    neodie.set_value(value)
                    self.dice_result.insert_result(neodie)
                    node.set_result(None)
                    dice_result.clear()
                    dice.displayed()

        self.result = self.dice_result
        if self.next_node is not None:
            self.next_node.run(self)

    def get_priority(self):
        return 2

    def to_string(self, with_label):
        if with_label:
            return f"{self.id} [label=\"ForLoopNode Node\"]"
        else:
            return self.id

    def get_copy(self):
        node = ForLoopNode()
        if self.internal is not None:
            node.set_internal(self.internal.get_copy())
        return node
