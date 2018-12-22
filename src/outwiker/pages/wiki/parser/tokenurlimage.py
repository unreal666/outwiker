# -*- coding: utf-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class UrlImageFactory (object):
    @staticmethod
    def make(parser):
        return UrlImageToken(parser).getToken()


class UrlImageToken (object):
    """
    Токен для ссылки на картинку
    """

    def __init__(self, parser):
        self.parser = parser

    def getToken(self):
        token = Regex(r"(https?|ftp)://[a-z0-9-]+(\.[a-z0-9-]+)+(/[-._\w%+]+)*/[-\w_.%+]+\.(gif|png|jpe?g|bmp|tiff?)",
                      re.IGNORECASE).setParseAction(lambda s, l, t: '<img src="%s"/>' % t[0])("image")
        return token
