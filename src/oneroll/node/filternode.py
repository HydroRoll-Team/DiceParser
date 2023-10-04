from .explodedicenode import ExecutionNode
from ..result.diceresult import DiceResult

class ValidatorList:
    def __init__(self):
        pass

class FilterNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_validatorList = None
        self.m_eachValue = False

    def setValidatorList(self, validatorList):
        self.m_validatorList = validatorList

    def run(self, previous):
        self.m_previousNode = previous
        if previous is None:
            return

        previousDiceResult = previous.getResult()
        self.m_result.setPrevious(previousDiceResult)

        if isinstance(previousDiceResult, DiceResult):
            diceList2 = []
            def f(die, index):
                if die is None:
                    return
                tmpdie = Die(die)
                diceList2.append(tmpdie)
                die.displayed()

            self.m_validatorList.validResult(previousDiceResult, True, True, f)

            diceList = previousDiceResult.getResultList()
            diceList = [die for die in diceList if die not in diceList2]
            for tmp in diceList:
                tmp.setHighlighted(False)
                tmp.setDisplayed(True)

            self.m_diceResult.setResultList(diceList2)

            if self.m_nextNode is not None:
                self.m_nextNode.run(self)

    def toString(self, withLabel):
        if withLabel:
            return "{} [label=\"FilterNode\"]".format(self.m_id)
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = FilterNode()
        if self.m_validatorList is not None:
            node.setValidatorList(self.m_validatorList.getCopy())
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node