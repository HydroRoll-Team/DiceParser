from .executionnode import ExecutionNode
from ..result.diceresult import DiceResult, Die

class BindNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_startList = None
        
    def run(self, previous):
        self.m_previousNode = previous
        if self.m_previousNode is None:
            return
        
        self.m_result.setPrevious(previous.getResult())
        for start in self.m_startList:
            last = self.getLatestNode(start)
            if last is not None:
                tmpResult = last.getResult()
                while tmpResult is not None:
                    dice = isinstance(tmpResult, DiceResult)
                    if dice:
                        self.m_diceResult.setHomogeneous(False)
                        for die in dice.getResultList():
                            if not die.hasBeenDisplayed():
                                tmpdie = Die(die)
                                die.displayed()
                                self.m_diceResult.getResultList().append(tmpdie)
                    tmpResult = tmpResult.getPrevious()
        
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)
    
    def getLatestNode(self, node):
        nextNode = node
        while nextNode.getNextNode() is not None and nextNode.getNextNode() != self:
            nextNode = nextNode.getNextNode()
        return nextNode
    
    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"Bind Node\"]"
        else:
            return self.m_id
    
    def getPriority(self):
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority
    
    def getCopy(self):
        node = BindNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node
    
    def getStartList(self):
        return self.m_startList
    
    def setStartList(self, startList):
        self.m_startList = startList