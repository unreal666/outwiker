# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx
import wx.lib.newevent

from outwiker.actions.search import (SearchAction,
                                     SearchNextAction,
                                     SearchPrevAction,
                                     SearchAndReplaceAction)
from outwiker.actions.polyactionsid import (SPELL_ON_OFF_ID,
                                            LINE_DUPLICATE_ID,
                                            MOVE_SELECTED_LINES_UP_ID,
                                            MOVE_SELECTED_LINES_DOWN_ID,
                                            DELETE_CURRENT_LINE_ID,
                                            JOIN_LINES_STR_ID,
                                            DELETE_WORD_LEFT_STR_ID,
                                            DELETE_WORD_RIGHT_STR_ID,
                                            DELETE_LINE_LEFT_STR_ID,
                                            DELETE_LINE_RIGHT_STR_ID)
from outwiker.core.system import getImagesDir
from outwiker.core.commands import MessageBox, pageExists
from outwiker.core.attachment import Attachment
from outwiker.core.config import IntegerOption
from outwiker.core.tree import RootWikiPage
from outwiker.gui.basepagepanel import BasePagePanel
from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.gui.guiconfig import EditorConfig


class BaseTextPanel(BasePagePanel):
    """
    Базовый класс для представления текстовых страниц и им подобных
   (где есть текстовый редактор)
    """
    __metaclass__ = ABCMeta

    def __init__(self, parent, application):
        super(BaseTextPanel, self).__init__(parent, application)

        self._baseTextPolyactions = [
            SPELL_ON_OFF_ID,
            LINE_DUPLICATE_ID,
            MOVE_SELECTED_LINES_UP_ID,
            MOVE_SELECTED_LINES_DOWN_ID,
            DELETE_CURRENT_LINE_ID,
            JOIN_LINES_STR_ID,
            DELETE_WORD_LEFT_STR_ID,
            DELETE_WORD_RIGHT_STR_ID,
            DELETE_LINE_LEFT_STR_ID,
            DELETE_LINE_RIGHT_STR_ID,
        ]

        self.searchMenu = None

        # Предыдущее сохраненное состояние.
        # Используется для выявления изменения страницы внешними средствами
        self._oldContent = None

        # Диалог, который показывается, если страница изменена
        # сторонними программами.
        # Используется для проверки того, что диалог уже показан и
        # еще раз его показывать не надо
        self.externalEditDialog = None

        self.searchMenuIndex = 2
        self.imagesDir = getImagesDir()

        self._spellOnOffEvent, self.EVT_SPELL_ON_OFF = wx.lib.newevent.NewEvent()

        self._addSearchTools()
        self._addSpellTools()
        self._addEditTools()

        self._application.onAttachmentPaste += self.onAttachmentPaste
        self._application.onPreferencesDialogClose += self.onPreferencesDialogClose

        self._onSetPage += self.__onSetPage

    @abstractmethod
    def GetContentFromGui(self):
        """
        Получить из интерфейса контент, который будет сохранен в файл
        __page.text
        """
        pass

    @abstractmethod
    def GetSearchPanel(self):
        """
        Вернуть панель поиска
        """
        pass

    @abstractmethod
    def SetCursorPosition(self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        pass

    @abstractmethod
    def GetCursorPosition(self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        pass

    @abstractmethod
    def GetEditor(self):
        """
        Return text editor from panel. It used for common polyactions.
        """
        pass

    def __onSetPage(self, page):
        self.__updateOldContent()

    def __updateOldContent(self):
        self._oldContent = self.page.content

    def onPreferencesDialogClose(self, prefDialog):
        pass

    def Save(self):
        """
        Сохранить страницу
        """
        if self.page is None:
            return

        if not pageExists(self.page):
            return

        if not self.page.isRemoved:
            self.checkForExternalEditAndSave()

    def checkForExternalEditAndSave(self):
        """
        Проверить, что страница не изменена внешними средствами
        """
        if(self._oldContent is not None and
                self._oldContent != self.page.content):
            # Старое содержимое не совпадает с содержимым страницы.
            # Значит содержимое страницы кто-то изменил
            self.__externalEdit()
        else:
            self._savePageContent(self.page)
            self.__updateOldContent()

    def __externalEdit(self):
        """
        Спросить у пользователя, что делать, если страница изменилась
        внешними средствами
        """
        if self.externalEditDialog is None:
            result = self.__showExternalEditDialog()

            if result == 0:
                # Перезаписать
                self._savePageContent(self.page)
                self.__updateOldContent()
            elif result == 1:
                # Перезагрузить
                self.__updateOldContent()
                self.UpdateView(self.page)

    def __showExternalEditDialog(self):
        """
        Показать диалог о том, что страница изменена сторонними программами и
        вернуть результат диалога:
            0 - перезаписать
            1 - перезагрузить
            2 - ничего не делать
        """
        buttons = [_(u"Overwrite"), _("Load"), _("Cancel")]

        message = _(u'Page "%s" is changed by the external program') % self.page.title
        self.externalEditDialog = ButtonsDialog(self,
                                                message,
                                                _(u"Owerwrite?"),
                                                buttons,
                                                default=0,
                                                cancel=2)

        result = self.externalEditDialog.ShowModal()
        self.externalEditDialog.Destroy()
        self.externalEditDialog = None

        return result

    def __stringsAreEqual(self, str1, str2):
        """
        Сравнение двух строк
        """
        return str1.replace("\r\n", "\n") == str2.replace("\r\n", "\n")

    def _savePageContent(self, page):
        """
        Сохранение содержимого страницы
        """
        if(page is None or page.isRemoved or page.readonly):
            return

        try:
            self._getCursorPositionOption(page).value = self.GetCursorPosition()
        except IOError as e:
            MessageBox(_(u"Can't save file %s") % (unicode(e.filename)),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)
            return

        if self.__stringsAreEqual(page.content, self.GetContentFromGui()):
            return

        try:
            page.content = self.GetContentFromGui()
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox(_(u"Can't save file %s") % (unicode(e.filename)),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)

    def _getCursorPositionOption(self, page):
        section = RootWikiPage.sectionGeneral
        cursor_section = u"CursorPosition"
        default = 0

        return IntegerOption(page.params,
                             section,
                             cursor_section,
                             default)

    def _getAttachString(self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при
        вставке выбранных прикрепленных файлов из панели вложений
        """
        text = ""
        count = len(fnames)

        for n in range(count):
            text += Attachment.attachDir + "/" + fnames[n]
            if n != count - 1:
                text += "\n"

        return text

    def Clear(self):
        """
        Убрать за собой
        """

        actionController = self._application.actionController
        map(lambda item: actionController.getAction(item).setFunc(None),
            self._baseTextPolyactions)

        self._application.onAttachmentPaste -= self.onAttachmentPaste
        self._application.onPreferencesDialogClose -= self.onPreferencesDialogClose
        self._onSetPage -= self.__onSetPage

        self.removeGui()
        super(BaseTextPanel, self).Clear()

    def removeGui(self):
        """
        Убрать за собой элементы управления
        """
        assert self.mainWindow is not None
        assert self.mainWindow.mainMenu.GetMenuCount() >= 3
        assert self.searchMenu is not None

        actionController = self._application.actionController
        map(lambda item: actionController.removeMenuItem(item),
            self._baseTextPolyactions)

        actionController.removeMenuItem(SearchAction.stringId)
        actionController.removeMenuItem(SearchAndReplaceAction.stringId)
        actionController.removeMenuItem(SearchNextAction.stringId)
        actionController.removeMenuItem(SearchPrevAction.stringId)

        if self.mainWindow.GENERAL_TOOLBAR_STR in self.mainWindow.toolbars:
            actionController.removeToolbarButton(SearchAction.stringId)
            actionController.removeToolbarButton(SearchAndReplaceAction.stringId)
            actionController.removeToolbarButton(SearchNextAction.stringId)
            actionController.removeToolbarButton(SearchPrevAction.stringId)
            actionController.removeToolbarButton(SPELL_ON_OFF_ID)

        self._removeAllTools()
        self.mainWindow.mainMenu.Remove(self.searchMenuIndex)
        self.searchMenu = None

    def onAttachmentPaste (self, fnames):
        """
        Пользователь хочет вставить ссылки на приаттаченные файлы
        """
        pass

    def _addSearchTools(self):
        assert self.mainWindow is not None
        self.searchMenu = wx.Menu()
        self.mainWindow.mainMenu.Insert(self.searchMenuIndex, self.searchMenu, _("Search"))

        toolbar = self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR]

        # Начать поиск на странице
        self._application.actionController.appendMenuItem(SearchAction.stringId, self.searchMenu)
        self._application.actionController.appendToolbarButton(SearchAction.stringId,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "local_search.png"),
                                                               fullUpdate=False)

        # Начать поиск и замену на странице
        self._application.actionController.appendMenuItem(SearchAndReplaceAction.stringId, self.searchMenu)
        self._application.actionController.appendToolbarButton(SearchAndReplaceAction.stringId,
                                                               toolbar,
                                                               os.path.join(self.imagesDir, "local_replace.png"),
                                                               fullUpdate=False)

        # Продолжить поиск вперед на странице
        self._application.actionController.appendMenuItem(SearchNextAction.stringId, self.searchMenu)

        # Продолжить поиск назад на странице
        self._application.actionController.appendMenuItem(SearchPrevAction.stringId, self.searchMenu)

    def _addSpellTools(self):
        generalToolbar = self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR]
        self._application.actionController.getAction(SPELL_ON_OFF_ID).setFunc(self._spellOnOff)

        self._application.actionController.appendMenuCheckItem(
            SPELL_ON_OFF_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        self._application.actionController.appendToolbarCheckButton(
            SPELL_ON_OFF_ID,
            generalToolbar,
            os.path.join(self.imagesDir, "spellcheck.png"),
            fullUpdate=False
        )

        enableSpell = EditorConfig(self._application.config).spellEnabled.value
        self._application.actionController.check(SPELL_ON_OFF_ID, enableSpell)

    def _addEditTools(self):
        self._application.mainWindow.mainMenu.editMenu.AppendSeparator()

        # Delete the current line line
        self._application.actionController.getAction(DELETE_CURRENT_LINE_ID).setFunc(lambda params: self.GetEditor().LineDelete())

        self._application.actionController.appendMenuItem(
            DELETE_CURRENT_LINE_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Duplicate the current line
        self._application.actionController.getAction(LINE_DUPLICATE_ID).setFunc(lambda params: self.GetEditor().LineDuplicate())

        self._application.actionController.appendMenuItem(
            LINE_DUPLICATE_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Move selected lines up
        self._application.actionController.getAction(MOVE_SELECTED_LINES_UP_ID).setFunc(lambda params: self.GetEditor().MoveSelectedLinesUp())

        self._application.actionController.appendMenuItem(
            MOVE_SELECTED_LINES_UP_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Move selected lines down
        self._application.actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).setFunc(lambda params: self.GetEditor().MoveSelectedLinesDown())

        self._application.actionController.appendMenuItem(
            MOVE_SELECTED_LINES_DOWN_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Join Lines
        self._application.actionController.getAction(JOIN_LINES_STR_ID).setFunc(lambda params: self.GetEditor().JoinLines())

        self._application.actionController.appendMenuItem(
            JOIN_LINES_STR_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Delete word left
        self._application.actionController.getAction(DELETE_WORD_LEFT_STR_ID).setFunc(lambda params: self.GetEditor().DelWordLeft())

        self._application.actionController.appendMenuItem(
            DELETE_WORD_LEFT_STR_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Delete word right
        self._application.actionController.getAction(DELETE_WORD_RIGHT_STR_ID).setFunc(lambda params: self.GetEditor().DelWordRight())

        self._application.actionController.appendMenuItem(
            DELETE_WORD_RIGHT_STR_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Delete line to start
        self._application.actionController.getAction(DELETE_LINE_LEFT_STR_ID).setFunc(lambda params: self.GetEditor().DelLineLeft())

        self._application.actionController.appendMenuItem(
            DELETE_LINE_LEFT_STR_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Delete line to end
        self._application.actionController.getAction(DELETE_LINE_RIGHT_STR_ID).setFunc(lambda params: self.GetEditor().DelLineRight())

        self._application.actionController.appendMenuItem(
            DELETE_LINE_RIGHT_STR_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

    def _spellOnOff(self, checked):
        EditorConfig(self._application.config).spellEnabled.value = checked
        event = self._spellOnOffEvent(checked=checked)
        wx.PostEvent(self, event)
