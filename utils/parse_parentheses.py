import ast
import re
from typing import List, Tuple

# re_parentheses = re.compile(r"\(+(.+?)\)+?")


# def find_all_string_parentheses(sear_str: str) -> List[str]:
#     """
#     寻找code里面的指标
#     :param sear_str:
#     :return:
#     """
#     return re_parentheses.findall(sear_str) or []


# def find_all_string_parentheses(sear_str: str) -> List[str]:
#     effect_result = []
#     simple_stack = []  # 栈
#     for idx, s in enumerate(sear_str):
#         if s == "(":
#             simple_stack.append((s, idx))
#         elif s == ")":
#             # 对称的括号，(xxx) 才为有效的
#             after_val, after_idx = simple_stack[-1]
#             if after_val == "(":
#                 effect_target = sear_str[after_idx + 1:idx]
#                 if effect_target:
#                     effect_result.append(effect_target)
#             simple_stack.append((s, idx))
#     return effect_result




def find_all_string_parentheses(sear_str: str) -> List[str]:
    # 有效括号
    EFFECT_PARENTHESES = {
        ")": "(",
        "]": "[",
        "}": "{",
        "【": "】"
    }
    if not sear_str or not isinstance(sear_str, str):
        return []

    effect_result = []
    simple_stack: List[Tuple[str, int]] = []  # 栈
    for idx, s in enumerate(sear_str):
        if s in EFFECT_PARENTHESES.values():
            # 右括号
            simple_stack.append((s, idx))

        elif s in EFFECT_PARENTHESES:
            # 左括号，(xxx) {xxx} [xxx] 对称的括号才为有效的
            after_val, after_idx = simple_stack[-1]
            if after_val == EFFECT_PARENTHESES.get(s):
                effect_target = sear_str[after_idx + 1:idx]  # 切片无所谓索引
                if effect_target:
                    effect_result.append(effect_target)
            simple_stack.append((s, idx))
    return effect_result


FORMULA_SET_CONFIG = {
    "sum3", "avg2", "current", "current_zero_exception", "current_nto",
    "sum1", "sum1_d2h", "sum1_increment"
}


def find_all_string_parentheses_with_ast(sear_str: str) -> List[str]:
    if not sear_str or not isinstance(sear_str, str):
        return []
    ast_nodes = []
    for node in ast.walk(ast.parse(sear_str)):
        if isinstance(node, ast.Call):
            ast_nodes.extend([i.id for i in node.args])
        elif isinstance(node, ast.Name):
            ast_nodes.append(node.id)
    func_result = [
        node
        for node in ast_nodes
        if node not in FORMULA_SET_CONFIG
    ]
    return func_result


if __name__ == '__main__':
    print(find_all_string_parentheses_with_ast(
        "( current(日不合格数)   /   current(日累计) )  *   100"))
    print(find_all_string_parentheses_with_ast(
        "current(计算理论节拍) / current(实际节拍) *100"))
    print(find_all_string_parentheses_with_ast(
        "((((current(日上班时间) - current(日关机时间)) - current(日速度损失)) - current(设备中断时间)))"))
    print(find_all_string_parentheses_with_ast(
        "( current(月上班时间) - current(月关机时间) - current(月速度损失) - current(月中断时间) )*3600/ current(月累计) "))
    print(find_all_string_parentheses_with_ast("None"))
    print(find_all_string_parentheses_with_ast(
        'sum1(p_pzng_0000)+sum1(p_pzng_0001)+sum1(p_pzng_0002)+sum1(p_pzng_0003)+sum1(p_pzng_0004)+sum1(p_pzng_0005)+sum1(p_pzng_0006)+sum1(p_pzng_0007)+sum1(p_pzng_0008)+sum1(p_pzng_0009)+sum1(p_pzng_0010)'))
    print(find_all_string_parentheses_with_ast("( 月加工时间   /  (( 月上班时间   -   月关机时间 )  -   月中断时间 ))  *   100 "))
