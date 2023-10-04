from node.executionnode import ExecutionNode
from result.stringresult import StringResult

class StringNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_data = ""
        self.m_stringResult = StringResult()

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            self.m_result.setPrevious(previous.getResult())
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def setString(self, string):
        self.m_data = string
        self.m_stringResult.addText(self.m_data)
        self.m_stringResult.finished()

    def toString(self, withLabel):
        if withLabel:
            dataCopy = self.m_data
            return f"{self.m_id} [label=\"StringNode {dataCopy.replace('%', '\\\\')}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = StringNode()
        node.setString(self.m_data)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node