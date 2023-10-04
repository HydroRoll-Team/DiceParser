from node.executionnode import ExecutionNode
from result.scalarresult import ScalarResult

class NumberNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_number = 0
        self.m_scalarResult = ScalarResult()

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            self.m_result.setPrevious(previous.getResult())
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def setNumber(self, a):
        self.m_scalarResult.setValue(a)
        self.m_number = a

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"NumberNode {self.m_number}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = NumberNode()
        node.setNumber(self.m_number)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node