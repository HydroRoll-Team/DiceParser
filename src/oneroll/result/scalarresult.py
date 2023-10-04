from .result import Result
from enum import Enum

class DiceResultType(Enum):
    SCALAR = 0

class ScalarResult(Result):
    def __init__(self):
        super().__init__()
        self.m_value = 0

    def setValue(self, i):
        self.m_value = i

    def getResult(self, type: DiceResultType):
        if type == DiceResultType.SCALAR:
            return self.m_value
        else:
            return None

    def getCopy(self):
        copy = ScalarResult()
        copy.setValue(self.m_value)
        return copy

    def toString(self, wl):
        if wl:
            return f"{self.m_value} [label=\"ScalarResult {self.m_id}\"]"
        else:
            return self.m_id