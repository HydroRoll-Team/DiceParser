from .diceresult import DiceResult, Die


class StringResult(DiceResult):
    def __init__(self):
        super().__init__()
        self.m_value = []
        self.m_highlight = True
        self.m_stringCount = 0
        self.m_commaSeparator = True

    def addText(self, text):
        self.m_value.append(text)

    def finished(self):
        if self.isDigitOnly():
            for val in self.m_value:
                die = Die()
                die.setMaxValue(self.m_stringCount)
                die.setValue(int(val))
                self.insertResult(die)

    def getText(self):
        return ",".join(self.m_value) if self.m_commaSeparator else "".join(self.m_value)

    def getResult(self, resultType):
        if resultType == Dice.RESULT_TYPE.STRING:
            return self.getText()
        elif resultType == Dice.RESULT_TYPE.SCALAR:
            return self.getScalarResult()
        else:
            return None

    def toString(self, wl):
        if wl:
            return f"{self.getText().replace('%', '_')} [label=\"StringResult_value_{self.m_id}\"]"
        else:
            return self.m_id

    def setHighLight(self, b):
        self.m_highlight = b

    def hasHighLight(self):
        return self.m_highlight

    def hasResultOfType(self, resultType):
        if resultType == Dice.RESULT_TYPE.STRING:
            return not self.isDigitOnly()
        elif resultType == Dice.RESULT_TYPE.SCALAR:
            return self.isDigitOnly()
        elif resultType == Dice.RESULT_TYPE.DICE_LIST:
            return self.isDigitOnly() and len(self.m_value) > 1
        else:
            return False

    def setNoComma(self, b):
        self.m_commaSeparator = not b

    def setStringCount(self, count):
        self.m_stringCount = count

    def isDigitOnly(self):
        return all(val.isdigit() for val in self.m_value)

    def getCopy(self):
        copy = StringResult()
        copy.setPrevious(self.getPrevious())
        copy.setHighLight(self.m_highlight)
        copy.m_value = self.m_value.copy()
        return copy

    def getStringResult(self):
        return self.getText()