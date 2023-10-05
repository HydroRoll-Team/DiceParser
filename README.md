OneRoll
=======

_This is a fork from Rolisteam/DiceParser, but all rewritten in Python._

> #### 注意
>名称可能和 OlivOS-Team/onedice 有点类似，但是这其中只是巧合，没有任何其他含义。

OneRoll，用一条指令实现几乎所有跑团所需功能之意（当然你还可以选择alias封装）。

### 语法

语法继承自 DiceParser，但有一些细微的改变。
```
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
```