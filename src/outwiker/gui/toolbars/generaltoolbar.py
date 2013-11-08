#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.aui

from outwiker.gui.mainid import MainId
from outwiker.core.system import getImagesDir
from .basetoolbar import BaseToolBar


class GeneralToolBar (BaseToolBar):
    def __init__ (self, parent, auiManager):
        super (GeneralToolBar, self).__init__(parent, auiManager)

        self.imagesDir = getImagesDir()

        self.AddTool(MainId.ID_NEW, 
                _(u"New…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Create new wiki…") + "  (Ctrl+N)",
                fullUpdate=False)

        self.AddTool(MainId.ID_OPEN, 
                _(u"Open…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Open wiki…") + "  (Ctrl+O)",
                fullUpdate=False)

        self.AddTool(MainId.ID_RELOAD, 
                _("Reload"), 
                wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), 
                _("Reload wiki") + "  (Ctrl+R)",
                fullUpdate=False)

        self.AddSeparator()

        self.AddTool(MainId.ID_ATTACH, 
                _(u"Attach files…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Attach files…") + "  (Ctrl+Alt+A)",
                fullUpdate=False)

        self.AddTool(MainId.ID_GLOBAL_SEARCH, 
                _(u"Global search…"), 
                wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), 
                _(u"Global search…") + "  (Ctrl+Shift+F)",
                fullUpdate=False)

        self.AddSeparator()
        self.Realize()


    def _createPane (self):
        return wx.aui.AuiPaneInfo().Name(self.name).Caption(self.caption).ToolbarPane().Top().Position(0)


    @property
    def name (self):
        return u"generalToolBar"


    @property
    def caption (self):
        return _(u"General")
