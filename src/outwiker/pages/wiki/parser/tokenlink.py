# -*- coding: UTF-8 -*-

import cgi

from outwiker.libs.pyparsing import QuotedString

from tokenattach import AttachToken
from outwiker.core.attachment import Attachment


class LinkFactory (object):
    @staticmethod
    def make (parser):
        return LinkToken(parser).getToken()


class LinkToken (object):
    linkStart1 = "[[["
    linkEnd1 = "]]]"
    linkStart2 = "[["
    linkEnd2 = "]]"
    attachString = u"Attach:"

    def __init__ (self, parser):
        self.parser = parser


    def getToken (self):
        return (QuotedString(LinkToken.linkStart1,
                             endQuoteChar = LinkToken.linkEnd1,
                             multiline = False) |
                QuotedString(LinkToken.linkStart2,
                             endQuoteChar = LinkToken.linkEnd2,
                             multiline = False)).setParseAction(self.__convertToLink)("link")


    def __convertToLink (self, s, l, t):
        """
        Преобразовать ссылку
        """
        if "->" in t[0]:
            return self.__convertLinkArrow (t[0])
        elif "|" in t[0]:
            return self.__convertLinkLine (t[0])

        return self.__convertEmptyLink (t[0])


    def __convertLinkArrow (self, text):
        """
        Преобразовать ссылки в виде [[comment -> url]]
        """
        attrs = ''
        comment, url = text.rsplit ("->", 1)

        if "=>" in url:
            url, attrs = url.split ("=>", 1)

        realurl = self.__prepareUrl (url)

        return self.__getUrlTag (realurl, cgi.escape (comment), attrs)


    def __convertLinkLine (self, text):
        """
        Преобразовать ссылки в виде [[url | comment]]
        """
        attrs = ''
        # Т.к. символ | может быть в ссылке и в тексте,
        # считаем, что после ссылки пользователь поставит пробел
        if " |" in text:
            url, comment = text.split (" |", 1)
        else:
            url, comment = text.rsplit ("|", 1)

        if "=>" in url:
            url, attrs = url.split ("=>", 1)

        realurl = self.__prepareUrl (url)

        return self.__getUrlTag (realurl, cgi.escape (comment), attrs)


    def __prepareUrl (self, url):
        """
        Подготовить адрес для ссылки. Если ссылка - прикрепленный файл, то создать путь до него
        """
        if url.strip().startswith (AttachToken.attachString):
            return url.strip().replace (AttachToken.attachString, Attachment.attachDir + "/", 1)

        return url


    def __getUrlTag (self, url, comment, attrs = ''):
        attrs = attrs.strip()

        if attrs:
            attrs = ' ' + attrs

        return '<a href="%s"%s>%s</a>' % (url.strip(), attrs, self.parser.parseLinkMarkup (comment.strip()))


    def __convertEmptyLink (self, text):
        """
        Преобразовать ссылки в виде [[link]]
        """
        textStrip = text.strip()

        if textStrip.startswith (AttachToken.attachString):
            # Ссылка на прикрепление
            url = textStrip.replace (AttachToken.attachString, Attachment.attachDir + "/", 1)
            comment = textStrip.replace (AttachToken.attachString, "")

        elif (textStrip.startswith ("#") and
                self.parser.page is not None and
                self.parser.page[textStrip] is None):
            # Ссылка начинается на #, но сложенных страниц с таким именем нет,
            # значит это якорь
            return '<a id="%s"></a>' % (textStrip[1:])
        else:
            # Ссылка не на прикрепление
            url = text.strip()
            comment = text.strip()

        return '<a href="%s">%s</a>' % (url, cgi.escape (comment))
