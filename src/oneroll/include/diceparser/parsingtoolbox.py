class SubtituteInfo:
    def __init__(self):
        self._length = 0
        self._resultIndex = 0
        self._position = 0
        self._digitNumber = 0
        self._subIndex = 0

    def isValid(self):
        return self._length > 0

    def length(self):
        return self._length

    def setLength(self, length):
        self._length = length

    def resultIndex(self):
        return self._resultIndex

    def setResultIndex(self, resultIndex):
        self._resultIndex = resultIndex

    def position(self):
        return self._position

    def setPosition(self, position):
        self._position = position

    def digitNumber(self):
        return self._digitNumber

    def setDigitNumber(self, digitNumber):
        self._digitNumber = digitNumber

    def subIndex(self):
        return self._subIndex

    def setSubIndex(self, subIndex):
        self._subIndex = subIndex
