sortresult.py:

class SortResultNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_ascending = True
        self.m_diceResult = DiceResult()

    def run(self, previous):
        self.m_previousNode = previous
        if previous is None:
            return
        previousDiceResult = previous.getResult()
        self.m_diceResult.setPrevious(previousDiceResult)
        if previousDiceResult is None:
            return

        diceList = previousDiceResult.getResultList()
        diceList2 = self.m_diceResult.getResultList()

        # half-interval search sorting
        for i in range(len(diceList)):
            tmp1 = Die(diceList[i])
            diceList[i].displayed()

            j = 0
            found = False
            start = 0
            end = len(diceList2)
            tmp2 = None
            while not found:
                distance = end - start
                j = (start + end) // 2
                if distance == 0:
                    j = end
                    found = True
                else:
                    tmp2 = diceList2[j]
                    if tmp1.getValue() < tmp2.getValue():
                        end = j
                    else:
                        start = j + 1
            diceList2.insert(j, tmp1)

        if not self.m_ascending:
            for i in range(len(diceList2) // 2):
                diceList2[i], diceList2[len(diceList2) - (1 + i)] = diceList2[len(diceList2) - (1 + i)], diceList2[i]

        self.m_diceResult.setResultList(diceList2)
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def setSortAscending(self, asc):
        self.m_ascending = asc

    def toString(self, wl):
        if wl:
            order = "Ascending" if self.m_ascending else "Descending"
            return f"{self.m_id} [label=\"SortResultNode {order}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def getCopy(self):
        node = SortResultNode()
        node.setSortAscending(self.m_ascending)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node