# -*- coding: utf-8 -*-

from outwiker.libs.pyparsing import NoMatch

class TagAttrsPattern(object):
    value = r"(?:<<(?P<attributes>(?:(?!>>).)+)>>)?"
    name = "attributes"


def getAttributes(toks):
    attrs = toks[TagAttrsPattern.name]
    return ' %s' % attrs if attrs else ''


def noConvert(s, l, t):
    return t[0]


def concatenate(tokenlist):
    """
    Склеить несколько токенов из списка
    """
    if len(tokenlist) == 0:
        return NoMatch()

    result = tokenlist[0]
    for token in tokenlist[1:]:
        result |= token

    return result


def convertToHTML(opening, closing, parser):
    """
    opening - открывающийся тег(и)
    closing - закрывающийся тег(и)
    parser - парсер, у которого есть метод parseWikiMarkup()
    """
    def conversionParseAction(s, l, t):
        return opening + parser.parseWikiMarkup(t[0]) + closing
    return conversionParseAction


def returnNone(s, l, t):
    return None


def escapeTextForRE(text):
    for char in r'\^$.*+?[]{}()|#':
        text = text.replace(char, '\\' + char)
    return text
