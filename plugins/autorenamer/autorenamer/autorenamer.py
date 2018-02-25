# -*- coding: utf-8 -*-

import wx

from outwiker.core.defines import PAGE_MODE_TEXT
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .actions import AddAutoRenameTagAction
from .preferencesPanel import PreferencesPanel
from .commands import AutoRenameTagCommand
from .renamer import Renamer

from .i18n import get_


class AutoRenamer(object):
    def __init__(self, plugin, application):
        self._application = application
        self._plugin = plugin
        self.ID_ADDAUTORENAMETAG = wx.NewId()
        self._menu = None

    def initialize(self):
        global _
        _ = get_()

        self._renamer = Renamer(self._application)

        self._application.onForceSave += self._renamer.RenamePage
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare

    def destroy(self):
        self._application.onForceSave -= self._renamer.RenamePage
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    def __onPreferencesDialogCreate(self, dialog):
        prefPanel = PreferencesPanel(dialog.treeBook, self._application.config)
        panelName = _(u"AutoRenamer [Plugin]")
        panelList = [PreferencePanelInfo(prefPanel, panelName)]
        dialog.appendPreferenceGroup(panelName, panelList)

    def __onPageViewCreate(self, page):
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self.addMenuItem()
            self._application.onPageModeChange += self._onTabChanged
            self.enableMenu()

    def __onPageViewDestroy(self, page):
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self.removeMenuItem()
            self._application.onPageModeChange -= self._onTabChanged

    def _onTabChanged(self, page, params):
        self.enableMenu()

    def __onWikiParserPrepare(self, parser):
        parser.addCommand(AutoRenameTagCommand(self._application, parser))

    def enableMenu(self):
        pageView = self._application.mainWindow.pagePanel.pageView
        enabled = (pageView.GetPageMode() == PAGE_MODE_TEXT and
                   not self._application.selectedPage.readonly)
        self._application.actionController.enableTools(
            AddAutoRenameTagAction.stringId,
            enabled)

    def addMenuItem(self):
        self._application.actionController.register(AddAutoRenameTagAction(self._application), None)
        if self._application.mainWindow is not None:
            self._menu = wx.Menu()
            self._submenuItem = self._application.mainWindow.pagePanel.pageView.toolsMenu.AppendSubMenu(self._menu, _(u"AutoRenamer"))
            self._application.actionController.appendMenuItem(AddAutoRenameTagAction.stringId, self._menu)

    def removeMenuItem(self):
        if self._application.mainWindow is not None:
            self._application.actionController.removeMenuItem(AddAutoRenameTagAction.stringId)
            self._application.mainWindow.pagePanel.pageView.toolsMenu.DestroyItem(self._submenuItem)
            self._submenuItem = None
            self._application.actionController.removeAction(AddAutoRenameTagAction.stringId)
