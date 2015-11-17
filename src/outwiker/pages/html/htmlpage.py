# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.events import PAGE_UPDATE_CONTENT
from outwiker.core.config import BooleanOption
from outwiker.core.tree import WikiPage
from outwiker.core.factory import PageFactory
from outwiker.gui.hotkey import HotKey
from outwiker.pages.html.htmlpageview import HtmlPageView

from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction

_actions = [
    (HtmlAutoLineWrap, None),
    (SwitchCodeResultAction, HotKey ("F4")),
]


class HtmlWikiPage (WikiPage):
    """
    Класс HTML-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)

        self.__autoLineWrapSection = u"General"
        self.__autoLineWrapParam = u"LineWrap"


    @property
    def autoLineWrap (self):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        return option.value


    @autoLineWrap.setter
    def autoLineWrap (self, value):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        option.value = value
        self.root.onPageUpdate (self, change=PAGE_UPDATE_CONTENT)


    @staticmethod
    def getTypeString ():
        return u"html"


class HtmlPageFactory (PageFactory):
    """
    Фабрика для создания HTML-страниц и их представлений
    """
    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application), actionTuple[1]), _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId), _actions)


    def getPageType(self):
        return HtmlWikiPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"HTML Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return HtmlPageView (parent)
