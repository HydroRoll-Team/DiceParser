from typing import Dict
from math import pow
from executionnode import ExecutionNode
from scalarresult import ScalarResult
from dice import ArithmeticOperator, ERROR_CODE

class ScalarOperatorNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_internalNode = None
        self.m_scalarResult = ScalarResult()
        self.m_arithmeticOperator = ArithmeticOperator.PLUS

    def run(self, previous: ExecutionNode):
        self.m_previousNode = previous
        if self.m_internalNode is not None:
            self.m_internalNode.run(self)
        if previous is not None:
            previousResult = previous.getResult()
            if previousResult is not None:
                internal = self.m_internalNode
                if internal is not None:
                    while internal.getNextNode() is not None:
                        internal = internal.getNextNode()
                    internalResult = internal.getResult()
                    self.m_result.setPrevious(internalResult)
                    if self.m_internalNode.getResult() is not None:
                        self.m_internalNode.getResult().setPrevious(previousResult)
                    if internalResult is None:
                        self.m_errors[ERROR_CODE.NO_VALID_RESULT] = f"No Valid result in arithmetic operation: {self.toString(True)}"
                        return
                    if self.m_arithmeticOperator == ArithmeticOperator.PLUS:
                        self.m_scalarResult.setValue(self.add(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR)))
                    elif self.m_arithmeticOperator == ArithmeticOperator.MINUS:
                        self.m_scalarResult.setValue(self.substract(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR)))
                    elif self.m_arithmeticOperator == ArithmeticOperator.MULTIPLICATION:
                        self.m_scalarResult.setValue(self.multiple(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR)))
                    elif self.m_arithmeticOperator == ArithmeticOperator.DIVIDE:
                        self.m_scalarResult.setValue(self.divide(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR)))
                    elif self.m_arithmeticOperator == ArithmeticOperator.INTEGER_DIVIDE:
                        self.m_scalarResult.setValue(int(self.divide(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR))))
                    elif self.m_arithmeticOperator == ArithmeticOperator.POW:
                        self.m_scalarResult.setValue(self.pow(previousResult.getResult(RESULT_TYPE.SCALAR), internalResult.getResult(RESULT_TYPE.SCALAR)))
                if self.m_nextNode is not None:
                    self.m_nextNode.run(self)

    def setInternalNode(self, node: ExecutionNode):
        self.m_internalNode = node

    @staticmethod
    def add(a: float, b: float) -> int:
        return int(a + b)

    @staticmethod
    def substract(a: float, b: float) -> int:
        return int(a - b)

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            self.m_errors[ERROR_CODE.DIVIDE_BY_ZERO] = "Division by zero"
            return 0
        return float(a / b)

    @staticmethod
    def multiple(a: float, b: float) -> int:
        return int(a * b)

    @staticmethod
    def pow(a: float, b: float) -> int:
        return int(pow(a, b))

    def getArithmeticOperator(self) -> ArithmeticOperator:
        return self.m_arithmeticOperator

    def setArithmeticOperator(self, arithmeticOperator: ArithmeticOperator):
        self.m_arithmeticOperator = arithmeticOperator

    def toString(self, wl: bool) -> str:
        op = ""
        if self.m_arithmeticOperator == ArithmeticOperator.PLUS:
            op = "+"
        elif self.m_arithmeticOperator == ArithmeticOperator.MINUS:
            op = "-"
        elif self.m_arithmeticOperator == ArithmeticOperator.MULTIPLICATION:
            op = "*"
        elif self.m_arithmeticOperator == ArithmeticOperator.DIVIDE:
            op = "/"
        elif self.m_arithmeticOperator == ArithmeticOperator.INTEGER_DIVIDE:
            op = "|"
        elif self.m_arithmeticOperator == ArithmeticOperator.POW:
            op = "^"
        if wl:
            return f"{self.m_id} [label=\"ScalarOperatorNode {op}\"]"
        else:
            return self.m_id

    def getPriority(self) -> int:
        if self.m_arithmeticOperator == ArithmeticOperator.PLUS or self.m_arithmeticOperator == ArithmeticOperator.MINUS:
            return 1
        elif self.m_arithmeticOperator == ArithmeticOperator.POW:
            return 3
        else:
            return 2

    def generateDotTree(self, s: str):
        id = self.toString(True)
        if id in s:
            return
        s += id
        s += ";\n"
        if self.m_nextNode is not None:
            s += self.toString(False)
            s += " -> "
            s += self.m_nextNode.toString(False)
            s += "[label=\"nextNode\"];\n"
            self.m_nextNode.generateDotTree(s)
        else:
            s += self.toString(False)
            s += " -> nullptr [label=\"nextNode\"];\n"
        if self.m_result is not None:
            s += self.toString(False)
            s += " ->"
            s += self.m_result.toString(False)
            s += " [label=\"Result\", style=\"dashed\"];\n"
            if self.m_nextNode is None:
                self.m_result.generateDotTree(s)
        str = "\n"
        if self.m_internalNode is not None:
            str += self.toString(False)
            str += " -> "
            str += self.m_internalNode.toString(False)
            str += " [label=\"internalNode\"];\n"
            self.m_internalNode.generateDotTree(str)
        s += str

    def getExecutionErrorMap(self) -> Dict[ERROR_CODE, str]:
        if self.m_internalNode is not None:
            keys = self.m_internalNode.getExecutionErrorMap().keys()
            for key in keys:
                self.m_errors[key] = self.m_internalNode.getExecutionErrorMap()[key]
        if self.m_nextNode is not None:
            keys = self.m_nextNode.getExecutionErrorMap().keys()
            for key in keys:
                self.m_errors[key] = self.m_nextNode.getExecutionErrorMap()[key]
        return self.m_errors

    def getCopy(self) -> ExecutionNode:
        node = ScalarOperatorNode()
        node.setInternalNode(self.m_internalNode.getCopy())
        node.setArithmeticOperator(self.m_arithmeticOperator)
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node