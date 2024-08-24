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

    def expr(self):
        """Parser / Parser / Interpreter, this function takes a tokenized stream
        and produces an abstract syntax tree, or more commonly a "value"."""
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

