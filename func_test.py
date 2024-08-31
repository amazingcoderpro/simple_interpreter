#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: func_test.py
@author: amazing coder
@date: 2024/8/29
@desc: 
"""
from spi_token import Token
from abs_syntax_tree import Num, BinOp, UnaryOp
from interpreter import Analyzer, Parser, Interpreter, INTEGER, MINUS

def test_unary_op():
    """
    测试一元运算符, text=6---1
    """
    text = '5---2'
    six_tok = Num(Token(INTEGER, 5))
    one_tok =  Num(Token(INTEGER, 2))
    minus_tok = Token(MINUS, '-')
    exp_node = BinOp(six_tok, minus_tok, UnaryOp(minus_tok, UnaryOp(minus_tok, one_tok)))
    interpreter = Interpreter(None)
    print(interpreter.visit(exp_node))

def test_analyzer():
    """
    测试语法分析器
    """
    text = "a=45"
    print(text)
    analyzer = Analyzer(text)
    token = analyzer.get_next_token()
    while token.symbol_type != 'EOF':
        print(token)
        token = analyzer.get_next_token()

def test_interpret_py_statements():
    """
    测试解释器
    """
    text = """a=1
    b=2
    c=a+b
    d=a+b+c
    e=45
    """
    print(text)
    print(repr(text))
    analyzer = Analyzer(text)
    parser = Parser(analyzer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)



if __name__ == '__main__':
    test_interpret_py_statements()