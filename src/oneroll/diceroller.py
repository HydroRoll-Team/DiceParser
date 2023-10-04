import json
from PySide2.QtCore import QObject, Signal
from PySide2.QtConcurrent import QtConcurrent

class DiceRoller(QObject):
    commandChanged = Signal()
    resultChanged = Signal()
    errorOccurs = Signal()
    diceListChanged = Signal()
    resultStrChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_diceList = ""
        self.m_resultStr = ""
        self.m_command = ""
        self.m_result = 0.0
        self.m_error = ""
        self.m_diceparser = DiceParser()

    def diceList(self):
        return self.m_diceList

    def resultStr(self):
        return self.m_resultStr

    def command(self):
        return self.m_command

    def result(self):
        return self.m_result

    def setCommand(self, cmd):
        if self.m_command != cmd:
            self.m_command = cmd
            self.commandChanged.emit()

    def readErrorAndWarning(self):
        self.setError("Error:\n{}\nWarnings:\n{}".format(self.m_diceparser.humanReadableError(), self.m_diceparser.humanReadableWarning()))

    def start(self):
        def run():
            if self.m_diceparser.parseLine(self.m_command):
                self.m_diceparser.start()
                self.readErrorAndWarning()
                jsonstr = self.m_diceparser.resultAsJSon(lambda value, _, __: value)
                doc = json.loads(jsonstr)
                self.m_result = float(doc["scalar"])
                self.resultChanged.emit()

        future = QtConcurrent.run(run)

    def error(self):
        return self.m_error

    def aliases(self):
        return self.m_diceparser.aliases()

    def parser(self):
        return self.m_diceparser

    def setError(self, error):
        if self.m_error == error:
            return

        self.m_error = error
        self.errorOccurs.emit()