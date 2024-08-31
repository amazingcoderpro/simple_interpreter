#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: spi_symbol.py
@author: amazing coder
@date: 2024/8/31
@desc: 增加通用符号类
"""

class Symbol(object):
    def __int__(self, name, type=None):
        self.name = name
        self.symbol_type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__int__(self, name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, type=None):
        # python 定义时可以不指定类型
        super().__int__(name, type)

    def __str__(self):
        return f'VarSymbol:name={self.name}: type={str(self.symbol_type)}'

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self):
        self._symbols = {}

    def __str__(self):
        return 'Symbols: {symbols}'.format(symbols=[value for value in self._symbols.values()])

    __repr__ = __str__

    def define(self, symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol
        return symbol

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol


def test_class():
    int_type = BuiltinTypeSymbol('INTEGER')
    float_type = BuiltinTypeSymbol('FLOAT')
    var_x = VarSymbol('x', int_type)
    var_y = VarSymbol('y', float_type)
    print(var_x)
    print(var_y)


if __name__ == '__main__':
    test_class()