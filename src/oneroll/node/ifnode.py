from .explodedicenode import ExecutionNode
from ..result.diceresult import DiceResult
from ..include.diceparser.diceparserhelper import Dice

class ValidatorList:
    pass

class PartialDiceRollNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()

    def insertDie(self, die):
        self.m_diceResult.insertResult(die)

    def run(self, previous=None):
        self.m_previousNode = previous
        presult = previous.getResult()
        if presult is not None:
            self.m_result.setPrevious(presult)
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def getCopy(self):
        return PartialDiceRollNode()

    def getPriority(self):
        priority = 4
        return priority

    def toString(self, withLabel):
        if withLabel:
            return f"{self.m_id} [label=\"PartialDiceRollNode \"]"
        else:
            return self.m_id

def getFirstDiceResult(result):
    found = None

    if result is None:
        return found
    while found is None and result is not None:
        found = isinstance(result, DiceResult)
        result = result.getPrevious()

    return found

class IfNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_conditionType = Dice.ConditionType.AllOfThem
        self.m_true = None
        self.m_false = None

    def run(self, previous):
        self.m_previousNode = previous
        if previous is None:
            return
        previousLoop = previous
        nextNode = None
        runNext = False if self.m_nextNode is None else True
        previousResult = previous.getResult()
        self.m_result = previousResult.getCopy()

        if self.m_result is not None:
            value = previousResult.getResult(Dice.RESULT_TYPE.SCALAR)

            if self.m_validatorList is not None:
                previousDiceResult = getFirstDiceResult(previousResult)
                if previousDiceResult is not None:
                    diceList = previousDiceResult.getResultList()

                    if self.m_conditionType == Dice.ConditionType.OnEach:
                        for dice in diceList:
                            diceNode = PartialDiceRollNode()
                            diceNode.insertDie(Die(dice))
                            if self.m_validatorList.hasValid(dice, True, True):
                                nextNode = self.m_true.getCopy() if self.m_true is not None else None
                            else:
                                nextNode = self.m_false.getCopy() if self.m_false is not None else None

                            if nextNode is not None:
                                if previousLoop.getNextNode() is None:
                                    previousLoop.setNextNode(nextNode)
                                if self.m_nextNode is None:
                                    self.m_nextNode = nextNode
                                diceNode.setNextNode(nextNode)
                                diceNode.run(previousLoop)
                                previousLoop = self.getLeafNode(nextNode)

                    elif self.m_conditionType == Dice.ConditionType.OneOfThem or self.m_conditionType == Dice.ConditionType.AllOfThem:
                        trueForAll = True
                        falseForAll = True

                        oneIsTrue = False
                        oneIsFalse = False

                        for dice in diceList:
                            result = self.m_validatorList.hasValid(dice, True, True)
                            trueForAll = trueForAll and result
                            falseForAll = falseForAll and result

                            oneIsTrue |= result
                            oneIsFalse = not result or oneIsFalse
                        if self.m_conditionType == Dice.ConditionType.OneOfThem:
                            if oneIsTrue:
                                nextNode = self.m_true.getCopy() if self.m_true is not None else None
                            else:
                                nextNode = self.m_false.getCopy() if self.m_false is not None else None
                        elif self.m_conditionType == Dice.ConditionType.AllOfThem:
                            if trueForAll:
                                nextNode = self.m_true.getCopy() if self.m_true is not None else None
                            else:
                                nextNode = self.m_false.getCopy() if self.m_false is not None else None

                        if nextNode is not None:
                            if self.m_nextNode is None:
                                self.m_nextNode = nextNode
                            nextNode.run(previousLoop)
                            previousLoop = self.getLeafNode(nextNode)

                    if self.m_conditionType == Dice.ConditionType.OnScalar:
                        dice = Die()
                        val = int(value)
                        dice.setValue(val)
                        dice.insertRollValue(val)
                        dice.setMaxValue(val)
                        if self.m_validatorList.hasValid(dice, True, True):
                            nextNode = self.m_true
                        else:
                            nextNode = self.m_false
                        if nextNode is not None:
                            if self.m_nextNode is None:
                                self.m_nextNode = nextNode
                            nextNode.run(previousLoop)
                            previousLoop = self.getLeafNode(nextNode)

        if self.m_nextNode is not None and runNext:
            self.m_nextNode.run(previousLoop)

    def setValidatorList(self, val):
        self.m_validatorList = val

    def setInstructionTrue(self, node):
        self.m_true = node

    def setInstructionFalse(self, node):
        self.m_false = node

    def generateDotTree(self, s):
        s.append(self.toString(True))
        s.append(";\n")

        if self.m_true is not None and self.m_true != self.m_nextNode:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.m_true.toString(False))
            s.append("[label=\"true" + self.m_validatorList.toString() + "\"];\n")

            self.m_true.generateDotTree(s)
        if self.m_false is not None and self.m_false != self.m_nextNode:
            s.append(self.toString(False))
            s.append(" -> ")
            s.append(self.m_false.toString(False))
            s.append("[label=\"false\"];\n")
            self.m_false.generateDotTree(s)

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

    def toString(self, wl):
        if wl:
            return f"{self.m_id} [label=\"IfNode\"]"
        else:
            return self.m_id

    def getPriority(self):
        return 0

    def getLeafNode(self, node):
        nextNode = node
        while nextNode.getNextNode() is not None:
            nextNode = nextNode.getNextNode()
        return nextNode

    def getConditionType(self):
        return self.m_conditionType

    def setConditionType(self, conditionType):
        self.m_conditionType = conditionType

    def getCopy(self):
        node = IfNode()

        node.setConditionType(self.m_conditionType)
        if self.m_validatorList is not None:
            node.setValidatorList(self.m_validatorList.getCopy())
        if self.m_false is not None:
            node.setInstructionFalse(self.m_false.getCopy())
        if self.m_true is not None:
            node.setInstructionTrue(self.m_true.getCopy())
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node