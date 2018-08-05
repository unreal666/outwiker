# -*- coding: utf-8 -*-

import logging
import os

import wx
import wx.aui

from outwiker.actions.search import (SearchAction,
                                     SearchNextAction,
                                     SearchPrevAction,
                                     SearchAndReplaceAction)
from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.system import getImagesDir
from outwiker.core.attachment import Attachment
from outwiker.core.defines import REGISTRY_PAGE_CURSOR_POSITION
from outwiker.core.events import PageUpdateNeededParams, PageModeChangeParams
from outwiker.core.system import getOS
from outwiker.utilites.textfile import readTextFile
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW


logger = logging.getLogger('outwiker.pages.basehtmlpanel')


class BaseHtmlPanel(BaseTextPanel):
    # Номера страниц-вкладок
    CODE_PAGE_INDEX = 0
    RESULT_PAGE_INDEX = 1

    def __init__(self, parent, application):
        super().__init__(parent, application)

        # Предыдущее содержимое результирующего HTML, чтобы не переписывать
        # его каждый раз
        self._oldHtmlResult = u""

        # Страница, для которой уже есть сгенерированный HTML
        self._oldPage = None

        # Где хранить параметы текущей страницы страницы (код, просмотр и т.д.)
        self.tabParamName = u"PageIndex"

        self._statusbar_item = 0

        self.imagesDir = getImagesDir()

        self.notebook = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_BOTTOM)
        self._codeEditor = self.getTextEditor()(self.notebook)

        self.htmlWindow = getOS().getHtmlRender(self.notebook)

        self.__do_layout()

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                  self._onTabChanged,
                  self.notebook)
        self.Bind(self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)
        self._application.onPageUpdate += self._onPageUpdate

    def GetPageMode(self):
        '''
        Return the current page mode.
        '''
        if self._selectedPageIndex == self.CODE_PAGE_INDEX:
            return PAGE_MODE_TEXT
        elif self._selectedPageIndex == self.RESULT_PAGE_INDEX:
            return PAGE_MODE_PREVIEW
        assert False

    def SetPageMode(self, pagemode):
        if pagemode == PAGE_MODE_TEXT:
            self._selectedPageIndex = self.CODE_PAGE_INDEX
        elif pagemode == PAGE_MODE_PREVIEW:
            self._selectedPageIndex = self.RESULT_PAGE_INDEX
        else:
            raise ValueError()

    def Clear(self):
        self.Unbind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                    source=self.notebook,
                    handler=self._onTabChanged)
        self.Unbind(self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)
        self._application.onPageUpdate -= self._onPageUpdate

        super(BaseHtmlPanel, self).Clear()

    def SetCursorPosition(self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        self.codeEditor.SetSelection(position, position)
        self.codeEditor.ScrollLineToCursor()

    def GetCursorPosition(self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        return self.codeEditor.GetCurrentPosition()

    def GetEditor(self):
        return self._codeEditor

    @property
    def codeEditor(self):
        return self._codeEditor

    def Print(self):
        currpanel = self.notebook.GetCurrentPage()
        if currpanel is not None:
            currpanel.Print()

    def getTextEditor(self):
        pass

    @property
    def _selectedPageIndex(self):
        """
        Возвращает номер выбранной страницы (код или просмотр)
        """
        return self.notebook.GetSelection()

    @_selectedPageIndex.setter
    def _selectedPageIndex(self, index):
        """
        Устанавливает выбранную страницу (код или просмотр)
        """
        if index >= 0 and index < self.pageCount:
            self.notebook.SetSelection(index)

    @property
    def pageCount(self):
        return self.notebook.GetPageCount()

    def addPage(self, parent, title):
        self.notebook.AddPage(parent, title)

    def onPreferencesDialogClose(self, prefDialog):
        self.codeEditor.setDefaultSettings()

    def onAttachmentPaste(self, fnames):
        if self.GetPageMode() == PAGE_MODE_TEXT:
            text = self._getAttachString(fnames)
            self.codeEditor.AddText(text)
            self.codeEditor.SetFocus()

    def UpdateView(self, page):
        self.htmlWindow.page = self._currentpage

        self.codeEditor.SetReadOnly(False)
        self.codeEditor.SetText(self._currentpage.content)
        self.codeEditor.EmptyUndoBuffer()
        self.codeEditor.SetReadOnly(page.readonly)

        reg = page.root.registry.get_page_registry(page)
        try:
            cursor_position = reg.getint(REGISTRY_PAGE_CURSOR_POSITION,
                                         default=0)
            self.SetCursorPosition(cursor_position)
        except (KeyError, ValueError):
            pass

        self._updateHtmlWindow()
        tabIndex = self.loadPageTab(self._currentpage)
        if tabIndex < 0:
            tabIndex = self._getDefaultPage()

        self.codeEditor.SetFocus()
        self._selectedPageIndex = tabIndex

    def GetContentFromGui(self):
        return self.codeEditor.GetText()

    def __do_layout(self):
        self.addPage(self.codeEditor, _("HTML"))
        self.addPage(self.htmlWindow, _("Preview"))

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.Add(self.notebook, 1, wx.EXPAND, 0)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)
        self.Layout()

    def _enableActions(self, enabled):
        pass

    def _getDefaultPage(self):
        assert self._currentpage is not None

        if (len(self._currentpage.content) > 0 or
                len(Attachment(self._currentpage).attachmentFull) > 0):
            return self.RESULT_PAGE_INDEX

        return self.CODE_PAGE_INDEX

    def _onTabChanged(self, event):
        pagemode = self.GetPageMode()
        params = PageModeChangeParams(pagemode)
        self._application.onPageModeChange(self._application.selectedPage,
                                           params)

    def savePageTab(self, page):
        """
        Сохранить текущую вкладку (код, просмотр и т.п.) в настройки страницы
        """
        assert page is not None

        reg = page.root.registry.get_page_registry(page)
        try:
            reg.set(self.tabParamName, self._selectedPageIndex)
        except KeyError:
            logger.error("Can't set tab index for {}".format(page.subpath))

    def loadPageTab(self, page):
        """
        Прочитать из страницы настройки текущей вкладки (код, просмотр и т.п.)
        """
        assert page is not None

        # Get global tab option
        generalConfig = GeneralGuiConfig(self._application.config)
        generalTab = generalConfig.pageTab.value

        if generalTab == GeneralGuiConfig.PAGE_TAB_CODE:
            return self.CODE_PAGE_INDEX
        elif generalTab == GeneralGuiConfig.PAGE_TAB_RESULT:
            return self.RESULT_PAGE_INDEX

        # Get tab option from page
        reg = page.root.registry.get_page_registry(page)
        try:
            return reg.getint(self.tabParamName, default=-1)
        except (KeyError, ValueError):
            return -1

    def _onSwitchToCode(self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions(not self._application.selectedPage.readonly)
        self.checkForExternalEditAndSave()
        self._enableAllTools()
        self.codeEditor.SetFocus()

    def _onSwitchToPreview(self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self.Save()
        self._enableActions(False)
        self._enableAllTools()
        self.htmlWindow.SetFocus()
        self.htmlWindow.Update()
        self._updatePage()
        self._updateHtmlWindow()

    def _updatePage(self):
        assert self._currentpage is not None

        setStatusText(_(u"Page rendered. Please wait…"), self._statusbar_item)
        self._application.onHtmlRenderingBegin(self._currentpage,
                                               self.htmlWindow)

        self._application.onPageUpdateNeeded(self._currentpage,
                                             PageUpdateNeededParams(True))

        setStatusText(u"", self._statusbar_item)
        self._application.onHtmlRenderingEnd(self._currentpage,
                                             self.htmlWindow)

    def _updateHtmlWindow(self):
        """
        Подготовить и показать HTML текущей страницы
        """
        assert self._currentpage is not None

        setStatusText(_(u"Page loading. Please wait…"), self._statusbar_item)

        try:
            path = self._currentpage.getHtmlPath()
            if not os.path.exists(path):
                self._updatePage()

            html = readTextFile(path)

            if(self._oldPage != self._currentpage or
                    self._oldHtmlResult != html):
                self.htmlWindow.LoadPage(path)
                self._oldHtmlResult = html
                self._oldPage = self._currentpage
        except EnvironmentError as e:
            logger.error(str(e))
            MessageBox(_(u'Page loading error: {}').format(
                self._currentpage.title),
                _(u'Error'), wx.ICON_ERROR | wx.OK)

        setStatusText(u"", self._statusbar_item)

    def _enableAllTools(self):
        """
        Активировать или дезактивировать инструменты (пункты меню и кнопки)
        в зависимости от текущей выбранной вкладки
        """
        for tool in self.allTools:
            self.enableTool(tool, self._isEnabledTool(tool))

        # Отдельно проверим возможность работы поиска по странице
        # Поиск не должен работать только на странице просмотра
        searchEnabled = self.GetPageMode() != PAGE_MODE_PREVIEW

        actionController = self._application.actionController

        actionController.enableTools(SearchAction.stringId, searchEnabled)
        actionController.enableTools(SearchNextAction.stringId, searchEnabled)
        actionController.enableTools(SearchPrevAction.stringId, searchEnabled)

        actionController.enableTools(
            SearchAndReplaceAction.stringId,
            searchEnabled and not self._application.selectedPage.readonly)

        self.mainWindow.UpdateAuiManager()

    def _isEnabledTool(self, tool):
        if "notebook" not in dir(self):
            return True

        assert self.notebook is not None
        assert self._selectedPageIndex != -1

        enabled = (tool.alwaysEnabled or
                   self.GetPageMode() == PAGE_MODE_TEXT)

        return enabled

    def GetSearchPanel(self):
        if self.GetPageMode() == PAGE_MODE_TEXT:
            return self.codeEditor.searchPanel

        return None

    def switchCodeResult(self):
        """
        Переключение между кодом и результатом
        """
        if self._currentpage is None:
            return

        if self.GetPageMode() == PAGE_MODE_PREVIEW:
            self.SetPageMode(PAGE_MODE_TEXT)
        else:
            self.SetPageMode(PAGE_MODE_PREVIEW)

    def turnText(self, left, right):
        """
        Обернуть выделенный текст строками left и right.
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.turnText(
            left, right)

    def replaceText(self, text):
        """
        Заменить выделенный текст строкой text
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(
            text)

    def escapeHtml(self):
        """
        Заменить символы на их HTML-представление
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.escapeHtml()

    def _onSpellOnOff(self, event):
        self._codeEditor.setDefaultSettings()

    def SetFocus(self):
        if self.GetPageMode() == PAGE_MODE_TEXT:
            return self.codeEditor.SetFocus()
        elif self.GetPageMode() == PAGE_MODE_PREVIEW:
            return self.htmlWindow.SetFocus()

    def _onPageUpdate(self, sender, **kwargs):
        if (sender == self._currentpage and
                self.notebook.GetSelection() == self.RESULT_PAGE_INDEX):
            self._updatePage()
            self._updateHtmlWindow()
