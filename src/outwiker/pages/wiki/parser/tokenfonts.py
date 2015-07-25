# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import QuotedString, Regex, OneOrMore, Suppress, Combine, ZeroOrMore, NotAny, CharsNotIn

from .tokenblock import TextBlockToken
from .utils import returnNone


class FontsFactory (object):
    """
    Фабрика для создания шрифтовых / блочных токенов
    """
    @staticmethod
    def makeItalic (parser):
        """
        Создать токен для курсивного шрифта
        """
        return ItalicToken(parser).getToken()


    @staticmethod
    def makeBold (parser):
        """
        Создать токен для полужирного шрифта
        """
        return BoldToken(parser).getToken()


    @staticmethod
    def makeBoldItalic (parser):
        """
        Создать токен для полужирного курсивного шрифта
        """
        return BoldItalicToken(parser).getToken()


    @staticmethod
    def makeUnderline (parser):
        """
        Создать токен для подчеркнутого шрифта
        """
        return UnderlineToken(parser).getToken()


    @staticmethod
    def makeStrike (parser):
        """
        Создать токен для зачеркнутого шрифта
        """
        return StrikeToken(parser).getToken()


    @staticmethod
    def makeSubscript (parser):
        """
        Создать токен для нижнего индекса
        """
        return SubscriptToken(parser).getToken()


    @staticmethod
    def makeSuperscript (parser):
        """
        Создать токен для верхнего индекса
        """
        return SuperscriptToken(parser).getToken()


    @staticmethod
    def makeCode (parser):
        """
        Создать токен для кода
        """
        return CodeToken(parser).getToken()


    @staticmethod
    def makeSmall (parser):
        """
        Создать парсер для мелкого шрифта
        """
        return SmallFontToken(parser).getToken()


    @staticmethod
    def makeBig (parser):
        """
        Создать парсер для крупного шрифта
        """
        return BigFontToken(parser).getToken()



class CodeToken (TextBlockToken):
    """
    Токен для кода
    """
    start = "@@"
    end = "@@"

    def getToken (self):
        return QuotedString (CodeToken.start,
                             endQuoteChar = CodeToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<code>", "</code>"))("code")


class SuperscriptToken (TextBlockToken):
    """
    Токен для верхнего индекса
    """
    start = "'^"
    end = "^'"

    def getToken (self):
        return QuotedString (SuperscriptToken.start,
                             endQuoteChar = SuperscriptToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<sup>", "</sup>"))("superscript")


class SubscriptToken (TextBlockToken):
    """
    Токен для нижнего индекса
    """
    start = "'_"
    end = "_'"

    def getToken (self):
        return QuotedString (SubscriptToken.start,
                             endQuoteChar = SubscriptToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<sub>", "</sub>"))("subscript")


class UnderlineToken (TextBlockToken):
    """
    Токен для курсива
    """
    start = "{+"
    end = "+}"

    def getToken (self):
        return QuotedString (UnderlineToken.start,
                             endQuoteChar = UnderlineToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<u>", "</u>"))("underline")


class StrikeToken (TextBlockToken):
    """
    Токен для курсива
    """
    start = "{-"
    end = "-}"

    def getToken (self):
        return QuotedString (StrikeToken.start,
                             endQuoteChar = StrikeToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<strike>", "</strike>"))("strike")



class ItalicToken (TextBlockToken):
    """
    Токен для курсива
    """
    start = "''"
    end = "''"
    anyExcept = Combine( ZeroOrMore( NotAny (start) + CharsNotIn('', exact=1) ) )

    def getToken (self):
        if not hasattr(self.parser, 'bolded'):
            if hasattr(self.parser, 'isFakeParser'):
                self.parser.bolded = FontsFactory.makeBold (None).setParseAction(returnNone)
            else:
                self.parser.bolded = FontsFactory.makeBold (self.parser)

        return (Suppress(ItalicToken.start) + ( OneOrMore( ItalicToken.anyExcept + self.parser.bolded) +
                                                      ItalicToken.anyExcept | ItalicToken.anyExcept ) +
                Suppress(ItalicToken.end)).leaveWhitespace().setParseAction(self.convertToHTML("<i>", "</i>"))("italic")



class BoldToken (TextBlockToken):
    """
    Токен для полужирного шрифта
    """
    start = "'''"
    end = "'''"

    def getToken (self):
        return QuotedString (BoldToken.start,
                             endQuoteChar = BoldToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<b>", "</b>"))("bold")


class BoldItalicToken (TextBlockToken):
    """
    Токен для полужирного курсивного шрифта
    """
    start = "''''"
    end = "''''"

    def getToken (self):
        return QuotedString (BoldItalicToken.start,
                             endQuoteChar = BoldItalicToken.end,
                             multiline = True).setParseAction(self.convertToHTML("<b><i>", "</i></b>"))("bold_italic")


class SmallFontToken (TextBlockToken):
    """
    Токен для мелкого шрифта
    """
    def getToken (self):
        return Regex (r"\[(?P<count>-{1,4})(?P<text>.*?)\1\]",
                      re.MULTILINE | re.UNICODE | re.DOTALL).setParseAction (self.__parse)("small")


    def __parse (self, s, l, t):
        # Расчет масштаба в зависимости от количества минусов
        size = 100 - len (t["count"]) * 20

        return u'<span style="font-size:{size}%">{text}</span>'.format (size=size, text=self.parser.parseTextLevelMarkup (t["text"]))


class BigFontToken (TextBlockToken):
    """
    Токен для крупного шрифта
    """
    def getToken (self):
        return Regex (r"\[(?P<count>\+{1,5})(?P<text>.*?)\1\]",
                      re.MULTILINE | re.UNICODE | re.DOTALL).setParseAction (self.__parse)("big")


    def __parse (self, s, l, t):
        # Расчет масштаба в зависимости от количества минусов
        size = 100 + len (t["count"]) * 20

        return u'<span style="font-size:{size}%">{text}</span>'.format (
            size=size,
            text=self.parser.parseTextLevelMarkup (t["text"])
        )
