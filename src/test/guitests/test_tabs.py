# -*- coding: UTF-8 -*-

from os.path import basename

from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.history import HistoryBackAction, HistoryForwardAction

from .basemainwnd import BaseMainWndTest


class TabsTest (BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)

        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create (self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create (self.wikiroot["Страница 1"], "Страница 5", [])

        self._tabsController = Application.mainWindow.tabsController


    def testInit (self):
        # Пока нет откытых вики, нет и вкладок
        self.assertEqual (self._tabsController.getTabsCount(), 0)


    def testCloneEmpty1 (self):
        # Пока нет откытых вики, нет и вкладок
        self.assertEqual (self._tabsController.getTabsCount(), 0)

        self._tabsController.cloneTab()
        self.assertEqual (self._tabsController.getTabsCount(), 0)


    def testCloneEmpty2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        self._tabsController.cloneTab()
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getPage(0), None)
        self.assertEqual (self._tabsController.getPage(1), None)


    def testOpenWiki (self):
        # Откываем вики, где нет сохраненных вкладок
        Application.wikiroot = self.wikiroot

        # Должна быть одна вкладка
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual (self._tabsController.getSelection(), 0)

        # Выбранной страницы нет
        self.assertEqual (self._tabsController.getPage(0), None)

        # Так как нет выбранной страницы, то заголовок вкладки содержит имя папки с вики
        self.assertEqual (self._tabsController.getTabTitle (0), basename (self.path))


    def testSelection (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        # Должна быть одна вкладка
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        # Вкладка должна быть выбана
        self.assertEqual (self._tabsController.getSelection(), 0)

        # Выбранная страница должна быть отражена на текущей вкладке
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")

        # Выберем более вложенную страницу
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 3")

        # Выберем более вложенную страницу
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        self.assertEqual (self._tabsController.getPage(0),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 4")


    def testCloneTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        self._tabsController.cloneTab()
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 1")

        self._tabsController.cloneTab()
        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (self._tabsController.getSelection(), 2)


    def testCloneTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        self._tabsController.cloneTab()
        Application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.cloneTab()

        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")

        self.assertEqual (self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 2")

        self.assertEqual (self._tabsController.getPage(2),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getTabTitle (2), "Страница 4")


    def testRemoveSelection (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        self.wikiroot["Страница 1"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), None)
        self.assertEqual (self._tabsController.getTabTitle (0), basename (self.path))


    def testRemoveSelection2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]

        self.wikiroot["Страница 2"].remove()

        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1), None)
        self.assertEqual (self._tabsController.getTabTitle (1), basename (self.path))


    def testRemoveSelection3 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        Application.selectedPage = self.wikiroot["Страница 2"]

        self.wikiroot["Страница 2"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1), None)
        self.assertEqual (self._tabsController.getTabTitle (1), basename (self.path))


    def testRenameSelection (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self.wikiroot["Страница 1"].title = "Бла-бла-бла"

        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Бла-бла-бла"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Бла-бла-бла")


    def testRename (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self.wikiroot["Страница 1"].title = "Бла-бла-бла"

        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Бла-бла-бла"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Бла-бла-бла")

        self.assertEqual (self._tabsController.getPage(1), self.wikiroot["Бла-бла-бла"])
        self.assertEqual (self._tabsController.getTabTitle (1), "Бла-бла-бла")

        self.assertEqual (self._tabsController.getPage(2), self.wikiroot["Бла-бла-бла"])
        self.assertEqual (self._tabsController.getTabTitle (2), "Бла-бла-бла")


    def testRemove1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self.wikiroot["Страница 1"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), None)
        self.assertEqual (self._tabsController.getTabTitle (0), basename (self.path))


    def testRemove2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)

        self.wikiroot["Страница 1"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 2")


    def testRemove3 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)

        self.wikiroot["Страница 1"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getSelection(), 0)

        self.assertEqual (self._tabsController.getPage(0), None)
        self.assertEqual (self._tabsController.getTabTitle (0), basename (self.path))

        self.assertEqual (self._tabsController.getPage(1), self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 2")


    def testRemove4 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)

        self.wikiroot["Страница 2"].remove()
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getSelection(), 0)

        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")


    def testOpenInTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], True)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual (self._tabsController.getSelection(), 1)

        self.assertEqual (self._tabsController.getPage(1),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 4")


    def testOpenInTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")

        self.assertEqual (self._tabsController.getPage(1),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 4")


    def testOpenInTab3 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self._tabsController.setSelection (0)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], True)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        self.assertEqual (self._tabsController.getTabTitle (1), "Страница 4")


    def testSetSelection (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")

        self._tabsController.setSelection (2)
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getSelection(), 2)
        self.assertEqual (self._tabsController.getPage(2), self.wikiroot["Страница 2"])

        self._tabsController.setSelection (1)
        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getSelection(), 1)
        self.assertEqual (self._tabsController.getPage(1),
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])


    def testCloseWiki (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.wikiroot = None
        self.assertEqual (self._tabsController.getTabsCount(), 0)


    def testSaveTabs1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.wikiroot = None
        self.assertEqual (self._tabsController.getTabsCount(), 0)

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getSelection(), 0)
        self.assertEqual (self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")


    def testSaveTabs2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], False)

        Application.wikiroot = None
        self.assertEqual (self._tabsController.getTabsCount(), 0)

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki

        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (self._tabsController.getSelection(), 0)

        self.assertEqual (self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")
        self.assertEqual (self._tabsController.getPage(1),
                          otherwiki["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getPage(2), otherwiki["Страница 2"])


    def testSaveTabs3 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], False)
        self._tabsController.setSelection (1)

        Application.wikiroot = None
        self.assertEqual (self._tabsController.getTabsCount(), 0)

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki

        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (self._tabsController.getSelection(), 1)

        self.assertEqual (self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")
        self.assertEqual (self._tabsController.getPage(1),
                          otherwiki["Страница 2/Страница 3/Страница 4"])
        self.assertEqual (self._tabsController.getPage(2), otherwiki["Страница 2"])


    def testSaveTabs4 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3/Страница 4"], False)
        self._tabsController.setSelection (1)
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        Application.wikiroot = None
        self.assertEqual (self._tabsController.getTabsCount(), 0)

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki

        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (self._tabsController.getSelection(), 1)

        self.assertEqual (self._tabsController.getPage(0), otherwiki["Страница 1"])
        self.assertEqual (self._tabsController.getTabTitle (0), "Страница 1")
        self.assertEqual (self._tabsController.getPage(1),
                          otherwiki["Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getPage(2), otherwiki["Страница 2"])


    def testSaveTabs5 (self):
        wiki = WikiDocument.load (self.path)
        Application.wikiroot = wiki

        Application.selectedPage = wiki["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab (wiki["Страница 2"], True)
        self.assertEqual (self._tabsController.getTabsCount(), 3)

        # Загрузим вики еще раз, чтобы убедиться, что состояние вкладок мы не поменяли
        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki
        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (Application.selectedPage, otherwiki["Страница 2"])


    def testSaveAfterRemove (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()
        self._tabsController.cloneTab()

        self.wikiroot["Страница 1"].remove()

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki
        self.assertEqual (self._tabsController.getTabsCount(), 4)
        self.assertEqual (self._tabsController.getSelection(), 3)
        self.assertEqual (self._tabsController.getPage (0), otherwiki["Страница 2"])
        self.assertEqual (self._tabsController.getPage (3), otherwiki["Страница 2"])


    def testSaveAfterMove (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)

        self.wikiroot["Страница 1"].moveTo (self.wikiroot["Страница 2"])

        otherwiki = WikiDocument.load (self.path)
        Application.wikiroot = otherwiki
        self.assertEqual (self._tabsController.getTabsCount (), 3)
        self.assertEqual (self._tabsController.getPage (0), otherwiki["Страница 2/Страница 1"])
        self.assertEqual (self._tabsController.getPage (1), otherwiki["Страница 2/Страница 1"])
        self.assertEqual (self._tabsController.getPage (2), otherwiki["Страница 2"])


    def testMove (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.setSelection (2)

        self.wikiroot["Страница 1"].moveTo (self.wikiroot["Страница 2"])
        self.assertEqual (self.wikiroot["Страница 2/Страница 1"], self._tabsController.getPage (0))
        self.assertEqual (self.wikiroot["Страница 2/Страница 1"], self._tabsController.getPage (1))

        self._tabsController.setSelection (0)
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 1"])


    def testReadOnly (self):
        wikiReadOnly = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = wikiReadOnly

        Application.selectedPage = wikiReadOnly["Страница 1"]
        self._tabsController.cloneTab()
        self._tabsController.openInTab (wikiReadOnly["Страница 2"], True)
        self.assertEqual (self._tabsController.getTabsCount(), 3)

        # Загрузим вики еще раз, чтобы убедиться, что состояние вкладок мы не поменяли
        otherwiki = WikiDocument.load (self.path, readonly=True)
        Application.wikiroot = otherwiki
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (Application.selectedPage, None)


    def testCloseLastTab (self):
        """
        Тест на попытку закрыть единственную вкладку
        """
        Application.wikiroot = self.wikiroot
        self.assertEqual (self._tabsController.getTabsCount(), 1)

        self._tabsController.closeTab (0)
        self.assertEqual (self._tabsController.getTabsCount(), 1)


    def testCloseTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertEqual (self._tabsController.getTabsCount(), 3)
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 3"])

        self._tabsController.closeTab (0)
        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getPage (1), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 3"])

        self._tabsController.closeTab (0)
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 3"])


    def testCloseTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertEqual (self._tabsController.getTabsCount(), 3)

        self._tabsController.closeTab (2)

        self.assertEqual (self._tabsController.getTabsCount(), 2)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getPage (1), self.wikiroot["Страница 2"])
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2"])

        self._tabsController.closeTab (1)
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot["Страница 1"])
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])

        self._tabsController.closeTab (0)
        self.assertEqual (self._tabsController.getTabsCount(), 1)
        self.assertEqual (self._tabsController.getPage (0), self.wikiroot["Страница 1"])
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])


    def testNextTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._tabsController.nextTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getSelection(), 1)

        self._tabsController.nextTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getSelection(), 2)

        self._tabsController.nextTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testNextTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._tabsController.nextTab()

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testPrevTab1 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], False)
        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._tabsController.previousTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2/Страница 3"])
        self.assertEqual (self._tabsController.getSelection(), 2)

        self._tabsController.previousTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 2"])
        self.assertEqual (self._tabsController.getSelection(), 1)

        self._tabsController.previousTab()
        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testPrevTab2 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)

        self._tabsController.previousTab()

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])
        self.assertEqual (self._tabsController.getSelection(), 0)


    def testCloseTabInvalid (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises (ValueError, self._tabsController.closeTab, -1)
        self.assertRaises (ValueError, self._tabsController.closeTab, 3)
        self.assertRaises (ValueError, self._tabsController.closeTab, 5)


    def testTabTitleInvalid (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises (ValueError, self._tabsController.getTabTitle, -1)
        self.assertRaises (ValueError, self._tabsController.getTabTitle, 3)
        self.assertRaises (ValueError, self._tabsController.getTabTitle, 5)


    def testSetSelectionInvalid (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises (ValueError, self._tabsController.setSelection, -1)
        self.assertRaises (ValueError, self._tabsController.setSelection, 3)
        self.assertRaises (ValueError, self._tabsController.setSelection, 5)


    def testGetPageInvalid (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.openInTab (self.wikiroot["Страница 2/Страница 3"], True)

        self.assertRaises (ValueError, self._tabsController.getPage, -1)
        self.assertRaises (ValueError, self._tabsController.getPage, 3)
        self.assertRaises (ValueError, self._tabsController.getPage, 5)


    def testHistoryEmpty (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryBackAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistoryGoto (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistoryCloseWiki (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        Application.wikiroot = None
        Application.wikiroot = self.wikiroot

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistorySeveralTabs_01 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())

        Application.selectedPage = self.wikiroot["Страница 1"]

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistorySeveralTabs_02 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab (self.wikiroot["Страница 2"], True)
        self._tabsController.setSelection (0)

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistorySeveralTabs_03 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        self._tabsController.openInTab (self.wikiroot["Страница 2"], False)

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistoryBack_01 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertTrue (info_forward.menuItem.IsEnabled())


    def testHistoryBack_02 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = None

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, self.wikiroot["Страница 1"])

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertTrue (info_forward.menuItem.IsEnabled())


        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistoryBackForward_01 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        Application.selectedPage = None


        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3"])

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2"])

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 1"])


        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertTrue (info_forward.menuItem.IsEnabled())


        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2"])

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3"])

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, None)


        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())


    def testHistoryBackForward_02 (self):
        actionController = Application.actionController
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]
        Application.selectedPage = self.wikiroot["Страница 2"]
        Application.selectedPage = None
        Application.selectedPage = self.wikiroot["Страница 2/Страница 3/Страница 4"]
        Application.selectedPage = None


        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, None)

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2"])

        Application.actionController.getAction (HistoryBackAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 1"])


        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertFalse (info_back.menuItem.IsEnabled())
        self.assertTrue (info_forward.menuItem.IsEnabled())


        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2"])

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, None)

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage,
                          self.wikiroot["Страница 2/Страница 3/Страница 4"])

        Application.actionController.getAction (HistoryForwardAction.stringId).run (None)

        self.assertEqual (Application.selectedPage, None)


        info_back = actionController.getActionInfo (HistoryBackAction.stringId)
        info_forward = actionController.getActionInfo (HistoryForwardAction.stringId)

        self.assertTrue (info_back.menuItem.IsEnabled())
        self.assertFalse (info_forward.menuItem.IsEnabled())
