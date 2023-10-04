from typing import List, Optional
from executionnode import ExecutionNode
from validatorlist import ValidatorList
from diceresult import DiceResult

class ReplaceValueNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_branchList = []
        self.m_diceResult = DiceResult()
        self.m_stopAtFirst = False

    def setStopAtFirst(self, b: bool):
        self.m_stopAtFirst = b

    def run(self, previous: Optional[ExecutionNode] = None):
        self.m_previousNode = previous
        if previous is None:
            self.m_errors[Dice.ERROR_CODE.NO_PREVIOUS_ERROR] = "No previous node before Switch/Case operator"
            return
        previousResult = previous.getResult()
        self.m_result.setPrevious(previousResult)

        if previousResult is None or (not previousResult.hasResultOfType(Dice.RESULT_TYPE.SCALAR) and not previousResult.hasResultOfType(Dice.RESULT_TYPE.DICE_LIST)):
            self.m_errors[Dice.ERROR_CODE.NO_VALID_RESULT] = "No scalar or dice result before Switch/Case operator"
            return

        dieList = []
        if previousResult.hasResultOfType(Dice.RESULT_TYPE.DICE_LIST):
            diceResult = previousResult
            dieList.extend(diceResult.getResultList())

        for die in dieList:
            resultList = []
            for info in self.m_branchList:
                if info.validatorList:
                    res = info.validatorList.hasValid(die, False)
                    if not res:
                        continue
                elif resultList:
                    break

                replaceValresult = info.node.getResult()
                if replaceValresult:
                    die.replaceLastValue(replaceValresult.getResult(Dice.RESULT_TYPE.SCALAR).toInt())
                break
            self.m_diceResult.insertResult(die)

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, withLabel: bool) -> str:
        if withLabel:
            return f"{self.m_id} [label=\"ReplaceValueNode\"]"
        else:
            return self.m_id

    def getPriority(self) -> int:
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self) -> ExecutionNode:
        node = ReplaceValueNode()
        for info in self.m_branchList:
            node.insertCase(info.node, info.validatorList)

        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def insertCase(self, node: ExecutionNode, validator: ValidatorList):
        info = Dice.CaseInfo(validator, node)
        self.m_branchList.append(info)