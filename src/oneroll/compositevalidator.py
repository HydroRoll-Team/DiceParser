from typing import List, Tuple

class CompositeValidator:
    class LogicOperation:
        OR = 0
        EXCLUSIVE_OR = 1
        AND = 2
        NONE = 3

    def __init__(self):
        self.m_operators = []
        self.m_validatorList = []

    def hasValid(self, b: Die, recursive: bool, unhighlight: bool) -> int:
        i = 0
        sum = 0
        highLight = False
        for validator in self.m_validatorList:
            val = validator.hasValid(b, recursive, unhighlight)
            if i == 0:
                sum = val
                if b.isHighlighted():
                    highLight = b.isHighlighted()
            else:
                if self.m_operators[i - 1] == self.LogicOperation.OR:
                    sum |= val
                    if highLight:
                        b.setHighlighted(highLight)
                elif self.m_operators[i - 1] == self.LogicOperation.EXCLUSIVE_OR:
                    sum ^= val
                elif self.m_operators[i - 1] == self.LogicOperation.AND:
                    sum &= val
            i += 1
        return sum

    def toString(self) -> str:
        validatorsTextList = [validator.toString() for validator in self.m_validatorList]
        operatorTextList = []
        for operator in self.m_operators:
            if operator == self.LogicOperation.OR:
                operatorTextList.append("|")
            elif operator == self.LogicOperation.EXCLUSIVE_OR:
                operatorTextList.append("^")
            elif operator == self.LogicOperation.AND:
                operatorTextList.append("&")
            elif operator == self.LogicOperation.NONE:
                operatorTextList.append("")
        if len(validatorsTextList) - 1 != len(operatorTextList):
            return "Error - operator and validator count don't fit"
        result = []
        for i in range(len(validatorsTextList)):
            result.append(validatorsTextList[i])
            result.append(operatorTextList[i])
        return " ".join(result)

    def isValidRangeSize(self, range: Tuple[int, int]) -> int:
        vec = [validator.isValidRangeSize(range) for validator in self.m_validatorList]
        if len(vec) != len(self.m_operators) + 1 or Dice.CONDITION_STATE.ERROR_STATE in vec:
            return Dice.CONDITION_STATE.ERROR_STATE
        i = 0
        val = Dice.CONDITION_STATE.ERROR_STATE
        for op in self.m_operators:
            currentState = vec[i + 1]
            if i == 0:
                val = vec[i]
            if op == self.LogicOperation.OR:
                val = self.testAND(val, currentState)
            elif op == self.LogicOperation.EXCLUSIVE_OR:
                val = self.testOR(val, currentState)
            elif op == self.LogicOperation.AND:
                val = self.testXOR(val, currentState)
            elif op == self.LogicOperation.NONE:
                val = Dice.CONDITION_STATE.ERROR_STATE
            i += 1
        return val

    def setOperationList(self, m: List[int]):
        self.m_operators = m

    def setValidatorList(self, valids: List[Validator]):
        self.m_validatorList = valids

    def getCopy(self) -> Validator:
        val = CompositeValidator()
        val.setOperationList(self.m_operators)
        val.setValidatorList(self.m_validatorList)
        return val

    @staticmethod
    def testAND(before: int, current: int) -> int:
        if before == Dice.CONDITION_STATE.UNREACHABLE or current == Dice.CONDITION_STATE.UNREACHABLE:
            return Dice.CONDITION_STATE.UNREACHABLE
        elif before == Dice.CONDITION_STATE.ALWAYSTRUE and current == Dice.CONDITION_STATE.ALWAYSTRUE:
            return Dice.CONDITION_STATE.ALWAYSTRUE
        else:
            return Dice.CONDITION_STATE.REACHABLE

    @staticmethod
    def testOR(before: int, current: int) -> int:
        if before == Dice.CONDITION_STATE.UNREACHABLE and current == Dice.CONDITION_STATE.UNREACHABLE:
            return Dice.CONDITION_STATE.UNREACHABLE
        elif before == Dice.CONDITION_STATE.ALWAYSTRUE or current == Dice.CONDITION_STATE.ALWAYSTRUE:
            return Dice.CONDITION_STATE.ALWAYSTRUE
        else:
            return Dice.CONDITION_STATE.REACHABLE

    @staticmethod
    def testXOR(before: int, current: int) -> int:
        if before == current and (before == Dice.CONDITION_STATE.UNREACHABLE or before == Dice.CONDITION_STATE.ALWAYSTRUE):
            return Dice.CONDITION_STATE.UNREACHABLE
        elif (before != current) and (before == Dice.CONDITION_STATE.ALWAYSTRUE or before == Dice.CONDITION_STATE.UNREACHABLE) and (before != Dice.CONDITION_STATE.REACHABLE or current != Dice.CONDITION_STATE.REACHABLE):
            return Dice.CONDITION_STATE.ALWAYSTRUE
        else:
            return Dice.CONDITION_STATE.REACHABLE