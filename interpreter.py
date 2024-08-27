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
"""

INTEGER, PLUS, EOF, MINUS, MUL, DIV, LPAREN, RPAREN = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
         return self.__str__()

class Analyzer(object):
    """Lexical analyzer 表达式的语法解析器，用于将表达式解析成token流"""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        return Exception("Invalid input")

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Skip whitespace, tab, newline."""
        while self.current_char is not None and self.current_char == ' ':
            self.advance()

    def integer(self):
        """return a multi-digit integer"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

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

            self.error()
        return Token(EOF, None)


class Interpreter(object):
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
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif self.current_token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    def factor(self):
        """返回参与运算的数，支持整型或者带括号的表达式"""
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
            self.error()

    def expr(self):
        """表达式解析：term((PLUS|MINUS) term)* .
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        result = self.term()
        while self.current_token.type in (PLUS, MINUS, MUL, DIV):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result


def main():
    while True:
        try:
            text = input('input a express like "10+2*3+16/(4+4)-(3-2)*2"(Only single digit integers are allowed in the input)> ')
        except EOFError:
            break

        if not text:
            continue
        analyzer = Analyzer(text)
        interpreter = Interpreter(analyzer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()

