from executionnode import ExecutionNode
from range import Range
from result.diceresult import DiceResult
from result.stringresult import StringResult

class ListSetRollNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_values = []
        self.m_diceResult = DiceResult()
        self.m_stringResult = StringResult()
        self.m_rangeIndexResult = []
        self.m_unique = False
        self.m_rangeList = []

    def getList(self):
        return self.m_values

    def toString(self, wl):
        if wl:
            return f"{self.m_id} [label=\"ListSetRoll list:{','.join(self.m_values)}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 4
        return priority

    def run(self, previous):
        self.previousNode = previous
        if previous is not None:
            result = previous.getResult()
            if result is not None:
                diceCount = result.getResult(Dice.RESULT_TYPE.SCALAR)
                if diceCount > len(self.m_values) and self.m_unique:
                    self.m_errors[Dice.ERROR_CODE.TOO_MANY_DICE] = "More unique values asked than possible values (L operator)"
                else:
                    self.m_result.setPrevious(result)
                    for i in range(diceCount):
                        rollResult = []
                        die = Die()
                        self.computeFacesNumber(die)
                        die.roll()
                        self.m_diceResult.insertResult(die)
                        self.getValueFromDie(die, rollResult)
                        for str in rollResult:
                            self.m_stringResult.addText(str)
                    self.m_stringResult.finished()
                if self.m_nextNode is not None:
                    self.m_nextNode.run(self)
    
    def setListValue(self, lirs):
        self.m_values = lirs
    
    def setUnique(self, u):
        self.m_unique = u
    
    def setNoComma(self, b):
        if self.m_stringResult:
            self.m_stringResult.setNoComma(b)
    
    def setRangeList(self, ranges):
        self.m_rangeList = ranges
    
    def computeFacesNumber(self, die):
        if not self.m_rangeList:
            die.setMaxValue(len(self.m_values))
        else:
            assert len(self.m_values) == len(self.m_rangeList)
            max_value = 0
            for i, range in enumerate(self.m_rangeList):
                if (i == 0 or max_value < range.getEnd()) and range.isFullyDefined():
                    max_value = range.getEnd()
            die.setMaxValue(max_value)
    
    def getValueFromDie(self, die, rollResult):
        if not self.m_rangeList:
            if die.getValue() - 1 < len(self.m_values):
                str = self.m_values[die.getValue() - 1]
                while self.m_unique and str in rollResult:
                    die.roll(False)
                    str = self.m_values[die.getValue() - 1]
                rollResult.append(str)
        else:
            assert len(self.m_values) == len(self.m_rangeList)
            found = False
            while not found:
                for i, range in enumerate(self.m_rangeList):
                    it = next((x for x in self.m_rangeIndexResult if x == i), None)
                    isValid = range.hasValid(die, False)
                    if (isValid and not self.m_unique) or (isValid and it is None):
                        self.m_rangeIndexResult.append(i)
                        rollResult.append(self.m_values[i])
                        found = True
                    i += 1
                if not found:
                    die.roll(False)
    
    def getCopy(self):
        node = ListSetRollNode()
        dataList = self.m_rangeList.copy()
        node.setRangeList(dataList)
        node.setUnique(self.m_unique)
        node.setListValue(self.m_values)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node
