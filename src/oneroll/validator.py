from typing import List, Callable, Tuple, Set
from diceparser.die import Die
from diceparser.dice import ConditionType

class Validator:
    def __init__(self):
        self.m_values: Set[int] = set()
        self.m_conditionType: ConditionType = ConditionType.OnEach

    def hasValid(self, b: Die, recursive: bool, unlight: bool = False) -> int:
        raise NotImplementedError

    def toString(self) -> str:
        raise NotImplementedError

    def isValidRangeSize(self, range: Tuple[int, int]) -> Dice.CONDITION_STATE:
        raise NotImplementedError

    def getCopy(self) -> 'Validator':
        raise NotImplementedError

    def getPossibleValues(self, range: Tuple[int, int]) -> Set[int]:
        raise NotImplementedError

    def validResult(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        result: int
        if self.m_conditionType == ConditionType.OnEach:
            result = self.onEach(b, recursive, unlight, functor)
        elif self.m_conditionType == ConditionType.OnEachValue:
            result = self.onEachValue(b, recursive, unlight, functor)
        elif self.m_conditionType == ConditionType.OneOfThem:
            result = self.oneOfThem(b, recursive, unlight, functor)
        elif self.m_conditionType == ConditionType.AllOfThem:
            result = self.allOfThem(b, recursive, unlight, functor)
        elif self.m_conditionType == ConditionType.OnScalar:
            result = self.onScalar(b, recursive, unlight, functor)
        return result

    def onEach(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        result: int = 0
        for die in b:
            if self.hasValid(die, recursive, unlight):
                result += 1
                functor(die, recursive, unlight)
        return result

    def onEachValue(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        result: int = 0
        for die in b:
            if self.hasValid(die, recursive, unlight):
                result += 1
                functor(die, recursive, unlight)
        return result

    def oneOfThem(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        oneOfThem: bool = any(self.hasValid(die, recursive, unlight) for die in b)
        if oneOfThem:
            functor(recursive, unlight)
        return 1 if oneOfThem else 0

    def allOfThem(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        all: bool = all(self.hasValid(die, recursive, unlight) for die in b)
        if all:
            functor(recursive, unlight)
        return 1 if all else 0

    def onScalar(self, b: List[Die], recursive: bool, unlight: bool, functor: Callable) -> int:
        result: int = 0
        for die in b:
            result += die.getValue()
        die = Die()
        die.setValue(result)
        if self.hasValid(die, recursive, unlight):
            functor(recursive, unlight)
            return 1
        return 0

    def getPossibleValues(self, range: Tuple[int, int]) -> Set[int]:
        return self.m_values

    def getConditionType(self) -> ConditionType:
        return self.m_conditionType

    def setConditionType(self, conditionType: ConditionType) -> None:
        self.m_conditionType = conditionType