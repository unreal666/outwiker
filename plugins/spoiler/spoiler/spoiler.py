#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Плагин для вставки свернутого текста
# История версий
# 1.1
#    * Исправлены ошибки, связанные с отключением плагина
#    * Требуется минимальная версия OutWiker - 1.6.0.632
# 1.0
#    * Первый релиз


import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.pages.wiki.wikipanel import WikiPagePanel

from .commandspoiler import SpoilerCommand


class PluginSpoiler (Plugin):
    """
    Плагин, добавляющий обработку команды spoiler в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        # Для работы этого плагина требуется OutWiker 1.6.0.632
        if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
            raise BaseException ("OutWiker version requirement: 1.6.0.632")

        Plugin.__init__ (self, application)
        self.__maxCommandIndex = 9
        self.SPOILER_TOOL_ID = u"PLUGIN_SPOILER_TOOL_ID"


    def __onWikiParserPrepare (self, parser):
        parser.addCommand (SpoilerCommand (parser, "spoiler", _))

        for index in range (self.__maxCommandIndex + 1):
            commandname = "spoiler{index}".format (index=index)
            parser.addCommand (SpoilerCommand (parser, commandname, _) )


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    def initialize(self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self.__initlocale()

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def __initlocale (self):
        domain = u"spoiler"

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e


    @property
    def _isCurrentWikiPage (self):
        return (self._application.selectedPage != None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if not self._isCurrentWikiPage:
            return

        pageView = self.__getPageView()

        helpString = _(u"Collapse text (:spoiler:)")
        image = self.__getButtonImage ()

        pageView.addTool (pageView.commandsMenu, 
                self.SPOILER_TOOL_ID, 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                image)
        

    def __getButtonImage (self):
        imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
        fname = os.path.join (imagedir, "spoiler.png")
        return fname


    def __onInsertCommand (self, event):
        startCommand = u'(:spoiler:)\n'
        endCommand = u'\n(:spoilerend:)'

        pageView = self.__getPageView()
        pageView.codeEditor.turnText (startCommand, endCommand)


    def __getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        pageView = self._application.mainWindow.pagePanel.pageView
        assert type (pageView) == WikiPagePanel

        return pageView


    @property
    def name (self):
        return u"Spoiler"

    
    @property
    def description (self):
        return _(u"""Add command (:spoiler:) in wiki parser.

<B>Usage:</B>
<PRE>(:spoiler:)
Text
(:spoilerend:)</PRE>

For nested spoilers use (:spoiler0:), (:spoiler1:)... (:spoiler9:) commands. 

<U>Example:</U>

<PRE>(:spoiler:)
Text
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Nested spoiler
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Params:</B>
<U>expandtext</U> - Link text for the collapsed spoiler. Default: "Expand".
<U>collapsetext</U> - Link text for the expanded spoiler. Default: "Collapse".

<U>Example:</U>

<PRE>(:spoiler expandtext="More..." collapsetext="Less":)
Text
(:spoilerend:)</PRE>
""")


    @property
    def version (self):
        return u"1.1"


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий и удалить свои кнопки, пункты меню и т.п.
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate

        if self._isCurrentWikiPage:
            pageView = self.__getPageView().removeTool (self.SPOILER_TOOL_ID)

    #############################################