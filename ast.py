#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: ast.py
@author: amazing coder
@date: 2024/8/28
@desc: abstract-syntax tree (AST) 抽象语法树节点定义
eg: 2 + 3 * 4
mul_token = Token(MUL, '*')
plus_token = Token(PLUS, '+')
node_mul = BinOp(Num(Token(INTEGER, 3)), mul_token, Num(Token(INTEGER, 4)))
node_plus = BinOp(Num(Token(INTEGER, 2), plus_token, node_mul))
"""


class  AST(object):
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
