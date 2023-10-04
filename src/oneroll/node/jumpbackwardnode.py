class JumpBackwardNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_backwardNode = None
        self.m_diceResult = DiceResult()

    def getPriority(self):
        return 4

    def toString(self, wl):
        if wl:
            return "{} [label=\"JumpBackwardNode\"]".format(self.__str__())
        else:
            return self.__str__()

    def generateDotTree(self, s):
        s.append(self.toString(True))
        s.append(";\n")

        if self.m_backwardNode is not None:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.m_backwardNode.toString(False))
            s.append("[label=\"backward\"];\n")
            # self.m_backwardNode.generateDotTree(s)

        if self.m_nextNode is not None:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.m_nextNode.toString(False))
            s.append("[label=\"next\"];\n")
            self.m_nextNode.generateDotTree(s)
        else:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append("nullptr;\n")

            if self.m_result is not None:
                s.append(self.toString(False))
                s.append(" ->")
                s.append(self.m_result.toString(False))
                s.append(" [label=\"Result\"];\n")
                self.m_result.generateDotTree(s)


    def run(self, previous):
        self.m_previousNode = previous
        parent = previous
        found = False
        result = None

        while parent is not None and not found:
            result = parent.getResult()
            if result is not None:
                if result.hasResultOfType(Dice.RESULT_TYPE.DICE_LIST):
                    found = True
                    self.m_backwardNode = parent
                else:
                    jpNode = parent
                    if jpNode is not None:
                        found = True
                        self.m_backwardNode = parent
            if not found:
                parent = parent.getPreviousNode()

        if result is None:
            self.m_errors[Dice.ERROR_CODE.DIE_RESULT_EXPECTED] = "The @ operator expects dice result. Please check the documentation to fix your command."
        else:
            diceResult = result
            if diceResult is not None:
                for die in diceResult.getResultList():
                    tmpdie = Die(die)
                    self.m_diceResult.insertResult(tmpdie)
                    die.displayed()

            self.m_result.setPrevious(previous.getResult())

            if self.m_nextNode is not None:
                self.m_nextNode.run(self)

            if diceResult is not None:
                for i in range(len(diceResult.getResultList())):
                    tmp = diceResult.getResultList()[i]
                    tmp2 = self.m_diceResult.getResultList()[i]
                    if tmp.isHighlighted():
                        tmp2.setHighlighted(True)

    def getCopy(self):
        node = JumpBackwardNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node
