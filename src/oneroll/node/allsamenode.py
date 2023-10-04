from .executionnode import ExecutionNode
from ..result.diceresult import DiceResult, Die

class AllSameNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            previous_result = previous.getResult()
            if isinstance(previous_result, DiceResult):
                self.m_result.setPrevious(previous_result)
                allSame = True
                i = 0
                previousValue = 0
                if len(previous_result.getResultList()) < 2:
                    self.m_errors[Dice.ERROR_CODE.ENDLESS_LOOP_ERROR] = "T operator must operate on more than 1 die"
                    return
                for die in previous_result.getResultList():
                    if i == 0:
                        previousValue = die.getValue()
                    tmpdie = Die(die)  # Assuming Die class exists
                    self.m_diceResult.insertResult(tmpdie)
                    die.displayed()
                    if previousValue != die.getValue():
                        allSame = False
                    i += 1

                while allSame:
                    list = self.m_diceResult.getResultList()
                    pValue = 0
                    i = 0
                    for die in list:
                        die.roll(True)
                        if i == 0:
                            pValue = die.getValue()
                        if pValue != die.getValue():
                            allSame = False
                        i += 1
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"AllSameNode\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        return AllSameNode()
