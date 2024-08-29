#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: interpreter.py
@author: amazing coder
@date: 2024/8/24
@desc: simple demo for python interpreter v2.0
v1.0 : only support single-digit integers +
v2.0 : support multi-digit integers +/-, support process whitespace
v3.0 : support to parse (recognize) and interpret arithmetic expressions that have any number of plus or minus operators in it, for example “7 - 3 + 2 - 1”.
v4.0 : support to parse and interpret arithmetic expressions with any number of multiplication and division operators in them, for example “7 * 4 / 2 * 3”
v5.0 : support to handle valid arithmetic expressions containing integers and any number of addition, subtraction, multiplication, and division operators.
v6.0 : support to evaluates arithmetic expressions that have different operators and parentheses.
v7.0 : using ASTs represent the operator-operand model of arithmetic expressions.
v8.0 : support unary operators (+, -)
v9.0 : support to handle python assignment statements.
"""

import keyword
from abs_syntax_tree import BinOp, Num, UnaryOp, Var, NoOp, Compound, Assign
from sip_token import Token


INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, REPL = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'ID', 'ASSIGN', 'REPL'
PYTHON_RESERVED_KEYWORDS = {key: Token(key, key) for key in keyword.kwlist}

class Analyzer(object):
    """Lexical analyzer 表达式的语法解析器，用于将表达式解析成token流"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        return SyntaxError("invalid syntax")

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Skip whitespace, tab, newline."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def integer(self):
        """return a multi-digit integer"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        """return a multi-digit identifier"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if result in PYTHON_RESERVED_KEYWORDS:
            return self.error()
        return Token(ID, result)

    def get_next_token(self):
        """this function breaking a sentence apart into tokens."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char.isalpha():
                return self.identifier()
            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')
            if self.current_char == '\\' and self.peek() == 'n':
                self.advance()
                self.advance()
                return Token(REPL, '\\n')

            self.error()
        return Token(EOF, None)


class Parser(object):
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.current_token = self.analyzer.get_next_token()

    def error(self):
        raise Exception('Invalid Syntax')

    def eat(self, token_type):
        """compare the current token type with the passed token type
        and if they match then "eat" the current token and assign
        the next token to the self.current_token, otherwise raise an exception."""
        if self.current_token.type == token_type:
            self.current_token = self.analyzer.get_next_token()
        else:
            self.error()

    def term(self):
        """计算乘除表达块： factor((MUL|DIV) factor)* """
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if self.current_token.type == MUL:
                self.eat(MUL)
            elif self.current_token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left=left, op=token, right=right)
        return node

    def statement(self):
        """statement : assignment_statement | empty"""
        if self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def statements(self):
        """
        statements : statement
                   | statement REPL statement_list
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == ID:
            results.append(self.statement())

        return results

    def compound_statement(self):
        """
        compound_statement : statement_list
        """
        # self.eat(REPL)
        nodes = self.statements()
        # self.eat(REPL)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def program(self):
        """program : compound_statement """
        node = self.compound_statement()
        return node

    def expr(self):
        """表达式解析：term((PLUS|MINUS) term)* .
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN | (PLUS|MINUS) factor
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if self.current_token.type == PLUS:
                self.eat(PLUS)
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def factor(self):
        """返回参与运算的数，支持整型或者带括号的表达式 INTEGER | LPAREN expr RPAREN | (PLUS|MINUS) factor | variable"""
        token = self.current_token
        if self.current_token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(op=token, expr=self.factor())
        elif self.current_token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(op=token, expr=self.factor())
        elif self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif self.current_token.type == ID:
            node = self.variable()
            return node
        else:
            self.error()

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.token.value

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_NoOp(self, node):
        pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit(self, node):
        if isinstance(node, BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, Num):
            return self.visit_Num(node)
        elif isinstance(node, UnaryOp):
            return self.visit_UnaryOp(node)
        elif isinstance(node, Var):
            return self.visit_Var(node)
        elif isinstance(node, Assign):
            return self.visit_Assign(node)
        elif isinstance(node, Compound):
            return self.visit_Compound(node)
        elif isinstance(node, NoOp):
            return self.visit_NoOp(node)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    print(f"begin parse input: {text}")
    lexer = Analyzer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()
