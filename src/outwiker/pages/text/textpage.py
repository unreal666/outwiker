# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с текстом
"""

from outwiker.core.tree import WikiPage
from outwiker.pages.text.textpanel import TextPanel
from outwiker.core.factory import PageFactory


class TextWikiPage (WikiPage):
    """
    Класс текстовых страниц
    """
    def __init__(self, path, title, parent, readonly = False):
        WikiPage.__init__ (self, path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"text"


class TextPageFactory (PageFactory):
    """
    Фабрика для создания текстовой страницы и ее представления
    """
    def getPageType(self):
        return TextWikiPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"Text Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return TextPanel (parent)


    def getPrefPanels (self, parent):
        return []
