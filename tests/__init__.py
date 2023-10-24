import re
import random

def roll_dice(expression):
    # 定义正则表达式模式
    pattern = r'(\d+)([+\-*/])(\d+)d(\d+)'

    # 使用正则表达式匹配表达式中的各个Token
    matches = re.findall(pattern, expression)

    # 遍历匹配结果，计算掷骰结果
    result = 0
    for match in matches: 
        num1 = int(match[0])
        operator = match[1]
        num2 = int(match[2])
        dice_count = int(match[3])
        dice_sides = int(match[4])

        # 掷骰子并计算结果
        dice_result = sum(random.randint(1, dice_sides) for _ in range(dice_count))

        # 根据运算符更新结果
        if operator == '+':
            result += num1 + num2 + dice_result
        elif operator == '-':
            result += num1 + num2 - dice_result
        elif operator == '*':
            result += (num1 + num2) * dice_result
        elif operator == '/':
            result += (num1 + num2) / dice_result

    return result

# 测试示例表达式
expression = '3d4+2d6-5'
result = roll_dice(expression)
print(f'{expression} = {result}')
