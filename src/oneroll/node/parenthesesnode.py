class ParenthesesNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.internalNode = None

    def setInternalNode(self, node):
        self.internalNode = node

    def run(self, previous=None):
        self.previousNode = previous
        if self.internalNode:
            self.internalNode.run(self)
            temp = self.internalNode
            while temp.getNextNode():
                temp = temp.getNextNode()
            self.result = temp.getResult()

        if self.nextNode:
            self.nextNode.run(self)

    def toString(self, b):
        if b:
            return f"{self.id} [label=\"ParenthesesNode\"]"
        else:
            return self.id

    def getPriority(self):
        return 3

    def getCopy(self):
        node = ParenthesesNode()
        if self.internalNode:
            node.setInternalNode(self.internalNode.getCopy())
        if self.nextNode:
            node.setNextNode(self.nextNode.getCopy())
        return node

    def generateDotTree(self, s):
        str_repr = self.toString(True)
        if str_repr in s:
            return
        s.append(str_repr)
        s.append(";\n")

        if self.internalNode:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.internalNode.toString(False))
            s.append("[label=\"internal\"];\n")
            self.internalNode.generateDotTree(s)

        if self.nextNode:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.nextNode.toString(False))
            s.append(" [label=\"next\"];\n")
            self.nextNode.generateDotTree(s)
        else:
            s.append(self.toString(False))
            s.append(" -> nullptr;\n")

        if self.result:
            s.append(self.toString(False))
            s.append(" ->")
            s.append(self.result.toString(False))
            s.append(" [label=\"Result\", style=\"dashed\"];\n")
            if not self.nextNode:
                self.result.generateDotTree(s)