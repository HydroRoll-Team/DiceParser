from oneroll.diceast import RollTransformer

from lark import Lark

# 定义一个简单的语法
grammar = """
    start: expr

    expr: NUMBER
    %import common.NUMBER
    %ignore " "
"""

# 创建一个 Lark 解析器
parser = Lark(grammar, start="start", parser="lalr")

# 示例输入字符串
input_string = "42"

# 解析输入字符串
tree = parser.parse(input_string)

# 创建转换器的实例
transformer = RollTransformer()

# 转换语法树
result = transformer.transform(tree)

# 打印结果（这将取决于实际 AST 的结构）
print(result)
