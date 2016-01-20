# -*- coding: UTF-8 -*-

import os
import os.path
import urllib

import wx

import gtk
import gtk.gdk

# pywebkitgtk (http://code.google.com/p/pywebkitgtk/)
# http://webkitgtk.org/reference/webkitgtk/stable/webkitgtk-webkitwebview.html
import webkit

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
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

        # Here is where we do the "magic" to embed webkit into wxGTK.
        whdl = self.GetHandle()

        window = gtk.gdk.window_lookup(whdl)

        # We must keep a reference of "pizza". Otherwise we get a crash.
        self.pizza = pizza = window.get_user_data()

        self.scrolled_window = scrolled_window = pizza.parent

        # Removing pizza to put a webview in it's place
        scrolled_window.remove(pizza)

        self.ctrl = ctrl = webkit.WebView()

        scrolled_window.add(ctrl)
        scrolled_window.show_all()

        self.canOpenUrl = False                # Можно ли открывать ссылки

        # Disable console output
        self.ctrl.connect("console-message", self._javascript_console_message)

        self.ctrl.connect("navigation-policy-decision-requested", self.__onNavigate)
        self.ctrl.connect("hovering-over-link", self.__onHoveredOverLink)
        self.ctrl.connect("notify::load-status", self.__onLoadStatus)

        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_CUT)

        self.ctrl.get_settings().set_property("tab-key-cycles-through-elements", False)

        self._path = None


    def _javascript_console_message(self, view, message, line, sourceid):
        return True


    def __onLoadStatus (self, frame, status):
        loadstatus = self.ctrl.get_load_status()

        if Application.anchor is not None and loadstatus.value_nick == "finished":
            assert self._path is not None
            self.ctrl.load_uri (self._path + "{}".format (Application.anchor))
            Application.anchor = None


    def Print (self):
        self.ctrl.get_main_frame().print_()


    def LoadPage (self, fname):
        self.canOpenUrl = True

        try:
            with open (fname) as fp:
                text = fp.read()
        except IOError:
            text = _(u"Can't read file %s") % (fname)

        self.SetPage (text, os.path.dirname (fname))
        self.canOpenUrl = False


    def SetPage (self, htmltext, basepath):
        self.canOpenUrl = True
        self._path = "file://" + urllib.quote (basepath.encode ("utf8")) + "/"

        self.ctrl.load_string (htmltext,
                               "text/html",
                               "utf8",
                               self._path)
        self.canOpenUrl = False


    def __onCopyFromHtml(self, event):
        self.ctrl.copy_clipboard ()
        event.Skip()


    def __identifyUri (self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename)
        """
        uri = self.ctrl.get_main_frame().get_uri()

        if uri is not None:
            basepath = unicode (urllib.unquote (self.ctrl.get_main_frame().get_uri()), "utf8")
            identifier = UriIdentifierWebKit (self._currentPage, basepath)

            return identifier.identify (href)

        return (None, None, None, None)


    def __onHoveredOverLink (self, view, title, uri):
        if uri is None:
            self.setStatusText (uri, u"")
            return

        try:
            href = unicode (urllib.unquote (uri), "utf8")
        except UnicodeDecodeError:
            self.setStatusText (uri, u"")
            return

        (url, page, filename, anchor) = self.__identifyUri (href)

        if url is not None:
            self.setStatusText (href, url)
            return

        if page is not None:
            text = page.subpath
            if anchor is not None:
                text += "/" + anchor

            self.setStatusText (href, text)
            return

        if filename is not None:
            self.setStatusText (href, filename)
            return

        if anchor is not None:
            self.setStatusText (href, anchor)
            return

        self.setStatusText (href, u"")


    def __onNavigate (self, view, frame, request, action, decision):
        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        if frame != self.ctrl.get_main_frame():
            return False

        # Проверка на перезагрузку страницы
        if action.get_reason().value_nick == "reload":
            return True

        curr_href = self.ctrl.get_main_frame().get_uri()

        try:
            href = unicode (urllib.unquote (request.get_uri()), "utf8")
        except UnicodeDecodeError:
            return True

        if self.canOpenUrl or href == curr_href:
            # Если вызов uri осуществляется из программы или это запрос на обновление, то
            # разрешить обработать запрос компоненту
            return False
        else:
            button = action.get_button()
            modifier = action.get_modifier_state()
            return self.__onLinkClicked (href, button, modifier)


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
        gtk_mouse_button - кнопка мыши, с помощью которой кликнули по ссылке (1 - левая, 2 - средняя, 3 - правая, -1 - не известно)
        gtk_key_modifier - зажатые клавиши (1 - Shift, 4 - Ctrl)
        """
        (url, page, filename, anchor) = self.__identifyUri (href)

        modifier = self.__gtk2OutWikerKeyCode (gtk_key_modifier)
        mouse_button = self.__gtk2OutWikerMouseButtonCode (gtk_mouse_button)

        params = self._getClickParams (self._decodeIDNA (href),
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

        elif page is not None and (mouse_button == ID_MOUSE_MIDDLE or modifier == ID_KEY_CTRL):
            Application.mainWindow.tabsController.openInTab (page, True)

        elif page is not None:
            Application.anchor = anchor
            self._currentPage.root.selectedPage = page

        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile (filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

        elif anchor is not None:
            return False

        return True
