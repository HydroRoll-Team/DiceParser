from enum import Enum, auto

# 完善TokenType类，添加通配符以及其他字符
class TokenType(Enum):
    EOF = auto()
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    ID = auto()
    ASSIGN = auto()
    SEMI = auto()
    COMMA = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    EQ = auto()
    NEQ = auto()
    AND = auto()

# 编写tokenize函数，对code:str参数进行遍历解析返回list[Token]
def tokenize(code: str):
    result = []
    i = 0
    while i < len(code):
        if code[i] == ' ':
            i += 1
            continue
        elif code[i] == '+':
            result.append(Token(TokenType.PLUS, i))
            i += 1
            continue
        elif code[i] == '-':
            result.append(Token(TokenType.MINUS, i))
            i += 1
            continue
        elif code[i] == '*':
            result.append(Token(TokenType.MUL, i))
            i += 1
            continue
        elif code[i] == '/':
            result.append(Token(TokenType.DIV, i))
            i += 1
            continue
        elif code[i] == '(':