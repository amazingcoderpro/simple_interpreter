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
"""

INTEGER, PLUS, EOF, MINUS, MUL, DIV = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MUL', 'DIV'

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

class Interpreter(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
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
        """Lexical analyzer / scanner / tokenizer, this function breaking a sentence apart into tokens."""
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

            self.error()
        return Token(EOF, None)

    def eat(self, token_type):
        """compare the current token type with the passed token type
        and if they match then "eat" the current token and assign
        the next token to the self.current_token, otherwise raise an exception."""
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        # 目前只支持整型类型的表达式
        if self.current_token.type != INTEGER:
            self.error()
        term = self.current_token
        self.eat(INTEGER)
        return term.value

    def factor(self):
        if self.current_token.type != INTEGER:
            self.error()
        factor = self.current_token
        self.eat(INTEGER)
        return factor.value

    def expr(self):
        """Parser / Parser / Interpreter, this function takes a tokenized stream
        and produces an abstract syntax tree, or more commonly a "value"."""
        self.current_token = self.get_next_token()
        result = self.term()
        while self.current_token.type in (PLUS, MINUS, MUL, DIV):
            # 目前只能支持纯加减，或者纯乘除的表达式，加减乘除的复合运算涉及优先级问题暂不支持
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif op.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
            elif op.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif op.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

def main():
    while True:
        try:
            text = input('input a express like "1+2"(Only single digit integers are allowed in the input)> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()

