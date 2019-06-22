# -*- coding: utf-8 -*-

import idna

import wx

import outwiker.core
from outwiker.core.application import Application
from outwiker.core.events import LinkClickParams, HoverLinkParams


class HtmlRender (wx.Panel):
    """
    Базовый класс для HTML-рендеров
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Номер элемента статусной панели, куда выводится текст
        self._status_item = 0
        self._currentPage = None

    def LoadPage(self, fname):
        """
        Загрузить страницу из файла
        """
        pass

    def SetPage(self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь до папки, относительно которой будут искаться
            локальные ресурсы (картинки)
        """
        pass

    def Sleep(self):
        pass

    def Awake(self):
        pass

    @property
    def page(self):
        return self._currentPage

    @page.setter
    def page(self, value):
        self._currentPage = value

    def openUrl(self, href):
        """
        Открыть ссылку в браузере (или почтовый адрес в почтовике)
        """
        try:
            outwiker.core.system.getOS().startFile(href)
        except OSError:
            text = _(u"Can't execute file '%s'") % (href)
            outwiker.core.commands.showError(Application.mainWindow, text)

    def _getLinkProtocol(self, link):
        """
        Return protocol for link or None if link contains not protocol
        """
        if link is None:
            return None

        endProtocol = u"://"
        pos = link.find(endProtocol)
        if pos == -1:
            return None

        return link[:pos + len(endProtocol)]

    def _decodeIDNA(self, link):
        """
        Decode link like protocol://xn--80afndtacjikc
        """
        if link is None:
            return None

        protocol = self._getLinkProtocol(link)
        if protocol is not None:
            url = link[len(protocol):]
            try:
                link = u"{}{}".format(
                    protocol,
                    idna.decode(url))
            except UnicodeError:
                # Под IE ссылки не преобразуются в кодировку IDNA
                pass

        return link

    def _getClickParams(self,
                        href,
                        button,
                        modifier,
                        isurl,
                        ispage,
                        isfilename,
                        isanchor):
        linktype = None

        if isanchor:
            linktype = u"anchor"

        if isurl:
            linktype = u"url"
        elif ispage:
            linktype = u"page"
        elif isfilename:
            linktype = u"filename"

        return LinkClickParams(
            link=href,
            button=button,
            modifier=modifier,
            linktype=linktype,
        )

    def setStatusText(self, link, text):
        """
        Execute onHoverLink event and set status text
        """
        link_decoded = self._decodeIDNA(link)

        params = HoverLinkParams(link=link_decoded, text=text)
        Application.onHoverLink(page=self._currentPage, params=params)

        outwiker.core.commands.setStatusText(params.text, self._status_item)
