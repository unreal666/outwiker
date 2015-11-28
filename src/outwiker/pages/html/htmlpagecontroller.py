# -*- coding: UTF-8 -*-

from outwiker.gui.pagedialogpanels.appearancepanel import (AppearancePanel,
                                                           AppearanceController)

from htmlspellcontroller import HtmlSpellController
from htmlpage import HtmlWikiPage


class HtmlPageController (object):
    """GUI controller for HTML page"""
    def __init__(self, application):
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None
        self._spellController = HtmlSpellController (self._application)


    def initialize (self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy


    def clear (self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        self._spellController.clear()


    def _addTab (self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel (dialog.getPanelsParent())
            dialog.addPanel (self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController (
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController (self._appearanceController)


    def __onPageDialogPageTypeChanged (self, page, params):
        if params.pageType == HtmlWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController (self._appearanceController)
            params.dialog.removePanel (self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None


    def __onPageDialogDestroy (self, page, params):
        self._appearancePanel = None
        self._appearanceController = None


    def __onPageViewCreate (self, page):
        assert page is not None
        self._spellController.initialize(page)


    def __onPageViewDestroy (self, page):
        assert page is not None
        self._spellController.clear()
