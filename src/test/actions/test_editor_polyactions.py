# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod


from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.polyactionsid import *


class BaseEditorPolyactionsTest (BaseMainWndTest):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _createPage(self):
        pass

    @abstractmethod
    def _getEditor(self):
        pass

    def setUp(self):
        BaseMainWndTest.setUp(self)
        self.page = self._createPage()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.page

    def test_LineDuplicate_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 1\nСтрока 1\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_LineDuplicate_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = u'Строка 1\nСтрока 2\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_LineDuplicate_03(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'\n'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesDown_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesDown_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 15)

        result = u'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUp_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUp_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 21)

        result = u'Строка 2\nСтрока 3\nСтрока 1\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUpDown_empty(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u''

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'), result)

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'), result)

    def test_DeleteCurrentLine_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 2\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_DeleteCurrentLine_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 10)

        result = u'Строка 1\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_DeleteCurrentLine_03_empty(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u''

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)


class WikiEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for wiki pages
    """
    def _createPage(self):
        return WikiPageFactory().create(self.wikiroot, u"Викистраница", [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor


class HtmlEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for HTML pages
    """
    def _createPage(self):
        return HtmlPageFactory().create(self.wikiroot, u"HTML-страница", [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor


class TextEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for text pages
    """
    def _createPage(self):
        return TextPageFactory().create(self.wikiroot,
                                        u"Текстовая страница",
                                        [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.textEditor
