# 导入ast模块
import ast

# 定义一个函数，用来解析表达式字符串，并返回AST
def parse_expr(expr):
    # 使用ast.parse函数，将表达式字符串转换为AST
    # mode参数指定只解析表达式，而不是完整的语句
    tree = ast.parse(expr, mode='eval')
    # 返回AST的根节点，即Expression节点
    return tree.body

# 定义一个函数，用来遍历AST，并求值
def eval_expr(node):
    # 如果节点是一个二元运算节点，例如加减乘除
    if isinstance(node, ast.BinOp):
        # 递归地求出左右子节点的值
        left = eval_expr(node.left)
        right = eval_expr(node.right)
        # 根据运算符的类型，进行相应的计算，并返回结果
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
    # 如果节点是一个数字节点，直接返回它的值
    elif isinstance(node, ast.Num):
        return node.n
    # 如果节点是其他类型，抛出异常
    else:
        raise Exception('Unsupported node type: ' + node.__class__.__name__)

# 测试一些表达式
exprs = ['1 + 2 * 3', '(1 + 2) * 3', '4 / 2 - 1', '2 ** 3']
for expr in exprs:
    # 解析表达式，得到AST
    node = parse_expr(expr)
    # 求值AST，得到结果
    result = eval_expr(node)
    # 打印表达式和结果
    print(expr, '=', result)
