paintnode.py:

from executionnode import ExecutionNode
from diceresult import DiceResult
from typing import List

class ColorItem:
    def __init__(self, str: str, val: int):
        self.m_colorNumber = val
        self.m_color = str

    def colorNumber(self) -> int:
        return self.m_colorNumber

    def setColorNumber(self, colorNumber: int):
        self.m_colorNumber = colorNumber

    def color(self) -> str:
        return self.m_color

    def setColor(self, color: str):
        self.m_color = color

class PainterNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_colors = []
        self.m_diceResult = None

    def run(self, previous: ExecutionNode = None):
        self.m_previousNode = previous
        if previous is None:
            self.m_errors[Dice.ERROR_CODE.NO_PREVIOUS_ERROR] = "No previous node before Paint operator"
            return
        previousResult = previous.getResult()
        if previousResult is None:
            return

        self.m_diceResult = DiceResult(previousResult.getCopy())
        if self.m_diceResult is not None:
            diceList = self.m_diceResult.getResultList()
            pastDice = 0
            for item in self.m_colors:
                current = item.colorNumber()
                it = iter(diceList)
                for _ in range(pastDice):
                    next(it)
                for die in it:
                    if current > 0:
                        die.setColor(item.color())
                        current -= 1
                        pastDice += 1
                    else:
                        break
            self.m_diceResult.setPrevious(previousResult)
            self.m_result = self.m_diceResult
        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, wl: bool = True) -> str:
        if wl:
            return f"{self.m_id} [label=\"PainterNode\"]"
        else:
            return self.m_id

    def getPriority(self) -> int:
        return 4

    def insertColorItem(self, color: str, value: int):
        item = ColorItem(color, value)
        self.m_colors.append(item)

    def getCopy(self) -> ExecutionNode:
        node = PainterNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node