#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

import wxversion

try:
    wxversion.select("2.8")
except wxversion.VersionError:
    if os.name == "nt":
        pass
    else:
        raise

import wx

from outwiker.core.application import Application
from outwiker.core.system import getOS, getPluginsDirList, getConfigPath, getExeFile
from outwiker.core.starter import Starter, StarterExit
from outwiker.core.commands import registerActions
from outwiker.gui.actioncontroller import ActionController


class OutWiker(wx.App):
    def __init__(self, *args, **kwds):
        self.logFileName = u"outwiker.log"

        wx.App.__init__ (self, *args, **kwds)


    def OnInit (self):
        getOS().migrateConfig()
        self._fullConfigPath = getConfigPath ()
        Application.init(self._fullConfigPath)

        try:
            starter = Starter()
            starter.processConsole()
        except StarterExit:
            return True

        # Если программа запускается в виде exe-шника, то перенаправить вывод ошибок в лог
        if getExeFile().endswith (u".exe"):
            # Закоментировать следующую строку, если не надо выводить strout/strerr в лог-файл
            self.RedirectStdio (self.getLogFileName (self._fullConfigPath))
            pass

        from outwiker.gui.mainwindow import MainWindow

        wx.InitAllImageHandlers()
        self.mainWnd = MainWindow(None, -1, "")
        self.SetTopWindow (self.mainWnd)

        Application.mainWindow = self.mainWnd
        Application.actionController = ActionController (self.mainWnd, Application.config)

        registerActions(Application)
        self.mainWnd.createGui()

        Application.plugins.load (getPluginsDirList())

        self.bindActivateApp()
        self.Bind (wx.EVT_QUERY_END_SESSION, self._onEndSession)

        starter.processGUI()

        return True


    def _onEndSession (self, event):
        self.mainWnd.Destroy()


    def getLogFileName (self, configPath):
        return os.path.join (os.path.split (configPath)[0], self.logFileName)


    def bindActivateApp (self):
        """
        Подключиться к событию при потере фокуса приложением
        """
        self.Bind (wx.EVT_ACTIVATE_APP, self.onActivate)


    def unbindActivateApp (self):
        """
        Отключиться от события при потере фокуса приложением
        """
        self.Unbind (wx.EVT_ACTIVATE_APP)


    def onActivate (self, event):
        Application.onForceSave()


# end of class OutWiker

if __name__ == "__main__":
    getOS().init()
    outwiker = OutWiker(False)
    outwiker.MainLoop()
