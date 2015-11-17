# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

from outwiker.core.tree import WikiPage
from wikipageview import WikiPageView
from outwiker.core.factory import PageFactory
from outwiker.gui.hotkey import HotKey

from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.nonparsed import WikiNonParsedAction
from actions.thumb import WikiThumbAction
from actions.openhtmlcode import WikiOpenHtmlCodeAction
from actions.updatehtml import WikiUpdateHtmlAction
from actions.attachlist import WikiAttachListAction
from actions.childlist import WikiChildListAction
from actions.include import WikiIncludeAction
from actions.dates import WikiDateCreationAction, WikiDateEditionAction


_actions = [
    (WikiFontSizeBigAction, HotKey (".", ctrl=True)),
    (WikiFontSizeSmallAction, HotKey (",", ctrl=True)),
    (WikiNonParsedAction, None),
    (WikiThumbAction, HotKey ("M", ctrl=True)),
    (WikiOpenHtmlCodeAction, HotKey ("F4", shift=True)),
    (WikiUpdateHtmlAction, HotKey ("F4", ctrl=True)),
    (WikiAttachListAction, None),
    (WikiChildListAction, None),
    (WikiIncludeAction, None),
    (WikiDateCreationAction, None),
    (WikiDateEditionAction, None),
]


class WikiWikiPage (WikiPage):
    """
    Класс wiki-страниц
    """
    def __init__ (self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"wiki"


class WikiPageFactory (PageFactory):
    """
    Фабрика для создания викистраниц и их представлений
    """
    def getPageType(self):
        return WikiWikiPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Wiki Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return WikiPageView (parent)


    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с викистраницей
        """
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application),
                                                                        actionTuple[1]),
             _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId),
             _actions)
