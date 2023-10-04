class SplitNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_result = self.m_diceResult

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            self.m_result.setPrevious(previous.getResult())

            tmpResult = previous.getResult()
            if tmpResult is not None:
                dice = tmpResult
                if isinstance(dice, DiceResult):
                    for oldDie in dice.getResultList():
                        oldDie.displayed()
                        m_diceResult.setOperator(oldDie.getOp())
                        for value in oldDie.getListValue():
                            tmpdie = Die()
                            tmpdie.insertRollValue(value)
                            tmpdie.setBase(oldDie.getBase())
                            tmpdie.setMaxValue(oldDie.getMaxValue())
                            tmpdie.setValue(value)
                            tmpdie.setOp(oldDie.getOp())
                            m_diceResult.insertResult(tmpdie)

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"SplitNode Node\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_nextNode is not None:
            priority = self.m_nextNode.getPriority()
        return priority

    def getCopy(self):
        node = SplitNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node