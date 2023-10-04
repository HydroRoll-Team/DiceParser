valueslistnode.py:

from executionnode import ExecutionNode
from result.diceresult import DiceResult

class ValuesListNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_data = []
        self.m_diceResult = DiceResult()

    def run(self, previous=None):
        self.m_previousNode = previous
        for node in self.m_data:
            node.run(self)
            result = node.getResult()
            if not result:
                continue
            val = result.getResult(Dice.RESULT_TYPE.SCALAR).toInt()
            die = Die()
            dyna = isinstance(node, VariableNode)
            if dyna is not None:
                dyna.setDisplayed()
            die.insertRollValue(val)
            self.m_diceResult.insertResult(die)

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def insertValue(self, value):
        self.m_data.append(value)

    def getCopy(self):
        node = ValuesListNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def toString(self, wl):
        if wl:
            return f"{self.m_id} [label=\"ValuesListNode list:\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 4
        return priority