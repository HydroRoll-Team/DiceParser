class DiceRollerNode(ExecutionNode):
    def __init__(self, max, min=1):
        self.m_max = max
        self.m_min = min
        self.m_diceResult = DiceResult()
        self.m_operator = Dice.ArithmeticOperator.PLUS
        self.m_unique = False

    def run(self, previous):
        self.m_previousNode = previous
        if previous is not None:
            result = previous.getResult()
            if result is not None:
                num = result.getResult(Dice.RESULT_TYPE.SCALAR)
                if num <= 0:
                    self.m_errors[Dice.ERROR_CODE.NO_DICE_TO_ROLL] = "No dice to roll"
                self.m_diceCount = int(num) if num > 0 else 0
                self.m_result.setPrevious(result)

                possibleValue = abs((self.m_max - self.m_min) + 1)
                if possibleValue < self.m_diceCount and self.m_unique:
                    self.m_errors[Dice.ERROR_CODE.TOO_MANY_DICE] = "More unique values asked than possible values (D operator)"
                    return

                for i in range(self.m_diceCount):
                    die = Die()
                    die.setOp(self.m_operator)
                    die.setBase(self.m_min)
                    die.setMaxValue(self.m_max)
                    die.roll()
                    if self.m_unique:
                        equal = lambda a, b: a.getValue() == b.getValue()
                        while self.m_diceResult.contains(die, equal):
                            die.roll(False)
                    self.m_diceResult.insertResult(die)

                if self.m_nextNode is not None:
                    self.m_nextNode.run(self)

    def getFaces(self):
        return abs(self.m_max - self.m_min) + 1

    def getRange(self):
        return (self.m_min, self.m_max)

    def toString(self, wl):
        if wl:
            return f"{self.m_id} [label=\"DiceRollerNode faces: {self.getFaces()}\"]"
        else:
            return self.m_id

    def getPriority(self):
        priority = 4
        return priority

    def getCopy(self):
        node = DiceRollerNode(self.m_max, self.m_min)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def getOperator(self):
        return self.m_operator

    def setOperator(self, dieOperator):
        self.m_operator = dieOperator
        self.m_diceResult.setOperator(dieOperator)

    def getUnique(self):
        return self.m_unique

    def setUnique(self, unique):
        self.m_unique = unique