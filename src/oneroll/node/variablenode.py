class VariableNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_index = 0
        self.m_data = None

    def run(self, previous):
        self.m_previousNode = previous
        if self.m_data is not None and len(self.m_data) > self.m_index:
            value = self.m_data[self.m_index]
            value = ParsingToolBox.getLeafNode(value)
            if value is None:
                return

            result = value.getResult()
            if not result:
                return

            self.m_result = result.getCopy()
            diceResult = isinstance(result, DiceResult)
            if diceResult:
                for die in diceResult.getResultList():
                    die.setDisplayed(False)

            if self.m_nextNode is not None:
                self.m_nextNode.run(self)
        else:
            self.m_errors[Dice.ERROR_CODE.NO_VARIBALE] = QObject.tr("No variable at index:%1").arg(self.m_index + 1)

    def setDisplayed(self):
        if not self.m_result:
            return
        diceResult = isinstance(self.m_result, DiceResult)
        if diceResult:
            for die in diceResult.getResultList():
                die.setDisplayed(True)

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"VariableNode index: {self.m_index + 1}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 4
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self):
        node = VariableNode()
        node.setIndex(self.m_index)
        if self.m_data is not None:
            node.setData(self.m_data)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def getIndex(self):
        return self.m_index

    def setIndex(self, index):
        self.m_index = index

    def getData(self):
        return self.m_data

    def setData(self, data):
        self.m_data = data