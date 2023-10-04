class ValidatorResult:
    def __init__(self):
        self.m_validDice = []
        self.m_allTrue = False

    def validDice(self):
        return self.m_validDice

    def validDiceRef(self):
        return self.m_validDice

    def setValidDice(self, pairs):
        self.m_validDice = pairs

    def appendValidDice(self, die, sum):
        self.m_validDice.append((die, sum))

    def setAllTrue(self, allTrue):
        self.m_allTrue = allTrue

    def allTrue(self):
        return self.m_allTrue

    def contains(self, die):
        return any(pair[0] == die for pair in self.m_validDice)


class ValidatorList:
    def __init__(self):
        self.m_operators = []
        self.m_validatorList = []

    def hasValid(self, b, recursive, unhighlight=False):
        i = 0
        sum = 0
        highLight = False
        for validator in self.m_validatorList:
            val = validator.hasValid(b, recursive, unhighlight)
            if i == 0:
                sum = val
                if b.isHighlighted():
                    highLight = b.isHighlighted()
            else:
                if self.m_operators[i - 1] == Dice.LogicOperation.OR:
                    sum |= val
                    if highLight:
                        b.setHighlighted(highLight)
            i += 1
        return sum

    def setOperationList(self, m):
        self.m_operators = m

    def setValidators(self, valids):
        self.m_validatorList = valids

    def validResult(self, result, recursive, unlight, functor):
        validityData = []
        for validator in self.m_validatorList:
            validResult = ValidatorResult()
            conditionType = validator.getConditionType()
            if conditionType == Dice.ConditionType.OnEach:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    continue
                for die in diceResult.getResultList():
                    score = validator.hasValid(die, recursive, unlight)
                    if score:
                        validResult.appendValidDice(die, score)
            elif conditionType == Dice.ConditionType.OnEachValue:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    continue
                for die in diceResult.getResultList():
                    score = validator.hasValid(die, recursive, unlight)
                    if score:
                        validResult.appendValidDice(die, score)
            elif conditionType == Dice.ConditionType.AllOfThem:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    continue
                diceList = diceResult.getResultList()
                allValid = all(validator.hasValid(die, recursive, unlight) for die in diceList)
                if allValid:
                    validResult.setAllTrue(True)
                    for die in diceResult.getResultList():
                        validResult.appendValidDice(die, die.getValue())
            elif conditionType == Dice.ConditionType.OneOfThem:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    continue
                diceList = diceResult.getResultList()
                anyValid = any(validator.hasValid(die, recursive, unlight) for die in diceList)
                if anyValid:
                    validResult.setAllTrue(True)
                    for die in diceResult.getResultList():
                        validResult.appendValidDice(die, die.getValue())
            validityData.append(validResult)

        if not validityData:
            return

        finalResult = ValidatorResult()
        for vec in validityData:
            diceList = vec.validDice()
            if not finalResult.validDice():
                finalResult.validDiceRef().extend(diceList)
            else:
                id = len(self.m_operators)
                if id >= len(self.m_operators):
                    continue
                op = self.m_operators[id]
                if op == Dice.LogicOperation.OR:
                    finalResult.validDiceRef().extend(diceList)
                elif op == Dice.LogicOperation.AND:
                    mergeResultsAsAND(vec, finalResult)
                elif op == Dice.LogicOperation.EXCLUSIVE_OR:
                    mergeResultsAsExeclusiveOR(vec, finalResult)

        if finalResult.allTrue():
            diceResult = getDiceResult(result)
            if diceResult is not None:
                diceList = diceResult.getResultList()
                finalResult.validDiceRef().extend((die, 0) for die in diceList)

        for die, score in finalResult.validDice():
            functor(die, score)

    def getCopy(self):
        val = ValidatorList()
        val.setOperationList(self.m_operators)
        val.setValidators(self.m_validatorList)
        return val


    def mergeResultsAsAND(diceList, result):
        val = ValidatorResult()
        for dice in diceList.validDice():
            if result.contains(dice[0]) or diceList.allTrue():
                val.appendValidDice(dice[0], dice[1])
        result.setValidDice(val.validDice())
        result.setAllTrue(diceList.allTrue() and result.allTrue())


    def mergeResultsAsExeclusiveOR(diceList, result):
        val = ValidatorResult()
        for dice in diceList.validDice():
            if not result.contains(dice[0]):
                val.appendValidDice(dice[0], dice[1])
        result.setValidDice(val.validDice())
        result.setAllTrue(diceList.allTrue() ^ result.allTrue())


    def getDiceResult(result):
        dice = result.getResult(Dice.RESULT_TYPE.SCALAR)
        if dice is None:
            value = result.getResult(Dice.RESULT_TYPE.SCALAR).toInt()
            dice = DiceResult()
            die = Die()
            die.setValue(value)
            dice.insertResult(die)
            print("Error, no dice result")
            # TODO: manage error here.
        return dice


class ValidatorList:
    def __init__(self):
        self.m_operators = []
        self.m_validatorList = []

    def ValidatorList(self):
        del self.m_validatorList[:]

    def hasValid(self, b, recursive, unhighlight):
        i = 0
        sum = 0
        highLight = False
        for validator in self.m_validatorList:
            val = validator.hasValid(b, recursive, unhighlight)
            if i == 0:
                sum = val
                if b.isHighlighted():
                    highLight = b.isHighlighted()
            else:
                if self.m_operators[i - 1] == Dice.LogicOperation.OR:
                    sum |= val
                    if highLight:
                        b.setHighlighted(highLight)
            i += 1
        return sum

    def setOperationList(self, m):
        self.m_operators = m

    def setValidators(self, valids):
        del self.m_validatorList[:]
        self.m_validatorList = valids

    def validResult(self, result, recursive, unlight, functor):
        validityData = []
        for validator in self.m_validatorList:
            validResult = ValidatorResult()
            conditionType = validator.getConditionType()
            if conditionType == Dice.ConditionType.OnScalar:
                die = Die()
                scalar = result.getResult(Dice.RESULT_TYPE.SCALAR).toInt()
                die.insertRollValue(scalar)
                if validator.hasValid(die, recursive, unlight):
                    validResult.setAllTrue(True)
                    diceResult = getDiceResult(result)
                    if diceResult is None:
                        break
                    if len(self.m_validatorList) > 1:
                        for die in diceResult.getResultList():
                            validResult.appendValidDice(die, die.getValue())
                    else:
                        validResult.appendValidDice(Die(die), die.getValue())
            elif conditionType == Dice.ConditionType.OnEach:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    break
                for die in diceResult.getResultList():
                    score = validator.hasValid(die, recursive, unlight)
                    if score:
                        validResult.appendValidDice(die, score)
            elif conditionType == Dice.ConditionType.OnEachValue:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    break
                for die in diceResult.getResultList():
                    score = validator.hasValid(die, recursive, unlight)
                    if score:
                        validResult.appendValidDice(die, score)
                allValid = all(validator.hasValid(die, recursive, unlight) for die in diceResult.getResultList())
                if allValid:
                    validResult.setAllTrue(True)
                    for die in diceResult.getResultList():
                        validResult.appendValidDice(die, die.getValue())
            elif conditionType == Dice.ConditionType.OneOfThem:
                diceResult = getDiceResult(result)
                if diceResult is None:
                    break
                diceList = diceResult.getResultList()
                anyValid = any(validator.hasValid(die, recursive, unlight) for die in diceList)
                if anyValid:
                    validResult.setAllTrue(True)
                    for die in diceResult.getResultList():
                        validResult.appendValidDice(die, die.getValue())
            validityData.append(validResult)

        if not validityData:
            return

        i = 0
        finalResult = ValidatorResult()

        for vec in validityData:
            diceList = vec.validDice()
            if i == 0:
                finalResult.setValidDice(diceList)
            else:
                id = i - 1
                if id >= len(self.m_operators):
                    continue
                op = self.m_operators[id]
                if op == Dice.LogicOperation.EXCLUSIVE_OR:
                    mergeResultsAsExeclusiveOR(vec, finalResult)
            i += 1

        if finalResult.allTrue():
            diceResult = getDiceResult(result)
            if diceResult is not None:
                diceList = diceResult.getResultList()
                finalResult.setValidDice([(die, 0) for die in diceList])

        for die, score in finalResult.validDice():
            functor(die, score)

    def getCopy(self):
        val = ValidatorList()
        val.setOperationList(self.m_operators)
        val.setValidators(self.m_validatorList)
        return val
