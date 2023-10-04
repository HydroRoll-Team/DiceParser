class Range(Validator):
    def __init__(self):
        self.m_start = 0
        self.m_end = 0
        self.m_hasEnd = False
        self.m_hasStart = False
        self.m_emptyRange = False

    def setValue(self, s, e):
        self.m_start = s
        self.m_end = e
        self.m_hasEnd = True
        self.m_hasStart = True

    def hasValid(self, m, recursive, unhighlight):
        result = 0
        if recursive:
            for value in m.getListValue():
                if value >= self.m_start and value <= self.m_end:
                    result += 1
        elif m.getLastRolledValue() >= self.m_start and m.getLastRolledValue() <= self.m_end:
            result += 1
        if unhighlight and result == 0:
            m.setHighlighted(False)
        return result

    def toString(self):
        return "[{}-{}]".format(self.m_start, self.m_end)

    def isValidRangeSize(self, range):
        minRange = min(self.m_start, self.m_end)
        minPossibleValue = min(range[0], range[1])

        maxRange = max(self.m_start, self.m_end)
        maxPossibleValue = max(range[0], range[1])

        if minRange == minPossibleValue and maxRange == maxPossibleValue:
            return Dice.CONDITION_STATE.ALWAYSTRUE
        elif maxRange < minPossibleValue or minRange > maxPossibleValue:
            return Dice.CONDITION_STATE.UNREACHABLE
        else:
            return Dice.CONDITION_STATE.UNREACHABLE

    def setStart(self, start):
        self.m_start = start
        self.m_hasStart = True

    def setEnd(self, end):
        self.m_end = end
        self.m_hasEnd = True

    def isFullyDefined(self):
        return self.m_hasEnd and self.m_hasStart

    def getStart(self):
        return self.m_start

    def getEnd(self):
        return self.m_end

    def setEmptyRange(self, b):
        self.m_emptyRange = b

    def isEmptyRange(self):
        return self.m_emptyRange

    def getCopy(self):
        val = Range()
        val.setEmptyRange(self.m_emptyRange)
        if self.m_hasEnd:
            val.setEnd(self.m_end)
        if self.m_hasStart:
            val.setStart(self.m_start)
        return val