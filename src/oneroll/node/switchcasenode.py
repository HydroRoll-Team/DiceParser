from typing import List, Optional
from executionnode import ExecutionNode
from validatorlist import ValidatorList
from stringresult import StringResult

class SwitchCaseNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_branchList = []
        self.m_stringResult = StringResult()
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

        diceResult = previousResult if isinstance(previousResult, DiceResult) else None

        finalResultList = []
        if diceResult:
            for die in diceResult.getResultList():
                resultList = []
                for info in self.m_branchList:
                    if self.m_stopAtFirst and resultList:
                        break
                    if info.validatorList:
                        if info.validatorList.hasValid(die, True):
                            lastNode = ParsingToolBox.getLeafNode(info.node)
                            if lastNode and lastNode.getResult():
                                resultList.append(lastNode.getResult().getStringResult())
                    elif not resultList:
                        info.node.run(self.m_previousNode)
                        lastNode = ParsingToolBox.getLeafNode(info.node)
                        if lastNode and lastNode.getResult():
                            resultList.append(lastNode.getResult().getStringResult())
                        else:
                            resultList.append(None)
                finalResultList.append(resultList)
        else:
            scalar = previousResult.getResult(Dice.RESULT_TYPE.SCALAR)
            for info in self.m_branchList:
                if self.m_stopAtFirst and finalResultList:
                    break
                if info.validatorList:
                    die = Die()
                    die.insertRollValue(scalar)
                    if info.validatorList.hasValid(die, True):
                        lastNode = ParsingToolBox.getLeafNode(info.node)
                        if lastNode and lastNode.getResult():
                            finalResultList.append(lastNode.getResult().getStringResult())
                elif not finalResultList:
                    info.node.run(self.m_previousNode)
                    lastNode = ParsingToolBox.getLeafNode(info.node)
                    if lastNode and lastNode.getResult():
                        finalResultList.append(lastNode.getResult().getStringResult())
                    else:
                        finalResultList.append(None)

        for text in finalResultList:
            self.m_stringResult.addText(text)

        if not self.m_stringResult.getText():
            self.m_errors[Dice.ERROR_CODE.NO_VALID_RESULT] = "No value fits the Switch/Case operator"

        if self.m_nextNode:
            self.m_nextNode.run(self)

    def toString(self, withLabel: bool) -> str:
        if withLabel:
            return f"{self.m_id} [label=\"SwitchCaseNode\"]"
        else:
            return self.m_id

    def getPriority(self) -> int:
        priority = 0
        if self.m_previousNode:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self) -> ExecutionNode:
        node = SwitchCaseNode()
        for info in self.m_branchList:
            node.insertCase(info.node, info.validatorList)

        if self.m_nextNode:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def insertCase(self, node: ExecutionNode, validator: ValidatorList):
        info = Dice.CaseInfo(validator, node)
        self.m_branchList.append(info)