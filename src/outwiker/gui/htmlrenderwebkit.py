# -*- coding: UTF-8 -*-

import os
import urllib

import wx

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_KEY_ANCHOR
from outwiker.gui.htmlcontrollerwebkit import UriIdentifierWebKit
from outwiker.gui.defines import (ID_MOUSE_LEFT,
                                  ID_MOUSE_MIDDLE,
                                  ID_MOUSE_RIGHT,
                                  ID_KEY_CTRL,
                                  ID_KEY_SHIFT)

'''
As far as I know (I may be wrong), a wx.Panel is "composed" by a GtkPizza
as a child of GtkScrolledWindow. GtkPizza is a custom widget created for
wxGTK.

WebKitGTK+ - the webkit port for GTK+ that has python bindings - wants a
GtkScrolledWindow as parent.

So all we need to embed webkit in wxGTK is find the wx.Panel's
GtkScrolledWindow.
This is acomplished using pygtk that is present in major distro's by
default, at least those that use gnome as its main desktop environment.

A last note is that for get a handle of a window in X, the window must be
"realized" first, in other words, must already exists. So we must Show
the wx.Frame before use this WKHtmlWindow class.

'''

from .htmlrender import HtmlRender


class HtmlRenderWebKit(HtmlRender):
    def __init__(self, parent):
        HtmlRender.__init__(self, parent)

        import wx.html2 as webview
        self.ctrl = webview.WebView.New(self)

        sizer = wx.FlexGridSizer (1)
        sizer.AddGrowableCol (0)
        sizer.AddGrowableRow (0)
        sizer.Add (self.ctrl, 0, wx.EXPAND)
        self.SetSizer (sizer)

        self.canOpenUrl = False                # Можно ли открывать ссылки

        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id=wx.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id=wx.ID_CUT)
        self.Bind (webview.EVT_WEBVIEW_NAVIGATING, self.__onNavigate)

        self._path = None

    def Print (self):
        self.ctrl.Print()

    def LoadPage (self, fname):
        url = u'file://' + fname
        if APP_DATA_KEY_ANCHOR in Application.sharedData:
            url += Application.sharedData[APP_DATA_KEY_ANCHOR]
            del Application.sharedData[APP_DATA_KEY_ANCHOR]

        self.canOpenUrl = True

        try:
            with open (fname) as fp:
                text = fp.read()
        except IOError:
            text = _(u"Can't read file %s") % (fname)
            self.SetPage (text, os.path.dirname (fname))

        self.ctrl.LoadURL(url)
        self.canOpenUrl = False

    def SetPage (self, htmltext, basepath):
        self.canOpenUrl = True
        self._path = "file://" + urllib.quote (basepath.encode ("utf8")) + "/"

        self.ctrl.SetPage (htmltext, self._path)

        self.canOpenUrl = False

    def __onCopyFromHtml(self, event):
        self.ctrl.Copy()
        event.Skip()

    def __identifyUri (self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename, anchor)
        """
        uri = self.ctrl.GetCurrentURL()

        if uri is not None:
            basepath = urllib.unquote (uri.encode('ascii')).decode ('utf8')
            identifier = UriIdentifierWebKit (self._currentPage, basepath)

            return identifier.identify (href)

        return (None, None, None, None)


    def __onNavigate(self, event):
        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        frame = event.GetTarget()
        if len(frame) != 0:
            return

        href = event.GetURL()
        curr_href = self.ctrl.GetCurrentURL()

        if not(self.canOpenUrl or href == curr_href):
            button = 1
            modifier = 0
            if self.__onLinkClicked (href, button, modifier):
                event.Veto()


    def __gtk2OutWikerKeyCode (self, gtk_key_modifier):
        """
        Convert from GTK key modifier to const from gui.defines
        """
        # Consts in GTK
        gtk_shift_key = 1
        gtk_ctrl_key = 4

        modifier = 0
        if gtk_key_modifier & gtk_shift_key:
            modifier |= ID_KEY_SHIFT

        if gtk_key_modifier & gtk_ctrl_key:
            modifier |= ID_KEY_CTRL

        return modifier


    def __gtk2OutWikerMouseButtonCode (self, gtk_mouse_button):
        """
        Convert from GTK mouse key modifier to const from gui.defines
        """
        # Consts in GTK
        gtk_left_button = 1
        gtk_middle_button = 2
        gtk_right_button = 3

        mouse_button = -1

        if gtk_mouse_button == gtk_left_button:
            mouse_button = ID_MOUSE_LEFT
        elif gtk_mouse_button == gtk_middle_button:
            mouse_button = ID_MOUSE_MIDDLE
        elif gtk_middle_button == gtk_right_button:
            mouse_button = ID_MOUSE_RIGHT

        return mouse_button


    def __onLinkClicked (self, href, gtk_mouse_button, gtk_key_modifier):
        """
        Клик по ссылке
        Возвращает False, если обрабатывать ссылку разрешить компоненту,
        в противном случае - True (если обрабатываем сами)
        href - ссылка
        gtk_mouse_button - кнопка мыши, с помощью которой кликнули по ссылке
        (1 - левая, 2 - средняя, 3 - правая, -1 - не известно)
        gtk_key_modifier - зажатые клавиши (1 - Shift, 4 - Ctrl)
        """
        source_href = href
        href = urllib.unquote (href.encode('ascii')).decode ('utf8')
        href = self._decodeIDNA (href)

        (url, page, filename, anchor) = self.__identifyUri (href)

        modifier = self.__gtk2OutWikerKeyCode (gtk_key_modifier)
        mouse_button = self.__gtk2OutWikerMouseButtonCode (gtk_mouse_button)

        params = self._getClickParams (source_href.encode('ascii'),
                                       mouse_button,
                                       modifier,
                                       url,
                                       page,
                                       filename,
                                       anchor)

        Application.onLinkClick (self._currentPage, params)
        if params.process:
            return True

        if url is not None:
            self.openUrl (url)
        elif (page is not None and
              (mouse_button == ID_MOUSE_MIDDLE or modifier == ID_KEY_CTRL)):
            Application.mainWindow.tabsController.openInTab (page, True)
        elif page is not None:
            if anchor is not None:
                Application.sharedData[APP_DATA_KEY_ANCHOR] = anchor
            self._currentPage.root.selectedPage = page
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile (filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.MessageBox (text,
                                                   _(u"Error"),
                                                   wx.ICON_ERROR | wx.OK)
        elif anchor is not None:
            return False

        return True
