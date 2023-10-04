from executionnode import ExecutionNode
from result.diceresult import DiceResult
from result.stringresult import StringResult
from validatorlist import ValidatorList

class OccurenceCountNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_width = 1
        self.m_height = 0
        self.m_validatorList = None
        self.m_stringResult = None
        self.m_diceResult = None
    
    def run(self, previous=None):
        self.m_previousNode = previous
        mapOccurence = {}
        if self.m_previousNode is None:
            return
        
        previousDiceResult = isinstance(self.m_previousNode.getResult(), DiceResult)
        if previousDiceResult is None:
            return
        
        diceList = previousDiceResult.getResultList()
        vec = []
        
        for dice in diceList:
            val = dice.getValue()
            
            vec.append(val)
            it = mapOccurence.get(val)
            if it is None:
                mapOccurence[val] = 1
            else:
                mapOccurence[val] += 1
        
        vec.sort()
        if self.m_nextNode is None:
            self.runForStringResult(mapOccurence, vec)
        else:
            self.runForDiceResult(mapOccurence)
    
    def toString(self, withLabel):
        if withLabel:
            return f"{m_id} [label=\"OccurenceCountNode {m_id}\"]"
        else:
            return m_id
    
    def getCopy(self):
        return None
    
    def getPriority(self):
        priority = 0
        
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority
    
    def getWidth(self):
        return self.m_width
    
    def setWidth(self, width):
        self.m_width = width
    
    def getHeight(self):
        return self.m_height
    
    def setHeight(self, height):
        self.m_height = height
    
    def getValidatorList(self):
        return self.m_validatorList
    
    def setValidatorList(self, validatorlist):
        self.m_validatorList = validatorlist
    
    def runForStringResult(self, mapOccurence, vec):
        self.m_stringResult = StringResult()
        self.m_result = self.m_stringResult
        list = []
        for key, value in mapOccurence.items():
            if self.m_validatorList is not None:
                die = Die()
                die.insertRollValue(key)
                if not self.m_validatorList.hasValid(die, True):
                    continue
            
            if value < self.m_width:
                continue
            
            if key >= self.m_height:
                list.append(f"{key}x{value}")
        
        resultList = [str(val) for val in vec]
        
        result = ""
        if len(list) > 0:
            result = ','.join(list)
        else:
            result = "No matching result"
        
        self.m_stringResult.addText(f"{result} - [{','.join(resultList)}]")
        self.m_stringResult.finished()
    
    def runForDiceResult(self, mapOccurence):
        self.m_diceResult = DiceResult()
        self.m_result = self.m_diceResult
        for key, value in mapOccurence.items():
            if self.m_validatorList is not None:
                die = Die()
                die.insertRollValue(key)
                if not self.m_validatorList.hasValid(die, True):
                    continue
            
            if value < self.m_width:
                continue
            
            if key >= self.m_height:
                die = Die()
                die.insertRollValue(key * value)
                self.m_diceResult.insertResult(die)
        
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)