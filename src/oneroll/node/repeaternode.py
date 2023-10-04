from node.executionnode import ExecutionNode
from result.scalarresult import ScalarResult
from result.stringresult import StringResult
from diceparser.diceparserhelper import DiceParserHelper
from diceparser.parsingtoolbox import ParsingToolBox

class RepeaterNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_cmd = []
        self.m_times = None
        self.m_sumAll = False

    def run(self, previousNode):
        self.m_previousNode = previousNode

        if self.m_times is None or len(self.m_cmd) == 0:
            return

        self.m_times.run(self)
        self.m_times = ParsingToolBox.getLeafNode(self.m_times)
        times = self.m_times.getResult()
        if times is None:
            return

        m_startingNodes = []
        timeCount = times.getResult(Dice.RESULT_TYPE.SCALAR).toInt()
        cmd = self.makeCopy(self.m_cmd)
        resultVec = []
        for i in range(timeCount):
            m_startingNodes.append(cmd)
            for node in cmd:
                node.run(self)
                end = ParsingToolBox.getLeafNode(node)
                leafResult = end.getResult()

                if leafResult is None:
                    continue

                resultVec.append(leafResult)
            cmd = self.makeCopy(self.m_cmd)
        if self.m_sumAll:
            scalar = ScalarResult()
            value = 0.0
            for result in resultVec:
                value += result.getResult(Dice.RESULT_TYPE.SCALAR).toDouble()
            scalar.setValue(value)
            self.m_result = scalar
        else:
            string = StringResult()

            listOfStrResult = []
            for instructions in m_startingNodes:
                parsingBox = ParsingToolBox()
                parsingBox.setStartNodes(instructions)
                finalString = parsingBox.finalStringResult(lambda result, _, __: result)
                listOfStrResult.append(finalString)
            if len(listOfStrResult) > 0:
                string.addText('\n'.join(listOfStrResult))

            self.m_result = string

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, withLabel):
        return "" if withLabel else ""

    def getPriority(self):
        return 4

    def getCopy(self):
        return None

    def setCommand(self, cmd):
        self.m_cmd = cmd

    def setTimeNode(self, time):
        self.m_times = time

    def setSumAll(self, b):
        self.m_sumAll = b

    @staticmethod
    def makeCopy(cmds):
        copy = []
        for node in cmds:
            copy.append(node.getCopy())
        return copy