"""Token 类
定义了 OneRoll 的一些 Token 类型。

有以下规则:
    1. 遵循 `EBNF` 范式。
    2. 非终结符双驼峰命名。
    3. 终结符单驼峰命名。   
    4. 特殊地，语义对象使用全大写命名。

"""

from enum import Enum


class TokenType(Enum):
    """
    Program =: Instruction [InstructionSeparator, Instruction]* Comment
    InstructionSeparator = ;
    Instruction =: Expression ([Operator, Expression]* | [Option]*)
    Operator =: ScalarOperator
    Expression =: OpenParenthesis Expression closeParenthesis
    | Option*
    | [Operator, Expression]*
    | Operand Dice
    | Command
    | function
    | NodeOperator [Option]*
    | ValuesList
    | Dice (Operand == 1)
    Operand =: DynamicVariable | Number | String
    OpenParenthesis = (
    closeParenthesis = )
    OpenList = [
    CloseList = ]
    ListSeparator = ,
    ValuesList=: OpenList (DynamicVariable | Number)? [ ListSeparator,(DynamicVariable | Number)]*  CloseList
    Dice =: DiceOperator [uniqueValue] DiceParameter
    DiceOperator =: D ParameterDice | L ParameterList
    DiceParameter =: ParameterDice | ParameterList
    ParameterDice =: Number|Range
    ParameterList =: List
    List=: OpenList String[Probability] [ListSeparator,String[Probability]]* CloseList
    Probability=: OpenList (Range|Percentage) CloseList
    Percentage =: number
    function =: functionName OpenParenthesis [function_args] closeParenthesis
    function_args =: Instruction [InstructionSeparator, Instruction] | Operand | ValidatorList
    functionName =: repeat
    Option =: Keep
    | KeepAndExplode
    | Filter
    | Sort
    | Count
    | Reroll
    | RerollUntil
    | RerollAndAdd
    | Explode
    | Merge
    | Bind
    | Occurences
    | Unique
    | Paint
    | If
    | Split
    | Group
    Range =: OpenList Number RangeSeparator Number CloseList
    RangeSeparator =: ..
    ScalarOperator =: [x,-,*,x,/,**]
    number =: [-] [0-9]+ | constantValue
    OpenVaribale=: ${
    CloseVariable=: }
    constantValue =: OpenVaribale (id | label) CloseVariable
    id=[_,a-z][_,A-z,0-9]* # must respect rules of QML id
    label=.*
    variable = OpenVaribale [0-9]+ CloseVariable
    ValidatorList =: OpenList CompareMethod Validator [LogicOpetator CompareMethod Validator]* CloseList
    LogicOpetator =: AND | XOR |  OR
    CompareMethod =: Each |  All | Scalar | ANY
    Each=:
    All=: *
    Scalar=: :
    ANY=: .
    AND =: &
    XOR =: ^
    OR =: |
    Ascendant=:l
    Validator =: BooleanValidator | RangeValidator | OperationValidator
    CompareOpetator =: = | > | >= | < | <= | !=
    RangeValidator =: Range
    OperationValidator =: Modulo operandNode BooleanValidator
    Modulo =: %
    BooleanValidator =: [=]Operand | [CompareOpetator Operand]
    ListOfValue=: String[Range],ListOfValue | String[Range]
    String =: .*[^ListSeparator]
    Keep =: k[Ascendant] Number
    KeepAndExplode =: K[Ascendant] number
    Filter =: f ValidatorList
    Sort =: s[Ascendant]
    Count =: c ValidatorList
    Reroll =: r ValidatorList
    RerollUntil =: R ValidatorList
    RerollAndAdd =: a ValidatorList
    Merge =: m
    Bind =: b
    Occurences =: OccurencesWidth ( ListSeparator  number | ValidatorList)
    OccurencesWidth =: number
    unique =: u
    Painter =: p PainterParameters
    PainterParameters =: OpenList PairColorOccurence [ListSeparator , PairColorOccurence]* CloseList
    PairColorOccurence =: Color PairSeparator Number
    PairSeparator =: :
    If =: i [compareMethod] ValidatorList Bloc[Bloc]
    compareMethod =: OnEach | OneOfThem | AllOfThem | onScalar
    OnEach =: ''
    OneOfThem = '.'
    AllOfThem = '*'
    onScalar = ':'
    Bloc =: OpenBranch Expression CloseBranch
    OpenBloc =: {
    CloseBloc =: }
    Split =: y
    Group =: g Number
    Sort =: s
    Group =: number
    Explode =: e ValidatorList
    NodeOperator = Jumpbackward
    Jumpbackward =: @
    Merge =: m | m Expression
    Command =: help | la
    uniqueValue = u
    Comment =: StartComment String
    StartComment =: #
    """

    OpenParenthesis = r"\("
    closeParenthesis = r"\)"
    OpenList = r"\["
    CloseList = r"\]"
    ListSeparator = r","
    InstructionSeparator = r";"
    SPACE = r" \t\r"
    RangeSeparator = r"\.\."
    ScalarOperator = rf"[+-*/]|**"
    OpenVaribale = r"\$\{"
    CloseVariable = r"\}"
    Each = r""  # 存疑
    All = r"\*"
    Scalar = r":"
    # Sort = r"s"
    ANY = r"\."
    AND = r"\&"
    XOR = r"\^"
    OR = r"\|"
    Ascendant = r"l"
    CompareOpetator = r"=|>|>=|<|<=|!="
    Modulo = r"\%"
    # Merge = r"m"
    Bind = r"b"
    unique = r"u"
    PairSeparator = r"\:"
    OnEach = r""
    OneOfThem = r"\."
    AllOfThem = r"\*"
    onScalar = r"\:"
    OpenBloc = r"\{"
    CloseBloc = r"\}"
    Split = r"y"
    Jumpbackward = r"@"
    label = r".*"
    ID = r"[_a-z][_A-z0-9]*"  # must respect rules of QML id\
    Number = INTEGER = r"[1-9]+[0-9]*|0"

    uniqueValue = r"u"
    Command = r"help|la"
    Merge = rf"m|m{{Expression}}"
    NodeOperator = rf"{Jumpbackward}"
    # Group =: number
    constantValue = rf"{OpenVaribale}({ID}|{label}){CloseVariable}"
    number = rf"[-]?[0-9]+|{constantValue}"
    Group = rf"g{Number}"
    Bloc = rf"{{OpenBranch}}{{Expression}}{{CloseBranch}}"
    compareMethod = rf"{OnEach}|{OneOfThem}|{AllOfThem}|{onScalar}"
    PairColorOccurence = rf"Color{PairSeparator}{Number}"
    PainterParameters = rf"{OpenList}{PairColorOccurence}[{ListSeparator}{PairColorOccurence}]*{CloseList}"
    Painter = rf"p{PainterParameters}"
    OccurencesWidth = rf"{number}"
    Sort = rf"s[{Ascendant}]"
    KeepAndExplode = rf"K[{Ascendant}]{number}"
    Keep = rf"k[{Ascendant}]{Number}"
    String = rf".*[^{ListSeparator}]"
    CompareMethod = rf"{Each}|{All}|{Scalar}|{ANY}"
    LogicOpetator = rf"{AND}|{XOR}|{OR}"
    variable = rf"{OpenVaribale}[0-9]+{CloseVariable}"
    Range = rf"{OpenList}{Number}{RangeSeparator}{Number}{CloseList}"
    RangeValidator = rf"{Range}"
    functionName = r"repeat"
    Percentage = rf"{number}"
    Probability = rf"{OpenList}({Range}|{Percentage}){CloseList}"
    List = rf"{OpenList}{String}[{Probability}][{ListSeparator}{String}[{Probability}]]*{CloseList}"
    ParameterList = rf"{List}"
    ParameterDice = rf"{Number}|{Range}"
    DiceParameter = rf"{ParameterDice}|{ParameterList}"
    DiceOperator = rf"D{ParameterDice}|L{ParameterList}"
    Dice = rf"{DiceOperator}[{uniqueValue}]{DiceParameter}"
    Operand = rf"{{DynamicVariable}}|{Number}|{String}"
    BooleanValidator = rf"[=]{Operand}|[{CompareOpetator}{Operand}]"
    OperationValidator = rf"{Modulo}{{operandNode}}{BooleanValidator}"
    Validator = rf"{BooleanValidator}|{RangeValidator}|{OperationValidator}"
    ValidatorList = rf"{OpenList}{CompareMethod}{Validator}[{LogicOpetator}{CompareMethod}{Validator}]*{CloseList}"
    IF = rf"i[{compareMethod}]{ValidatorList}{Bloc}[{Bloc}]"
    Filter = rf"f{ValidatorList}"
    ValuesList = rf"{OpenList}({{DynamicVariable}}|{Number})?[{ListSeparator}({{DynamicVariable}}|{Number})]*{CloseList}"
    Explode = rf"e{ValidatorList}"
    Occurences = rf"{OccurencesWidth}({ListSeparator}{number}|{ValidatorList})"
    RerollAndAdd = rf"a{ValidatorList}"
    RerollUntil = rf"R{ValidatorList}"
    Reroll = rf"r{ValidatorList}"
    Count = rf"c{ValidatorList}"
    ListOfValue = rf"{String}[{Range}]{{ListOfValue}}|{String}[{Range}]"
    Operator = rf"{ScalarOperator}"
    Option = rf"{Keep}|{KeepAndExplode}|{Filter}|{Sort}|{Count}|{Reroll}|{RerollUntil}|{RerollAndAdd}|{Explode}|{Merge}|{Bind}|{Occurences}|{unique}|{Painter}|{IF}|{Split}|{Group}"
    Function = rf"{functionName}{OpenParenthesis}[{{function_args}}]{closeParenthesis}"
    Expression = rf"{OpenParenthesis} {{Expression}} {closeParenthesis}"
    Instruction = rf"{Expression}([{Operator}{Expression}]*|[{Option}])"
    function_args = (
        rf"{Instruction}[{InstructionSeparator}{Instruction}]|{Operand}|{ValidatorList}"
    )
    # Expression = rf"{Option}*|[{Operator}{Expression}]*|[{Operand} {Dice}]|{Command}|{Function}|{NodeOperator}[{Option}]*|{ValuesList}|{Dice}({Operand})"
    StartComment = r"#"
    Comment = rf"{StartComment} {String}"
    Program = (
        rf"{Instruction}[{InstructionSeparator}{Instruction}]?[{SPACE}]?{Comment}?"
    )


EOF = r"EOF"


class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        """String representation of the class instance.

        Example:
            >>> Token(TokenType.INTEGER, 7, lineno=5, column=10)
            Token(TokenType.INTEGER, 7, position=5:10)
        """
        return "Token({type}, {value}, position={lineno}:{column})".format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )

    def __repr__(self):
        return self.__str__()


def _build_reserved_keywords():
    """Build a dictionary of reserved keywords.

    The function relies on the fact that in the TokenType
    enumeration the beginning of the block of reserved keywords is
    marked with PROGRAM and the end of the block is marked with
    the END keyword.

    Result:
        {'PROGRAM': <TokenType.PROGRAM: 'PROGRAM'>,
         'INTEGER': <TokenType.INTEGER: 'INTEGER'>,
         'REAL': <TokenType.REAL: 'REAL'>,
         'DIV': <TokenType.INTEGER_DIV: 'DIV'>,
         'VAR': <TokenType.VAR: 'VAR'>,
         'PROCEDURE': <TokenType.PROCEDURE: 'PROCEDURE'>,
         'BEGIN': <TokenType.BEGIN: 'BEGIN'>,
         'END': <TokenType.END: 'END'>}
    """
    # enumerations support iteration, in definition order
    tt_list = list(TokenType)
    start_index = tt_list.index(TokenType.OpenParenthesis)
    end_index = tt_list.index(TokenType.Program)
    reserved_keywords = {
        token_type.value: token_type
        for token_type in tt_list[start_index : end_index + 1]
    }
    return reserved_keywords


RESERVED_KEYWORDS = _build_reserved_keywords()


print(TokenType.Program)
