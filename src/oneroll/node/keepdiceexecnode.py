class KeepDiceExecNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_numberOfDiceNode = None
        self.m_diceResult = DiceResult()

    def run(self, previous):
        self.m_previousNode = previous
        
        if previous is None or self.m_numberOfDiceNode is None:
            return
        
        self.m_numberOfDiceNode.run(previous)
        lastnode = ParsingToolBox.getLeafNode(self.m_numberOfDiceNode)
        
        if lastnode is None:
            return
        
        result = lastnode.getResult()
        
        if result is None:
            return
        
        if not result.hasResultOfType(Dice.RESULT_TYPE.SCALAR):
            return
        
        numberOfDice = result.getResult(Dice.RESULT_TYPE.SCALAR).toInt()
        
        previousDiceResult = previous.getResult()
        self.m_result.setPrevious(previousDiceResult)
        
        if previousDiceResult is not None:
            diceList = previousDiceResult.getResultList()
            
            if numberOfDice < 0:
                numberOfDice = len(diceList) + numberOfDice
            
            diceList3 = diceList[:numberOfDice]
            diceList2 = []
            
            for die in diceList3:
                tmpdie = Die(die)
                diceList2.append(tmpdie)
                die.displayed()
                die.setSelected(False)
            
            if numberOfDice > len(diceList):
                self.m_errors.insert(Dice.ERROR_CODE.TOO_MANY_DICE,
                                     " You ask to keep {} dice but the result only has {}".format(numberOfDice, len(diceList)))
            
            for tmp in diceList[numberOfDice: ]:
                tmp.setHighlighted(False)
            
            self.m_diceResult.setResultList(diceList2)
            
            if self.m_nextNode is not None:
                self.m_nextNode.run(self)
    
    def setDiceKeepNumber(self, n):
        self.m_numberOfDiceNode = n
    
    def toString(self, wl):
        if wl:
            return "{} [label=\"KeepDiceExecNode\"]".format(self.m_id)
        else:
            return self.m_id
    
    def getPriority(self):
        priority = 0
        
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        
        return priority
    
    def getCopy(self):
        node = KeepDiceExecNode()
        
        if self.m_numberOfDiceNode is not None:
            node.setDiceKeepNumber(self.m_numberOfDiceNode.getCopy())
        
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        
        return node