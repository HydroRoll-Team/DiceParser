from typing import Union, Optional
from oneroll.node.explodedicenode import ExecutionNode
from oneroll.result.diceresult import DiceResult
from validatelist import ValidatorList

class ExplodeDiceNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_validatorList = None
        self.m_limit = None

    def run(self, previous: Optional[ExecutionNode] = None):
        self.m_previousNode = previous
        if not previous:
            return

        if not previous.getResult():
            return

        previous_result = previous.getResult()
        if not isinstance(previous_result, DiceResult):
            return

        self.m_result.setPrevious(previous_result)

        for die in previous_result.getResultList():
            tmpdie = Die(die)  # Assuming a Die class exists
            self.m_diceResult.insertResult(tmpdie)
            die.displayed()

        limit = -1
        if self.m_limit:
            self.m_limit.run(self)
            limitNode = ParsingToolBox.getLeafNode(self.m_limit)
            result = limitNode.getResult()
            if result.hasResultOfType(Dice.RESULT_TYPE.SCALAR):
                limit = int(result.getResult(Dice.RESULT_TYPE.SCALAR))

        hasExploded = False

        def f(die, value):
            nonlocal hasExploded
            nonlocal limit
            static_hash = {}
            if Dice.CONDITION_STATE.ALWAYSTRUE == self.m_validatorList.isValidRangeSize((die.getBase(), die.getMaxValue())):
                self.m_errors[Dice.ERROR_CODE.ENDLESS_LOOP_ERROR] = f"Condition ({self.toString(True)}) cause an endless loop with this dice: d[{int(die.getBase())},{int(die.getMaxValue())}]"
            hasExploded = True
            if limit >= 0:
                if die in static_hash:
                    d = static_hash[die]
                    if d == limit:
                        hasExploded = False
                        return
                    d += 1
            die.roll(True)

        while True:
            hasExploded = False
            self.m_validatorList.validResult(self.m_diceResult, False, False, f)
            if not hasExploded:
                break

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def setValidatorList(self, val: ValidatorList):
        self.m_validatorList = val

    def toString(self, with_label: bool) -> str:
        if with_label:
            return f"{self.m_id} [label=\"ExplodeDiceNode {self.m_validatorList.toString()}\"]"
        else:
            return self.m_id

    def getPriority(self) -> int:
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self) -> ExecutionNode:
        node = ExplodeDiceNode()
        if self.m_validatorList is not None:
            node.setValidatorList(self.m_validatorList.getCopy())
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def setLimitNode(self, limitNode: ExecutionNode):
        self.m_limit = limitNode