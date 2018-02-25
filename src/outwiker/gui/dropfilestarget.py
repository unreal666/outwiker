# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import attachFiles


class DropFilesTarget(wx.FileDropTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и OutWiker
    """
    def __init__(self, application, dropWnd):
        wx.FileDropTarget.__init__(self)
        self._application = application
        self._dropWnd = dropWnd
        self._dropWnd.SetDropTarget(self)

    def destroy(self):
        self._dropWnd.SetDropTarget(None)
        self._dropWnd = None

    def OnDropFiles(self, x, y, files):
        if len(files) == 1 and '\n' in files[0]:
            files = files[0].split('\n')

        file_protocol = 'file://'

        correctedFiles = []
        for fname in files:
            if not fname.strip():
                continue

            if fname.startswith(file_protocol):
                fname = fname[len(file_protocol):]

            correctedFiles.append(fname)

        if (self._application.wikiroot is not None and
                self._application.wikiroot.selectedPage is not None):
            attachFiles(self._application.mainWindow,
                        self._application.wikiroot.selectedPage,
                        correctedFiles)
            return True
