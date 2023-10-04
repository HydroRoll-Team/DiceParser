from node.executionnode import ExecutionNode
from result.diceresult import DiceResult

class UniqueNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            self.m_result.setPrevious(previous.getResult())
            tmpResult = previous.getResult()
            if tmpResult is not None:
                dice = tmpResult
                if isinstance(dice, DiceResult):
                    resultList = dice.getResultList()
                    formerValues = []
                    for oldDie in resultList:
                        value = oldDie.getValue()
                        if value not in formerValues:
                            die = Die(oldDie)
                            self.m_diceResult.insertResult(die)
                            formerValues.append(value)
                        oldDie.displayed()
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"UniqueNode Node\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = UniqueNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node