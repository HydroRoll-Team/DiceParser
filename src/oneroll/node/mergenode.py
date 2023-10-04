mergenode.py:

from typing import List

from node.executionnode import ExecutionNode
from result.diceresult import DiceResult


class MergeNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_diceResult = DiceResult()
        self.m_startList = None

    def run(self, previous: ExecutionNode):
        if previous is None:
            self.m_errors[Dice.ERROR_CODE.NO_PREVIOUS_ERROR] = "No previous node before Merge operator"
            return

        self.m_previousNode = previous
        self.m_result.setPrevious(previous.getResult())
        previousLast = None
        pastResult = []
        for start in self.m_startList:
            last = self.get_latest_node(start)
            if last is None or previousLast is None:
                previousLast = last
                continue

            startResult = start.getResult()
            if startResult is None:
                continue

            startResult.setPrevious(previousLast.getResult())
            previousLast.setNextNode(start)

            previousLast = last
            tmpResult = last.getResult()
            while tmpResult is not None:
                dice = tmpResult  # Assume tmpResult is a DiceResult
                if isinstance(dice, DiceResult):
                    self.m_diceResult.setHomogeneous(False)
                    for die in dice.getResultList():
                        if die not in self.m_diceResult.getResultList() and not die.hasBeenDisplayed():
                            tmpdie = Die(die)  # Assume Die is a class defined elsewhere
                            die.displayed()
                            self.m_diceResult.getResultList().append(tmpdie)

                if tmpResult.getPrevious() not in pastResult:
                    pastResult.append(previousLast.getResult())
                    tmpResult = tmpResult.getPrevious()
                else:
                    tmpResult.setPrevious(None)
                    tmpResult = None

        first = self.m_startList[0]
        self.m_startList.clear()
        self.m_startList.append(first)

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def get_latest_node(self, node: ExecutionNode):
        next_node = node
        while next_node.getNextNode() is not None and next_node.getNextNode() != self:
            next_node = next_node.getNextNode()
        return next_node

    def to_string(self, with_label: bool) -> str:
        if with_label:
            return f"{self.m_id} [label=\"Merge Node\"]"
        else:
            return self.m_id

    def get_priority(self) -> int:
        priority = 0
        if self.m_previousNode is not None:
            priority = self.m_previousNode.getPriority()
        return priority

    def get_copy(self):
        node = MergeNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node

    def get_start_list(self) -> List[ExecutionNode]:
        return self.m_startList

    def set_start_list(self, start_list: List[ExecutionNode]):
        self.m_startList = start_list