class StartingNode(ExecutionNode):
    def __init__(self):
        super().__init__()

    def run(self, node):
        self.previousNode = None
        if self.nextNode is not None:
            self.nextNode.run(self)

    def toString(self, withlabel):
        if withlabel:
            return f"{self.id} [label=\"StartingNode\"]"
        else:
            return self.id

    def getPriority(self):
        priority = 0
        if self.nextNode is not None:
            priority = self.nextNode.getPriority()
        return priority

    def getCopy(self):
        node = StartingNode()
        if self.nextNode is not None:
            node.setNextNode(self.nextNode.getCopy())
        return node