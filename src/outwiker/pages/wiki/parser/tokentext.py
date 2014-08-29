# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class TextFactory (object):
    @staticmethod
    def make (parser):
        return TextToken().getToken()


class TextToken (object):
    """
    Токен для обычного текста
    """
    def getToken (self):
        textRegex = "[\w]+"
        token = Regex (textRegex, re.UNICODE)("text")
        token.leaveWhitespace()
        return token
