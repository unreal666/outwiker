# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from outwiker.libs.pyparsing import nestedExpr, originalTextFor


class TextBlockToken(object):
    """
    Класс, содержащий метод для оборачивания текста в теги текстового уровня
    """
    def __init__(self, parser):
        self.parser = parser

    def convertToHTML(self, opening, closing):
        """
        opening - открывающийся тег(и)
        closing - закрывающийся тег(и)
        """
        def conversionParseAction(s, l, t):
            return ''.join([
                opening,
                self.parser.parseTextLevelMarkup(''.join(t)),
                closing,
            ])
        return conversionParseAction


class NestedBlockBase(object, metaclass=ABCMeta):
    """
    Base class for tokens of the nested blocks.
    """
    start = None
    end = None
    start_html = None
    end_html = None
    name = None
    ignore = None
    attrs_re = None
    attrs_name = None

    def __init__(self, parser):
        self.parser = parser

    @abstractmethod
    def convertToHTML(self, opening, closing):
        pass

    def getToken(self):
        assert self.start is not None
        assert self.end is not None
        assert self.start_html is not None
        assert self.end_html is not None
        assert self.name is not None

        token = originalTextFor(nestedExpr(opener=self.start,
                                           closer=self.end,
                                           content=None,
                                           ignoreExpr=self.ignore
                                           ))
        token = token.setParseAction(self.convertToHTML(self.start_html, self.end_html))(self.name)

        return token


class SimpleNestedBlock(NestedBlockBase):
    """
    Base class to replace wiki tags to HTML tags for nested blocks.
    """
    def convertToHTML(self, opening, closing):
        """
        opening - opened HTML tag
        closing - closed HTML tag
        """
        if self.attrs_re:
            assert self.attrs_name is not None

        def conversionParseAction(s, l, t):
            text = s[t[0]:t[-1]]
            assert text.startswith(self.start)
            assert text.endswith(self.end)

            inner_text = text[len(self.start):-len(self.end)]

            if self.attrs_re:
                match = self.attrs_re.search(inner_text)
                if match:
                    attrs = ' %s' % match.groupdict()[self.attrs_name]
                    _opening = opening.format(attrs, attrs=attrs)
                    inner_text = text[match.end() - match.start():]
                else:
                    _opening = opening
            else:
                _opening = opening

            return ''.join([
                _opening,
                self.parser.parseWikiMarkup(inner_text),
                closing,
            ])
        return conversionParseAction
