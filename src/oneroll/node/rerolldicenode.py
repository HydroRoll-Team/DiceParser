rerolldicenode.py:

from executionnode import ExecutionNode
from result.diceresult import DiceResult
from validatorlist import ValidatorList

class RerollDiceNode(ExecutionNode):
    class ReRollMode(Enum):
        EQUAL = 0
        LESSER = 1
        GREATER = 2

    def __init__(self, reroll, addingMode):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_validatorList = None
        self.m_instruction = None
        self.m_reroll = reroll
        self.m_adding = addingMode
        self.m_result = self.m_diceResult

    def __del__(self):
        if self.m_validatorList is not None:
            del self.m_validatorList
            self.m_validatorList = None

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None and previous.getResult() is not None:
            previous_result = previous.getResult()
            if isinstance(previous_result, DiceResult):
                self.m_result.setPrevious(previous_result)
                for die in previous_result.getResultList():
                    tmpdie = Die(die)
                    self.m_diceResult.insertResult(tmpdie)
                    die.displayed()
                list = self.m_diceResult.getResultList()
                toRemove = []
                for die in list:
                    finished = False
                    state = self.m_validatorList.isValidRangeSize((die.getBase(), die.getMaxValue()))
                    if (state == Dice.CONDITION_STATE.ALWAYSTRUE and self.m_adding) or (not self.m_reroll and not self.m_adding and state == Dice.CONDITION_STATE.UNREACHABLE):
                        self.m_errors[Dice.ERROR_CODE.ENDLESS_LOOP_ERROR] = f"Condition ({self.toString(True)}) cause an endless loop with this dice: d[{int(die.getBase())},{int(die.getMaxValue())}]"
                        continue
                    while self.m_validatorList.hasValid(die, False) and not finished:
                        if self.m_instruction is not None:
                            self.m_instruction.run(self)
                            lastNode = ParsingToolBox.getLeafNode(self.m_instruction)
                            if lastNode is not None:
                                lastResult = lastNode.getResult()
                                if isinstance(lastResult, DiceResult):
                                    toRemove.append(die)
                                    list.extend(lastResult.getResultList())
                                    lastResult.clear()
                        else:
                            die.roll(self.m_adding)
                        if self.m_reroll:
                            finished = True
                for die in toRemove:
                    list.remove(die)
                if self.m_nextNode is not None:
                    self.m_nextNode.run(self)
            else:
                self.m_errors[Dice.ERROR_CODE.DIE_RESULT_EXPECTED] = "The a operator expects dice result. Please check the documentation and fix your command."

    def setValidatorList(self, val):
        self.m_validatorList = val

    def toString(self, wl):
        if wl:
            return f"{self.m_id} [label=\"RerollDiceNode validatior: {self.m_validatorList.toString()}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = RerollDiceNode(self.m_reroll, self.m_adding)
        node.setValidatorList(self.m_validatorList)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def getInstruction(self):
        return self.m_instruction

    def setInstruction(self, instruction):
        self.m_instruction = instruction