# -*- coding: UTF-8 -*-

import traceback

from .tokenfonts import FontsFactory
from .tokennoformat import NoFormatFactory
from .tokenpreformat import PreFormatFactory
from .tokenthumbnail import ThumbnailFactory
from .tokenheading import HeadingFactory
from .tokenadhoc import AdHocFactory
from .tokenhorline import HorLineFactory
from .tokenlink import LinkFactory
from .tokenalign import AlignFactory
from .tokentable import TableFactory
from .tokenurl import UrlFactory
from .tokenurlimage import UrlImageFactory
from .tokenattach import AttachFactory, AttachImagesFactory
from .tokenlist import ListFactory
from .tokenlinebreak import LineBreakFactory
from .tokenlinejoin import LineJoinFactory
from .tokencommand import CommandFactory
from .tokentext import TextFactory
from .tokenquote import QuoteFactory
from .tokendefinitionlist import DefinitionListFactory

from ..thumbnails import Thumbnails
from outwiker.libs.pyparsing import NoMatch
from outwiker.core.system import getOS


class Parser(object):
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.error_template = u"<b>{error}</b>"

        # Dictionary with nonstandard parameters(for plugins for example)
        self.customProps = {}

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        # Массив строк-атрибутов, которые надо добавить в тег <html>
        self.__htmlAttrs = ['']

        self.__footers = []

        # Команды, которые обрабатывает парсер.
        # Формат команд:(:name params... :) content...(:nameend:)
        # Ключ - имя команды, значение - экземпляр класса команды
        self.commands = {}

        if not hasattr(self, 'italicized'): self.italicized = FontsFactory.makeItalic(self)
        if not hasattr(self, 'bolded'): self.bolded = FontsFactory.makeBold(self)
        if not hasattr(self, 'boldItalicized'): self.boldItalicized = FontsFactory.makeBoldItalic(self)
        if not hasattr(self, 'underlined'): self.underlined = FontsFactory.makeUnderline(self)
        if not hasattr(self, 'strike'): self.strike = FontsFactory.makeStrike(self)
        if not hasattr(self, 'subscript'): self.subscript = FontsFactory.makeSubscript(self)
        if not hasattr(self, 'superscript'): self.superscript = FontsFactory.makeSuperscript(self)
        if not hasattr(self, 'quote'): self.quote = QuoteFactory.make(self)
        if not hasattr(self, 'code'): self.code = FontsFactory.makeCode(self)
        if not hasattr(self, 'mark'): self.mark = FontsFactory.makeMark(self)
        if not hasattr(self, 'small'): self.small = FontsFactory.makeSmall(self)
        if not hasattr(self, 'big'): self.big = FontsFactory.makeBig(self)
        if not hasattr(self, 'headings'): self.headings = HeadingFactory.make(self)
        if not hasattr(self, 'thumb'): self.thumb = ThumbnailFactory.make(self)
        if not hasattr(self, 'noformat'): self.noformat = NoFormatFactory.make(self)
        if not hasattr(self, 'preformat'): self.preformat = PreFormatFactory.make(self)
        if not hasattr(self, 'horline'): self.horline = HorLineFactory.make(self)
        if not hasattr(self, 'link'): self.link = LinkFactory.make(self)
        if not hasattr(self, 'align'): self.align = AlignFactory.make(self)
        if not hasattr(self, 'table'): self.table = TableFactory.make(self)
        if not hasattr(self, 'url'): self.url = UrlFactory.make(self)
        if not hasattr(self, 'urlImage'): self.urlImage = UrlImageFactory.make(self)
        if not hasattr(self, 'attaches'): self.attaches = AttachFactory.make(self)
        if not hasattr(self, 'attachImages'): self.attachImages = AttachImagesFactory.make(self)
        if not hasattr(self, 'adhoctokens'): self.adhoctokens = AdHocFactory.make(self)
        if not hasattr(self, 'lists'): self.lists = ListFactory.make(self)
        if not hasattr(self, 'definitionList'): self.definitionList = DefinitionListFactory.make(self)
        if not hasattr(self, 'lineBreak'): self.lineBreak = LineBreakFactory.make(self)
        if not hasattr(self, 'lineJoin'): self.lineJoin = LineJoinFactory.make(self)
        if not hasattr(self, 'command'): self.command = CommandFactory.make(self)
        if not hasattr(self, 'text'): self.text = TextFactory.make(self)

        # Common wiki tokens
        self.wikiTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.quote,
            self.preformat,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.lists,
            self.definitionList,
            self.table,
            self.headings,
            self.command,
        ]

        # Tokens for using inside links
        self.linkTokens = [
            self.attachImages,
            self.urlImage,
            self.text,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.underlined,
            self.code,
            self.small,
            self.big,
            self.mark,
            self.strike,
            self.command,
            self.lineBreak,
            self.lineJoin,
            self.noformat,
        ]

        # Tokens for using inside headings
        self.headingTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.small,
            self.big,
            self.mark,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.command,
        ]

        # Tokens for using inside text
        self.textLevelTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.command,
        ]

        # Tokens for using inside list items(bullets and numeric)
        self.listItemsTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.preformat,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.subscript,
            self.superscript,
            self.quote,
            self.definitionList,
            self.attaches,
            self.command,
        ]

        self._wikiMarkup = None
        self._listItemMarkup = None
        self._linkMarkup = None
        self._headingMarkup = None
        self._textLevelMarkup = None

    def _createMarkup(self, tokensList):
        markup = NoMatch()
        for token in tokensList:
            markup |= token

        return markup

    @property
    def head(self):
        """
        Свойство возвращает строку из добавленных заголовочных элементов
       (то, что должно быть внутри тега <head>...</head>)
        """
        return u"\n".join(self.__headers)

    def appendToHead(self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append(header)

    @property
    def headItems(self):
        '''
        Return list of the strings for the <head> HTML tag.

        Added in outwiker.core 1.3
        '''
        return self.__headers

    @property
    def footer(self):
        '''
        Added in outwiker.core 1.3
        '''
        return u''.join(self.__footers)

    @property
    def footerItems(self):
        '''
        Added in outwiker.core 1.3
        '''
        return self.__footers

    def appendToFooter(self, footer):
        """
        Added in outwiker.core 1.3
        """
        self.__footers.append(footer)

    @property
    def htmlAttrs(self):
        """
        Свойство возвращает строку из добавленных атрибутов для тега <html>
        """
        return u" ".join(self.__htmlAttrs)

    def appendToHtmlTag(self, attr):
        """
        Добавить строку-атрибуты в тег <html>
        """
        self.__htmlAttrs.append(attr)

    def toHtml(self, text):
        """
        Сгенерить HTML без заголовков типа <HTML> и т.п.
        """
        thumb = Thumbnails(self.page)
        thumb.clearDir()

        return self.parseWikiMarkup(text)

    def parseWikiMarkup(self, text):
        if self._wikiMarkup is None:
            self._wikiMarkup = self._createMarkup(self.wikiTokens)

        try:
            return self._wikiMarkup.transformString(text)
        except Exception:
            error = unicode(traceback.format_exc(), getOS().filesEncoding)
            return self.error_template.format(error=error)

    def parseListItemMarkup(self, text):
        if self._listItemMarkup is None:
            self._listItemMarkup = self._createMarkup(self.listItemsTokens)

        try:
            return self._listItemMarkup.transformString(text)
        except Exception:
            error = unicode(traceback.format_exc(), getOS().filesEncoding)
            return self.error_template.format(error=error)

    def parseLinkMarkup(self, text):
        if self._linkMarkup is None:
            self._linkMarkup = self._createMarkup(self.linkTokens)

        try:
            return self._linkMarkup.transformString(text)
        except Exception:
            error = unicode(traceback.format_exc(), getOS().filesEncoding)
            return self.error_template.format(error=error)

    def parseHeadingMarkup(self, text):
        if self._headingMarkup is None:
            self._headingMarkup = self._createMarkup(self.headingTokens)

        try:
            return self._headingMarkup.transformString(text)
        except Exception:
            error = unicode(traceback.format_exc(), getOS().filesEncoding)
            return self.error_template.format(error=error)

    def parseTextLevelMarkup(self, text):
        if self._textLevelMarkup is None:
            self._textLevelMarkup = self._createMarkup(self.textLevelTokens)

        try:
            return self._textLevelMarkup.transformString(text)
        except Exception:
            error = unicode(traceback.format_exc(), getOS().filesEncoding)
            return self.error_template.format(error=error)

    def addCommand(self, command):
        self.commands[command.name] = command

    def removeCommand(self, commandName):
        if commandName in self.commands:
            del self.commands[commandName]
