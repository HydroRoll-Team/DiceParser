from .explodedicenode import ExecutionNode
from ..result.scalarresult import ScalarResult
from ..result.diceresult import DiceResult
from ..include.diceparser.diceparserhelper import Dice

class CountExecuteNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_scalarResult = ScalarResult()
        self.m_validatorList = None

    def setValidatorList(self, validatorlist):
        self.m_validatorList = validatorlist

    def run(self, previous):
        self.m_previousNode = previous
        if previous is None:
            self.m_errors[Dice.ERROR_CODE.NO_PREVIOUS_ERROR] = "No scalar result before Swith/Case operator"
            return
        previousResult = previous.getResult()
        if isinstance(previousResult, DiceResult):
            self.m_result.setPrevious(previousResult)
            sum = 0
            def f(die, score): 
                nonlocal sum
                sum += score
            self.m_validatorList.validResult(previousResult, True, True, f)
            self.m_scalarResult.setValue(sum)
            if self.m_nextNode is not None:
                self.m_nextNode.run(self)

    def toString(self, withlabel):
        if withlabel:
            return f"{self.m_id} [label=\"CountExecuteNode {self.m_validatorList}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self):
        node = CountExecuteNode()
        if self.m_validatorList is not None:
            node.setValidatorList(self.m_validatorList.getCopy())
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node