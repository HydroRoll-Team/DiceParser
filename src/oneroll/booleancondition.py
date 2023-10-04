from typing import List, Tuple
from diceparser.diceparserhelper import Die
from node.executionnode import ExecutionNode
from validator import Validator
from enum import Enum

class CompareOperator(Enum):
    Equal = "="
    GreaterThan = ">"
    LesserThan = "<"
    GreaterOrEqual = ">="
    LesserOrEqual = "<="
    Different = "!="

class CONDITION_STATE(Enum):
    UNREACHABLE = 0
    ALWAYSTRUE = 1
    REACHABLE = 2

def testEqual(insideRange: bool, range: Tuple[int, int]) -> CONDITION_STATE:
    if not insideRange:
        return CONDITION_STATE.UNREACHABLE
    elif insideRange and (range[0] == range[1]):
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

def testGreatherThan(value: int, range: Tuple[int, int]) -> CONDITION_STATE:
    if value >= max(range[0], range[1]):
        return CONDITION_STATE.UNREACHABLE
    elif value < min(range[0], range[1]):
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

def testLesserThan(value: int, range: Tuple[int, int]) -> CONDITION_STATE:
    if value <= min(range[0], range[1]):
        return CONDITION_STATE.UNREACHABLE
    elif value > max(range[0], range[1]):
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

def testGreaterOrEqual(value: int, range: Tuple[int, int]) -> CONDITION_STATE:
    if value > max(range[0], range[1]):
        return CONDITION_STATE.UNREACHABLE
    elif value <= min(range[0], range[1]):
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

def testLesserOrEqual(value: int, range: Tuple[int, int]) -> CONDITION_STATE:
    if value < min(range[0], range[1]):
        return CONDITION_STATE.UNREACHABLE
    elif value >= max(range[0], range[1]):
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

def testDifferent(inside: bool, range: Tuple[int, int]) -> CONDITION_STATE:
    if inside and (range[0] == range[1]):
        return CONDITION_STATE.UNREACHABLE
    elif not inside:
        return CONDITION_STATE.ALWAYSTRUE
    else:
        return CONDITION_STATE.REACHABLE

class BooleanCondition(Validator):
    def __init__(self):
        super().__init__()
        self.m_operator = CompareOperator.Equal
        self.m_value = None

    def __del__(self):
        if self.m_value is not None:
            del self.m_value
            self.m_value = None

    def hasValid(self, b: Die, recursive: bool, unhighlight: bool) -> int:
        listValues = []
        if self.m_conditionType == Dice.OnEachValue:
            listValues.append(b.getValue())
        elif recursive:
            listValues = b.getListValue()
        else:
            listValues.append(b.getLastRolledValue())

        sum = 0
        valueScalar = self.valueToScalar()
        for value in listValues:
            if self.m_operator == CompareOperator.Equal:
                sum += 1 if value == valueScalar else 0
            elif self.m_operator == CompareOperator.GreaterThan:
                sum += 1 if value > valueScalar else 0
            elif self.m_operator == CompareOperator.LesserThan:
                sum += 1 if value < valueScalar else 0
            elif self.m_operator == CompareOperator.GreaterOrEqual:
                sum += 1 if value >= valueScalar else 0
            elif self.m_operator == CompareOperator.LesserOrEqual:
                sum += 1 if value <= valueScalar else 0
            elif self.m_operator == CompareOperator.Different:
                sum += 1 if value != valueScalar else 0

        if unhighlight and sum == 0:
            b.setHighlighted(False)
        else:
            b.setHighlighted(True)

        return sum

    def setOperator(self, m: CompareOperator):
        self.m_operator = m

    def setValueNode(self, v: ExecutionNode):
        self.m_value = v

    def toString(self) -> str:
        str = ""
        if self.m_operator == CompareOperator.Equal:
            str += "="
        elif self.m_operator == CompareOperator.GreaterThan:
            str += ">"
        elif self.m_operator == CompareOperator.LesserThan:
            str += "<"
        elif self.m_operator == CompareOperator.GreaterOrEqual:
            str += ">="
        elif self.m_operator == CompareOperator.LesserOrEqual:
            str += "<="
        elif self.m_operator == CompareOperator.Different:
            str += "!="
        return "[{}{}]".format(str, self.valueToScalar())

    def isValidRangeSize(self, range: Tuple[int, int]) -> CONDITION_STATE:
        valueScalar = self.valueToScalar()
        boundValue = max(range[0], min(valueScalar, range[1]))
        isInsideRange = boundValue == valueScalar
        if self.m_operator == CompareOperator.Equal:
            return testEqual(isInsideRange, range)
        elif self.m_operator == CompareOperator.GreaterThan:
            return testGreatherThan(valueScalar, range)
        elif self.m_operator == CompareOperator.LesserThan:
            return testLesserThan(valueScalar, range)
        elif self.m_operator == CompareOperator.GreaterOrEqual:
            return testGreaterOrEqual(valueScalar, range)
        elif self.m_operator == CompareOperator.LesserOrEqual:
            return testLesserOrEqual(valueScalar, range)
        elif self.m_operator == CompareOperator.Different:
            return testDifferent(isInsideRange, range)

    def getCopy(self) -> Validator:
        val = BooleanCondition()
        val.setOperator(self.m_operator)
        val.setValueNode(self.m_value.getCopy())
        return val

    def valueToScalar(self) -> int:
        if self.m_value is None:
            return 0

        self.m_value.run(None)
        result = self.m_value.getResult()
        if result:
            return int(result.getResult(Dice.RESULT_TYPE.SCALAR))
        else:
            return 0