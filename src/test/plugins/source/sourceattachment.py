#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.utils import removeWiki
from .sourcefakedialog import FakeInsertDialog


class SourceAttachmentPluginTest (unittest.TestCase):
    """
    Тесты интерфейса для плагина Source
    """
    def setUp(self):
        self.__pluginname = u"Source"

        self.__createWiki()

        dirlist = [u"../plugins/source"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()
        

    def __readFile (self, path):
        with open (path) as fp:
            result = unicode (fp.read(), "utf8")

        return result
    

    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]
        

    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testAttachment1 (self):
        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.attachmentComboBox.GetCount(), 0)


    def testAttachment2 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        self.assertEqual (dialog.attachmentComboBox.GetSelection(), 0)
        self.assertEqual (dialog.attachmentComboBox.GetCount(), 2)
        self.assertEqual (dialog.attachmentComboBox.GetItems(), 
                [u"source_cp1251.cs", u"source_utf8.py"])


    def testAttachment3 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs":)', u'(:sourceend:)'))


    def testAttachment4 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (1)
        dialog.encodingComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_utf8.py":)', u'(:sourceend:)'))


    def testAttachment5 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment6 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)
        dialog.languageComboBox.SetSelection (3)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="haskell" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment7 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"haskell", u"csharp"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)
        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (2)
        dialog.languageComboBox.SetSelection (0)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" encoding="cp1251":)', u'(:sourceend:)'))


    def testAttachment8 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)
        dialog.languageComboBox.SetSelection (2)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="csharp":)', u'(:sourceend:)'))


    def testAttachment9 (self):
        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = u"../test/samplefiles/sources"
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_utf8.py")])
        Attachment(self.testPage).attach ([os.path.join (self.samplefilesPath, u"source_cp1251.cs")])

        self.config.languageList.value = [u"cpp", u"csharp", u"haskell"]

        dialog = FakeInsertDialog ()
        controller = self.loader[self.__pluginname].insertDialogControllerClass(self.testPage, dialog, self.config)
        controller.showDialog()

        dialog.fileCheckBox.SetValue(True)

        # Т.к. при изменении состояния флажка события не возникают,
        # Вручную обновим список языков
        controller.loadLanguagesState()

        dialog.attachmentComboBox.SetSelection (0)
        dialog.encodingComboBox.SetSelection (0)
        dialog.languageComboBox.SetSelection (2)
        dialog.tabWidthSpin.SetValue (10)

        result = controller.getCommandStrings()

        self.assertEqual (result, (u'(:source file="Attach:source_cp1251.cs" lang="csharp" tabwidth="10":)', u'(:sourceend:)'))