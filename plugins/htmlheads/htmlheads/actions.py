# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class BaseHeadAction (BaseAction):
    """
    Базовый класс действий для вставки команд
    """
    def __init__ (self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()


    def _getEditor (self):
        """
        Возвращает указатель на редактор
        """
        return self._application.mainWindow.pagePanel.pageView.codeEditor



class TitleAction (BaseHeadAction):
    """
    Вставить команду (:title:)
    """
    stringId = u"HtmlHeads_InsertTitle"


    @property
    def title (self):
        return _(u"Title (:title ...:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:title... :) command")


    def run (self, params):
        self._getEditor().turnText (u"(:title ", u":)")



class DescriptionAction (BaseHeadAction):
    """
    Вставить команду (:description:)
    """
    stringId = u"HtmlHeads_InsertDescription"


    @property
    def title (self):
        return _(u"Description (:description ...:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:description... :) command")


    def run (self, params):
        self._getEditor().turnText (u"(:description ", u":)")



class KeywordsAction (BaseHeadAction):
    """
    Вставить команду (:keywords:)
    """
    stringId = u"HtmlHeads_InsertKeywords"


    @property
    def title (self):
        return _(u"Keywords (:keywords ...:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:keywords... :) command")


    def run (self, params):
        self._getEditor().turnText (u"(:keywords ", u":)")


class CustomHeadsAction (BaseHeadAction):
    """
    Вставить команду (:htmlhead:)
    """
    stringId = u"HtmlHeads_InsertHtmlHead"


    @property
    def title (self):
        return _(u"Custom head (:htmlhead:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:htmlhead:) command")


    def run (self, params):
        self._getEditor().turnText (u"(:htmlhead:)\n", u"\n(:htmlheadend:)")


class HtmlAttrsAction (BaseHeadAction):
    """
    Вставить команду (:keywords:)
    """
    stringId = u"HtmlHeads_InsertHtmlAttrs"


    @property
    def title (self):
        return _(u"<html> tag attributes (:htmlattrs ...:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:htmlattrs... :) command")


    def run (self, params):
        self._getEditor().turnText (u"(:htmlattrs ", u":)")
