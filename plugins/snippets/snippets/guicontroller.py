# -*- coding: UTF-8 -*-

import os
from collections import namedtuple

import wx

from outwiker.core.system import getSpecialDirList
from outwiker.core.commands import MessageBox
from outwiker.utilites.textfile import readTextFile

from snippets.actions.updatemenu import UpdateMenuAction
from snippets.actions.editsnippets import EditSnippetsAction
from snippets.events import RunSnippetParams
from snippets.i18n import get_
from snippets.snippetsloader import SnippetsLoader
from snippets.gui.variablesdialog import VariablesDialogController
import snippets.defines as defines

from jinja2 import TemplateError

SnippetInfo = namedtuple('SnippetInfo', ['filename', 'menuitem', 'parentmenu'])


class GuiController(object):
    def __init__(self, application):
        self._application = application

        self._menu = None
        self._mainMenu = None

        self.MENU_POS = 6
        self._menuName = None

        self._snippets_id = {}
        self._varDialogController = VariablesDialogController(
            self._application
        )

        self._actions = [
            UpdateMenuAction,
            EditSnippetsAction,
        ]

    def initialize(self):
        global _
        _ = get_()

        if self._application.mainWindow is not None:
            self._mainMenu = self._application.mainWindow.mainMenu
            self._menuName = _(u'Snippets')
            self._createMenu()
            self._varDialogController.onFinishDialogEvent += self._onFinishDialog
            self._application.customEvents.bind(defines.EVENT_UPDATE_MENU,
                                                self._onMenuUpdate)
            self._application.customEvents.bind(defines.EVENT_RUN_SNIPPET,
                                                self._onRunSnippet)

    def _createMenu(self):
        self._menu = wx.Menu(u'')

        controller = self._application.actionController
        map(lambda action: controller.appendMenuItem(action.stringId, self._menu),
            self._actions)

        self._menu.AppendSeparator()
        self._updateMenu()
        self._mainMenu.Insert(self.MENU_POS, self._menu, self._menuName)

    def _onMenuUpdate(self, params):
        self._updateMenu()

    def _removeSnippetsFromMenu(self):
        # Remove all snippets
        for snippet_id, snippet_info in reversed(self._snippets_id.items()):
            menu_item = snippet_info.menuitem
            menu = snippet_info.parentmenu
            self._application.mainWindow.Unbind(wx.EVT_MENU,
                                                handler=self._onClick,
                                                id=snippet_id
                                                )
            menu.RemoveItem(menu_item)
            menu_item.Destroy()
            # wx.Window.UnreserveControlId(snippet_id)

        # Count menu items for snippets. (+-1 because of separator exists)
        menu_snippets_count = (self._menu.GetMenuItemCount() -
                               len(self._actions)) - 1

        for _ in range(menu_snippets_count):
            menu_item = self._menu.FindItemByPosition(len(self._actions) + 1)
            self._menu.RemoveItem(menu_item)
            menu_item.Destroy()

        self._snippets_id = {}

    def _updateMenu(self):
        self._removeSnippetsFromMenu()
        sl = SnippetsLoader(getSpecialDirList(defines.SNIPPETS_DIR)[-1])
        snippets_tree = sl.getSnippets()
        self._buildTree(snippets_tree, self._menu)

    def _buildTree(self, snippets_tree, menu):
        # Create submenus
        for subdir in sorted(snippets_tree.dirs, key=lambda x: x.name):
            submenu = wx.Menu(u'')
            self._buildTree(subdir, submenu)
            menu.AppendSubMenu(submenu, subdir.name)

        # Create menu items
        menu.AppendSeparator()
        for snippet in sorted(snippets_tree.snippets):
            name = os.path.basename(snippet)[:-len(defines.EXTENSION)]
            menu_item_id = wx.Window.NewControlId()
            menu_item = menu.Append(menu_item_id, name)

            self._snippets_id[menu_item_id] = SnippetInfo(snippet,
                                                          menu_item,
                                                          menu)

            self._application.mainWindow.Bind(
                wx.EVT_MENU,
                handler=self._onClick,
                id=menu_item_id
            )

    def _destroyMenu(self):
        index = self._mainMenu.FindMenu(self._menuName)
        assert index != wx.NOT_FOUND

        actionController = self._application.actionController

        map(lambda action: actionController.removeMenuItem(action.stringId),
            self._actions)
        self._mainMenu.Remove(index)
        self._menu = None

    def destroy(self):
        if self._application.mainWindow is not None:
            self._destroyMenu()
            self._varDialogController.onFinishDialogEvent -= self._onFinishDialog

        self._varDialogController.destroy()

    def _onRunSnippet(self, params):
        # type: (RunSnippetParams) -> None
        if self._application.selectedPage is None:
            return

        snippet_fname = params.snippet_fname
        selectedText = params.selectedText
        try:
            template = self._loadTemplate(snippet_fname)
        except EnvironmentError:
            MessageBox(
                _(u"Can't read the snippet\n{}").format(snippet_fname),
                _(u"Error"),
                wx.ICON_ERROR | wx.OK)
            return

        try:
            self._varDialogController.ShowDialog(
                selectedText,
                template,
                os.path.dirname(snippet_fname)
            )
        except TemplateError as e:
            text = _(u'Template error at line {line}:\n{text}').format(
                line=e.lineno,
                text=unicode(e.message)
            )
            MessageBox(text, _(u"Snippet error"), wx.ICON_ERROR | wx.OK)
        except EnvironmentError as e:
            text = _(u'Snippet reading error:\n{text}').format(
                text=unicode(e)
            )
            MessageBox(text, _(u"Snippet error"), wx.ICON_ERROR | wx.OK)
        except BaseException as e:
            text = _(u'Snippet processing error:\n{text}').format(
                text=unicode(e)
            )
            MessageBox(text, _(u"Snippet error"), wx.ICON_ERROR | wx.OK)

    def _onClick(self, event):
        if self._application.selectedPage is None:
            return

        assert event.GetId() in self._snippets_id
        snippet_fname = self._snippets_id[event.GetId()].filename

        editor = self._getEditor()
        if editor is not None:
            selectedText = editor.GetSelectedText()
            eventParams = RunSnippetParams(snippet_fname, selectedText)
            self._application.customEvents(defines.EVENT_RUN_SNIPPET,
                                           eventParams)

    def _loadTemplate(self, fname):
        template = readTextFile(fname)
        if template.endswith(u'\n'):
            template = template[:-1]
        return template

    def _getEditor(self):
        if self._application.selectedPage is None:
            return None
        pageView = self._application.mainWindow.pagePanel.pageView
        if 'GetEditor' in dir(pageView):
            return pageView.GetEditor()

    def _onFinishDialog(self, params):
        editor = self._getEditor()
        if editor is not None:
            editor.replaceText(params.text)
