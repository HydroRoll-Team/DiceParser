import json
from typing import Callable, Dict, List, Tuple

class DiceParser:
    def __init__(self):
        self.parsingToolbox = ParsingToolBox()
        self.command = ""

    def constAliases(self) -> List[DiceAlias]:
        return self.parsingToolbox.getAliases()

    def aliases(self) -> List[DiceAlias]:
        return self.parsingToolbox.aliases()

    def cleanAliases(self):
        self.parsingToolbox.cleanUpAliases()

    def insertAlias(self, dice: DiceAlias, i: int):
        self.parsingToolbox.insertAlias(dice, i)

    def parseLine(self, str: str, allowAlias: bool) -> bool:
        if allowAlias:
            str = self.parsingToolbox.convertAlias(str)
        self.parsingToolbox.clearUp()
        self.command = str
        instructions = self.parsingToolbox.readInstructionList(str, True)
        self.command = self.command.replace(self.parsingToolbox.getComment(), "")
        value = bool(instructions)
        if not value:
            self.parsingToolbox.addError(Dice.ERROR_CODE.NOTHING_UNDERSTOOD,
                                         "Nothing was understood. To roll dice: !1d6 - full documentation: "
                                         "<a href=\"https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md\">"
                                         "https://github.com/Rolisteam/DiceParser/blob/master/HelpMe.md</a>")
        elif value and str:
            i = len(self.command) - len(str)
            self.parsingToolbox.addWarning(Dice.ERROR_CODE.UNEXPECTED_CHARACTER,
                                           f"Unexpected character at {i} - end of command was ignored \"{str}\"")

        if self.parsingToolbox.hasError():
            value = False

        return value

    def convertAlias(self, cmd: str) -> str:
        return self.parsingToolbox.convertAlias(cmd)

    def start(self):
        for start in self.parsingToolbox.getStartNodes():
            start.run()

    def diceCommand(self) -> str:
        return self.command

    def hasIntegerResultNotInFirst(self) -> bool:
        return self.parsingToolbox.hasIntegerResultNotInFirst()

    def hasDiceResult(self) -> bool:
        return self.parsingToolbox.hasDiceResult()

    def hasStringResult(self) -> bool:
        return self.parsingToolbox.hasStringResult()

    def startNodeCount(self) -> int:
        return len(self.parsingToolbox.getStartNodes())

    def scalarResultsFromEachInstruction(self) -> List[float]:
        return self.parsingToolbox.scalarResultsFromEachInstruction()

    def stringResultFromEachInstruction(self, hasAlias: bool) -> List[str]:
        return self.parsingToolbox.allFirstResultAsString(hasAlias)

    def diceResultFromEachInstruction(self) -> List[ExportedDiceResult]:
        return self.parsingToolbox.diceResultFromEachInstruction()

    def comment(self) -> str:
        return self.parsingToolbox.getComment()

    def setComment(self, comment: str):
        self.parsingToolbox.setComment(comment)

    def errorMap(self) -> Dict[Dice.ERROR_CODE, str]:
        map = {}
        for start in self.parsingToolbox.getStartNodes():
            mapTmp = start.getExecutionErrorMap()
            for key in mapTmp:
                map[key] = mapTmp[key]
        return map

    def humanReadableError(self) -> str:
        parsingError = self.parsingToolbox.getErrorList()
        str = ""
        for text in parsingError:
            str += text + "\n"

        errMap = self.errorMap()
        for text in errMap.values():
            str += text + "\n"
        return str

    def humanReadableWarning(self) -> str:
        warningMap = self.parsingToolbox.getWarningList()
        str = ""
        for value in warningMap.values():
            str += value + "\n"
        return str

    def finalStringResult(self, colorize: Callable[[str, str, bool], str]) -> str:
        return self.parsingToolbox.finalStringResult(colorize)

    def resultAsJSon(self, colorize: Callable[[str, str, bool], str], removeUnhighligthed: bool) -> str:
        obj = {}
        instructions = []
        for start in self.parsingToolbox.getStartNodes():
            inst = {}

            self.parsingToolbox.addResultInJson(inst, Dice.RESULT_TYPE.SCALAR, "scalar", start, True)
            self.parsingToolbox.addResultInJson(inst, Dice.RESULT_TYPE.STRING, "string", start, False)
            self.parsingToolbox.addDiceResultInJson(inst, start, colorize)

            instructions.append(inst)
        obj["instructions"] = instructions
        obj["comment"] = self.parsingToolbox.getComment()
        obj["error"] = self.humanReadableError()
        obj["scalar"] = self.parsingToolbox.finalScalarResult()[0]
        obj["string"] = self.parsingToolbox.finalStringResult(colorize, removeUnhighligthed)
        obj["warning"] = self.humanReadableWarning()
        obj["command"] = self.command

        return json.dumps(obj)

    def writeDownDotTree(self, filepath: str):
        if not self.parsingToolbox.getStartNodes():
            return

        str = "digraph ExecutionTree {\n"
        for start in self.parsingToolbox.getStartNodes():
            start.generateDotTree(str)
        str += "}\n"

        with open(filepath, "w") as file:
            file.write(str)

    def setPathToHelp(self, l: str):
        self.parsingToolbox.setHelpPath(l)

    def setVariableDictionary(self, variables: Dict[str, str]):
        ParsingToolBox.setVariableHash(variables)