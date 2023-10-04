listaliasnode.py:

from diceparser.dicealias import DiceAlias
from executionnode import ExecutionNode
from result.stringresult import StringResult

class ListAliasNode(ExecutionNode):
    def __init__(self, mapAlias):
        self.m_aliasList = mapAlias
        self.m_result = StringResult()

    def run(self, previous=None):
        self.m_previousNode = previous
        txtResult = self.m_result
        txtResult.setHighLight(False)

        txtResult.addText(self.buildList())
        txtResult.finished()

        if previous is not None:
            self.m_result.setPrevious(previous.getResult())

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def buildList(self):
        result = "List of Alias:\n"
        for key in self.m_aliasList:
            result += "{0} : {1}  # {2}\n".format(key.pattern(), key.command(), key.comment())
        return result

    def toString(self, wl):
        resultList = []
        for key in self.m_aliasList:
            resultList.append("{{{0} {1}}}".format(key.pattern(), key.command()))

        if wl:
            return "{0} [label=\"ListAliasNode {1}\"]".format(self.m_id, ", ".join(resultList))
        else:
            return self.m_id

    def getPriority(self):
        return 0

    def getCopy(self):
        node = ListAliasNode(self.m_aliasList)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node