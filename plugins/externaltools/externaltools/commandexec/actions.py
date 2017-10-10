# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction

from externaltools.i18n import get_
from externaltools.commandexec.execdialog import ExecDialog
from externaltools.commandexec.execdialogcontroller import ExecDialogController
from externaltools.commandexec.commandparams import(
    MACROS_PAGE,
    MACROS_HTML,
    MACROS_FOLDER,
    MACROS_ATTACH,
)


class BaseHeadAction(BaseAction):
    """
    A base class for inserting commands and macros
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    def _getEditor(self):
        """
        Return pointer to editor
        """
        return self._application.mainWindow.pagePanel.pageView.codeEditor


class CommandExecAction(BaseHeadAction):
    """
    Insert (:exec:) command
    """
    stringId = u"ExternalTools_InsertCommandExec"

    @property
    def title(self):
        return _(u"Run applications (:exec:)")

    @property
    def description(self):
        return _(u"ExternalTools plugin. Insert (:exec:) command")

    def run(self, params):
        assert self._application.mainWindow is not None

        with ExecDialog(self._application.mainWindow) as dlg:
            controller = ExecDialogController(dlg, self._application)
            if controller.showDialog() == wx.ID_OK:
                begin, end = controller.getResult()
                self._getEditor().turnText(begin, end)


class MacrosPageAction(BaseHeadAction):
    """
    Insert %page% macros
    """
    stringId = u"ExternalTools_InsertMacrosPage"

    @property
    def title(self):
        return _(u"%page%. Current page. Text file")

    @property
    def description(self):
        return _(u"ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file.")

    def run(self, params):
        self._getEditor().replaceText(MACROS_PAGE)


class MacrosHtmlAction(BaseHeadAction):
    """
    Insert %html% macros
    """
    stringId = u"ExternalTools_InsertMacrosHtml"

    @property
    def title(self):
        return _(u"%html%. Current page. HTML file")

    @property
    def description(self):
        return _(u"ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file.")

    def run(self, params):
        self._getEditor().replaceText(MACROS_HTML)


class MacrosAttachAction(BaseHeadAction):
    """
    Insert %attach% macros
    """
    stringId = u"ExternalTools_InsertMacrosAttach"

    @property
    def title(self):
        return _(u"%attach%. Path to current attachments folder")

    @property
    def description(self):
        return _(u"ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder.")

    def run(self, params):
        self._getEditor().replaceText(MACROS_ATTACH)


class MacrosFolderAction(BaseHeadAction):
    """
    Insert %folder% macros
    """
    stringId = u"ExternalTools_InsertMacrosFolder"

    @property
    def title(self):
        return _(u"%folder%. Path to current page folder")

    @property
    def description(self):
        return _(u"ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder.")

    def run(self, params):
        self._getEditor().replaceText(MACROS_FOLDER)
