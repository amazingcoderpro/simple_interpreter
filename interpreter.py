#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: interpreter.py
@author: amazing coder
@date: 2024/8/24
@desc: simple demo for python interpreter v2.0
v1.0 : only support single-digit integers +
v2.0 : support multi-digit integers +/-, support process whitespace
"""

INTEGER, PLUS, EOF, MINUS = 'INTEGER', 'PLUS', 'EOF', 'MINUS'

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

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]
        self.pos += 1

        if current_char.isdigit():
            while self.pos < len(text) and text[self.pos].isdigit():
                current_char += text[self.pos]
                self.pos += 1
            return Token(INTEGER, int(current_char))
        if current_char == '+':
            return Token(PLUS, current_char)
        if current_char == '-':
            return Token(MINUS, current_char)
        if current_char == ' ':
            return self.get_next_token()
        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            op_str = '+'
            self.eat(PLUS)
        elif op.type == MINUS:
            op_str = '-'
            self.eat(MINUS)
        else:
            self.error()

        right = self.current_token
        self.eat(INTEGER)

        result = ' '.join([str(left.value), op_str, str(right.value)])

        return eval(result)

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

