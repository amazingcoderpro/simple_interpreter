#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: abs_syntax_tree.py
@author: amazing coder
@date: 2024/8/28
@desc: abstract-syntax tree (AST) 抽象语法树节点定义
eg: 2 + 3 * 4
mul_token = Token(MUL, '*')
plus_token = Token(PLUS, '+')
node_mul = BinOp(Num(Token(INTEGER, 3)), mul_token, Num(Token(INTEGER, 4)))
node_plus = BinOp(Num(Token(INTEGER, 2), plus_token, node_mul))
"""


class AST(object):
    """
    ASTs represent the operator-operand model.
    每一个 AST 节点都代表一个运算符和一个操作数
    """
    def __init__(self):
        pass


class BinOp(AST):
    """
    二元运算符节点，也是非叶子节点，代表一个二元运算符
    比如 2 + 3 这个表达式，2 和 3 都是叶子节点，+ 是二元运算符节点
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    """
    数字节点, 也是叶子节点，代表一个数字
    """
    def __init__(self, token):
         self.token = token
         self.value = token.value


class UnaryOp(AST):
    """
    一元运算符节点，也是非叶子节点，代表一个一元运算符
    比如 -2 这个表达式，- 是一元运算符节点，2 是叶子节点
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Assign(AST):
    """
    赋值运算符节点，也是非叶子节点，代表一个赋值运算符
    比如 a = 2 这个表达式，a 是变量，2是值， 都是叶子节点，= 是赋值运算符节点
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """
    变量节点，也是叶子节点，代表一个变量
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Compound(AST):
    def __init__(self):
        self.children = []