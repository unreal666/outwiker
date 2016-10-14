# -*- coding: UTF-8 -*-

import os

from outwiker.core.style import Style
from outwiker.core.event import pagetype
from outwiker.gui.pagedialogpanels.appearancepanel import(AppearancePanel,
                                                          AppearanceController)
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.utilites.textfile import writeTextFile

from wikipage import WikiWikiPage, WikiPageFactory
from wikipreferences import WikiPrefGeneralPanel
from wikicolorizercontroller import WikiColorizerController


class WikiPageController(object):
    """GUI controller for wiki page"""
    def __init__(self, application):
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None
        self._colorizerController = WikiColorizerController(
            self._application,
            WikiWikiPage.getTypeString())

    def initialize(self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded
        self._colorizerController.clear()

    def _addTab(self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel(dialog.getPanelsParent())
            dialog.addPanel(self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController(
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController(self._appearanceController)

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == WikiWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController(self._appearanceController)
            params.dialog.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def __onPageDialogDestroy(self, page, params):
        self._appearancePanel = None
        self._appearanceController = None

    def __onPreferencesDialogCreate(self, dialog):
        panel = WikiPrefGeneralPanel(dialog.treeBook)
        prefPanelInfo = PreferencePanelInfo(panel, _(u"General"))

        dialog.appendPreferenceGroup(_(u'Wiki Page'), [prefPanelInfo])

    @pagetype(WikiWikiPage)
    def __onPageViewCreate(self, page):
        self._colorizerController.initialize(page)
        self._application.mainWindow.pagePanel.pageView.SetFocus()

    @pagetype(WikiWikiPage)
    def __onPageViewDestroy(self, page):
        self._colorizerController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(WikiPageFactory())

    def __onPageUpdateNeeded(self, page, params):
        if (page is None or
                page.getTypeString() != WikiWikiPage.getTypeString() or
                page.readonly):
            return

        if not params.allowCache:
            HtmlCache(page, self._application).resetHash()
        self._updatePage(page)

    def _updatePage(self, page):
        path = page.getHtmlPath()
        cache = HtmlCache(page, self._application)

        # Проверим, можно ли прочитать уже готовый HTML
        if cache.canReadFromCache() and os.path.exists(path):
            return

        style = Style()
        stylepath = style.getPageStyle(page)
        generator = HtmlGenerator(page)

        html = generator.makeHtml(stylepath)
        writeTextFile(path, html)
        cache.saveHash()
