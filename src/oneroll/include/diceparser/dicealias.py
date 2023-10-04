from enum import Enum


class DiceAlias:
    class RESOLUTION_TYPE(Enum):
        REPLACE = 0
        REGEXP = 1

    def __init__(self, pattern, command, comment="", isReplace=True, isEnable=True):
        self._pattern = pattern
        self._command = command
        self._comment = comment
        self._isReplace = isReplace
        self._isEnable = isEnable

    def resolved(self, string):
        # Implement the resolved method logic here
        pass

    def setPattern(self, pattern):
        self._pattern = pattern

    def setCommand(self, command):
        self._command = command

    def setComment(self, comment):
        self._comment = comment

    def setReplace(self, isReplace):
        self._isReplace = isReplace

    def setEnable(self, isEnable):
        self._isEnable = isEnable
