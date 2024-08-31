#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file: spi_token.py
@author: amazing coder
@date: 2024/8/29
@desc: 
"""
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
