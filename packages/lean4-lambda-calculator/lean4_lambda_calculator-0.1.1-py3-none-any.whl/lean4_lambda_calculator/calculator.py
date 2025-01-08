# -*- coding: utf-8 -*-
"""
Author: Peng Lingwei
Date: 2024-11-27
License: MIT
"""

from lean4_lambda_calculator.level import Level, SuccLevel, MaxLevel, PreLevel, is_solvable
from lean4_lambda_calculator.expr import Expr, BoundVar, Const, Lambda, Forall, App, Sort, Arg, expr_rename_level, expr_todef, get_sort_eq_conditions

import time
import logging

# 全局日志开关
LOGGING_ENABLED = False

# 根据日志开关来动态设置日志级别
if LOGGING_ENABLED:
    logging.basicConfig(
        level=logging.INFO,  # 如果启用日志，设置为 INFO 或 DEBUG
        filename="./execution_times.log",
        filemode="a",  # 追加模式
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
else:
    logging.basicConfig(
        level=logging.CRITICAL,  # 如果禁用日志，设置为 CRITICAL 这样只有最严重的日志会输出
    )

# 记录函数执行时间的装饰器
def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000  # 转换为毫秒
        logging.info(f"{func.__name__} executed in {duration_ms:.2f} ms")
        return result
    return wrapper

# 求解表达式的类型
# 返回化简后的表达式和类型
@log_execution_time
def calc(expr: Expr, context: list[Arg] = None, type_pool: dict[str, Expr] = None, def_pool: dict[str, Expr] = None, used_free_symbols: set[str] = None, type_no_check: bool = False) -> tuple[Expr, Expr]:
    if context is None:
        context = []
    if type_pool is None:
        type_pool = {}
    if def_pool is None:
        def_pool = {}
    if used_free_symbols is None:
        used_free_symbols: set[str] = set()
    if isinstance(expr, Sort):
        used_free_symbols.update(str(s) for s in expr.level.symbol.free_symbols)
        return expr, Sort(SuccLevel(expr.level))
    elif isinstance(expr, Const):
        assert expr.label in type_pool, f"Const {expr.label} is not defined."
        # 常量的类型的定义不需要考虑上下文化简, 直接返回定义的类型 
        expr_type, new_used_free_symbols = expr_rename_level(type_pool[expr.label], used_free_symbols)
        used_free_symbols.update(new_used_free_symbols)
        return expr, expr_type
    elif isinstance(expr, Arg):
        arg_type, _ = calc(expr.type, context, type_pool, def_pool, used_free_symbols)
        return Arg(arg_type, expr.name), arg_type
    elif isinstance(expr, BoundVar):
        assert expr.index < len(
            context
        ), f"Index {expr.index} out of bounds for context: {context}"
        return expr, shift_expr(context[expr.index].type, offset=0, step=expr.index+1)
    elif isinstance(expr, Forall):
        assert isinstance(expr.var_type, Arg), f"Type of variable in Forall should be Arg, but got {expr.var_type}"
        var_type, _ = calc(expr.var_type, context, type_pool, def_pool, used_free_symbols)
        assert isinstance(var_type, Arg), f"Type of variable in Forall should be Arg, but got {var_type}"
        new_context = [var_type] + context
        new_body, body_type = calc(
            expr.body, new_context, type_pool, def_pool, used_free_symbols
        )
        return_expr = Forall(var_type, new_body)
        return_type = Sort(SuccLevel(MaxLevel(get_level(var_type, context, type_pool, def_pool), get_level(new_body, new_context, type_pool, def_pool))))
        return return_expr, return_type
    elif isinstance(expr, Lambda):
        assert isinstance(expr.var_type, Arg), f"Type of variable in Lambda should be Arg, but got {expr.var_type}"
        var_type, _ = calc(expr.var_type, context, type_pool, def_pool, used_free_symbols)
        assert isinstance(var_type, Arg), f"Type of variable in Forall should be Arg, but got {var_type}"
        new_context = [var_type] + context
        new_body, body_type = calc(
            expr.body, new_context, type_pool, def_pool, used_free_symbols
        )
        return_expr = Lambda(var_type, new_body)
        return_type = Forall(var_type, body_type)
        return return_expr, return_type
    elif isinstance(expr, App):
        arg, arg_type = calc(expr.arg, context, type_pool, def_pool, used_free_symbols)
        func, func_type = calc(expr.func, context, type_pool, def_pool, used_free_symbols)
        if not isinstance(func_type, Forall):
            def_func_type = calc(expr_todef(func_type, def_pool), context, type_pool, def_pool, used_free_symbols)[0]
            if not isinstance(def_func_type, Forall):
                raise ValueError(f"Function application to a non-function: {func_type}")
            func_type = def_func_type
        if not type_no_check and not DefEq(func_type.var_type, arg_type, context, type_pool, def_pool, used_free_symbols):
            raise ValueError(f"Type mismatch: want {func_type.var_type}, get {arg_type}")
        tmp = unshift_expr(func_type.body, head=arg, offset=0)
        unshifted_funcbody_type, _ = calc(tmp, context, type_pool, def_pool, used_free_symbols)
        if isinstance(func, Lambda):
            tmp = unshift_expr(func.body, head=arg, offset=0)
            unshifted_funcbody, _ = calc(tmp, context, type_pool, def_pool, used_free_symbols)
            return unshifted_funcbody, unshifted_funcbody_type
        return App(func, arg), unshifted_funcbody_type
    else:
        raise ValueError("Unknown expr", expr)

@log_execution_time
def DefEq(target: Expr, source: Expr, context: list[Arg], type_pool: dict[str, Expr], def_pool: dict[str, Expr], used_free_symbols: set[str]=None) -> bool:
    if used_free_symbols is None:
        used_free_symbols = set()
    if target == source:
        return True
    subs_target = calc(expr_todef(target, def_pool), context, type_pool, def_pool, used_free_symbols, type_no_check=True)[0]
    subs_source = calc(expr_todef(source, def_pool), context, type_pool, def_pool, used_free_symbols, type_no_check=True)[0]
    if subs_target == subs_source:
        conditions = get_sort_eq_conditions(subs_target, subs_source)
        if is_solvable(conditions):
            return True
    return False

@log_execution_time
def shift_expr(expr: Expr, offset: int = 0, step: int = 1):
    if step == 0:
        return expr
    if isinstance(expr, Sort):
        return expr
    elif isinstance(expr, Const):
        return expr
    elif isinstance(expr, Arg):
        return Arg(shift_expr(expr.type, offset=offset, step=step), expr.name)
    elif isinstance(expr, BoundVar):
        if expr.index >= offset:
            return BoundVar(expr.index + step)
        return expr
    elif isinstance(expr, Forall):
        shifted_var_type = shift_expr(expr.var_type, offset=offset, step=step)
        shifted_body = shift_expr(expr.body, offset=offset + 1, step=step)
        return Forall(shifted_var_type, shifted_body)
    elif isinstance(expr, Lambda):
        shifted_var_type = shift_expr(expr.var_type, offset=offset, step=step)
        shifted_body = shift_expr(expr.body, offset=offset + 1, step=step)
        return Lambda(shifted_var_type, shifted_body)
    elif isinstance(expr, App):
        shifted_func = shift_expr(expr.func, offset=offset, step=step)
        shifted_arg = shift_expr(expr.arg, offset=offset, step=step)
        return App(shifted_func, shifted_arg)
    else:
        raise ValueError("Unknown expr", expr)

@log_execution_time
def unshift_expr(expr: Expr, offset: int, head: Expr):
    if isinstance(expr, Sort):
        return expr
    elif isinstance(expr, Const):
        return expr
    elif isinstance(expr, Arg):
        return Arg(unshift_expr(expr.type, offset=offset, head=head), expr.name)
    elif isinstance(expr, BoundVar):
        if expr.index >= offset:
            if expr.index == offset:
                return shift_expr(head, offset=0, step=offset)
            return BoundVar(expr.index - 1)
        return expr
    elif isinstance(expr, Forall):
        shifted_var_type = unshift_expr(expr.var_type, offset=offset, head=head)
        shifted_body = unshift_expr(expr.body, offset=offset + 1, head=head)
        return Forall(shifted_var_type, shifted_body)
    elif isinstance(expr, Lambda):
        shifted_var_type = unshift_expr(expr.var_type, offset=offset, head=head)
        shifted_body = unshift_expr(expr.body, offset=offset + 1, head=head)
        return Lambda(shifted_var_type, shifted_body)
    elif isinstance(expr, App):
        shifted_func = unshift_expr(expr.func, offset=offset, head=head)
        shifted_arg = unshift_expr(expr.arg, offset=offset, head=head)
        return App(shifted_func, shifted_arg)
    return expr

@log_execution_time
def get_level(expr: Expr, context: list[Arg], type_pool: dict[str, Expr], def_pool: dict[str, Expr]) -> Level:
    if isinstance(expr, Sort):
        result = expr.level
    elif isinstance(expr, Const):
        assert expr.label in type_pool, f"Const {expr.label} is not defined."
        expr_type = type_pool[expr.label]
        result = PreLevel(get_level(expr_type, context, type_pool, def_pool))
    elif isinstance(expr, Arg):
        result = get_level(expr.type, context, type_pool, def_pool)
    elif isinstance(expr, BoundVar):
        next_expr = context[expr.index]
        result = PreLevel(get_level(next_expr, context[expr.index+1:], type_pool, def_pool))
    elif isinstance(expr, Forall):
        left = get_level(expr.var_type, context, type_pool, def_pool)
        right = get_level(expr.body, [expr.var_type] + context, type_pool, def_pool)
        result = MaxLevel(left, right)
    elif isinstance(expr, Lambda):
        left = get_level(expr.var_type, context, type_pool)
        right = get_level(expr.body, [expr.var_type] + context, type_pool, def_pool)
        result = PreLevel(MaxLevel(left, SuccLevel(right)))
    elif isinstance(expr, App):
        _, func_type = calc(expr.func, context, type_pool, def_pool, type_no_check=True)
        assert isinstance(func_type, Forall), f"Function application to a non-function: {func_type}"
        result = PreLevel(get_level(func_type.body, [func_type.var_type] + context, type_pool, def_pool))
    else:
        raise ValueError("Unknown expr", expr)
    return result

@log_execution_time
def proof_step(action: Expr, goal: Expr, diff_context: list[Arg] = None, same_context: list[Arg] = None, type_pool:dict[str,Expr]=None, def_pool:dict[str,Expr]=None) -> list[Expr] | None:
    if diff_context is None:
        diff_context = []
    if same_context is None:
        same_context = []
    if DefEq(action, goal, diff_context + same_context, type_pool, def_pool):
        goals: list[Expr] = []
        for arg in diff_context:
            goals = [Forall(arg, goal) for goal in goals]
            goals.append(arg.type)
        for arg in same_context:
            goals = [Forall(arg, goal) for goal in goals]
        return goals
    if isinstance(action, Forall):
        if len(diff_context) == 0 and isinstance(goal, Forall) and DefEq(action.var_type, goal.var_type, diff_context + same_context, type_pool, def_pool):
            return proof_step(action.body, goal.body, diff_context, [action.var_type] + same_context, type_pool, def_pool)
        else:
            return proof_step(action.body, shift_expr(goal), [action.var_type] + diff_context, same_context, type_pool, def_pool)
    # 什么都没证明 
    return None

if __name__ == "__main__":
    Prop = Const("Prop")
    type_pool = {
        "Prop": Sort(1),
        "Iff": Forall(Prop, Forall(Prop, Prop)),
        "Iff.intro": Forall(Prop, Forall( Prop, Forall(Forall(BoundVar(1), BoundVar(1)), Forall(Forall(BoundVar(1), BoundVar(3)), App(App(Const("Iff"), BoundVar(3)), BoundVar(2))))))
    }

    Iff_intro = Const("Iff.intro")
    Iff_refl = Forall(Prop, App(App(Const("Iff"), BoundVar(0)), BoundVar(0)))
    action1 = Lambda(Prop, App(App(Iff_intro, BoundVar(0)), BoundVar(0)))
    _, action1_type = calc(action1, [], type_pool)
    goals1 = proof_step(action1_type, Iff_refl)
    print(goals1)

    action2 = Lambda(Prop, Lambda(Forall(BoundVar(0), BoundVar(1)), BoundVar(0)))
    _, action2_type = calc(action2, [], type_pool)
    goals2 = proof_step(action2_type, goals1[0])
    print(goals2)

    action3 = Lambda(Prop, Lambda(BoundVar(0), BoundVar(0)))
    _, action3_type = calc(action3, [], type_pool)
    goals3 = proof_step(action3_type, goals1[1])
    print(goals3)
