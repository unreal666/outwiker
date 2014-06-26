# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class MainWndTest(BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.rootwiki, u"Страница 1", [])
        factory.create (self.rootwiki, u"Страница 2", [])
        factory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
        factory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testProperties (self):
        self.assertNotEqual (None, self.wnd.treePanel.panel)
        self.assertNotEqual (None, self.wnd.pagePanel)
        self.assertNotEqual (None, self.wnd.attachPanel)
        self.assertNotEqual (None, self.wnd.mainMenu)
        self.assertNotEqual (None, self.wnd.toolbars)
        self.assertNotEqual (None, self.wnd.statusbar)
        self.assertNotEqual (None, self.wnd.taskBarIcon)

        self.assertNotEqual (None, self.wnd.mainWindowConfig)
        self.wnd.mainToolbar.Realize()


    def testTitle1 (self):
        conf = MainWindowConfig (Application.config)
        conf.titleFormat.value = u"OutWiker - {page} - {file}"

        self.assertEqual (self.wnd.GetTitle(), u"OutWiker")

        Application.wikiroot = self.rootwiki
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker -  - testwiki")

        self.rootwiki.selectedPage = self.rootwiki[u"Страница 1"]
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 1 - testwiki")

        self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 3 - testwiki")


    def testTitle2 (self):
        conf = MainWindowConfig (Application.config)
        conf.titleFormat.value = u"{file} - {page} - OutWiker"

        self.assertEqual (self.wnd.GetTitle(), u"OutWiker")

        Application.wikiroot = self.rootwiki
        self.assertEqual (self.wnd.GetTitle(), u"testwiki -  - OutWiker")

        self.rootwiki.selectedPage = self.rootwiki[u"Страница 1"]
        self.assertEqual (self.wnd.GetTitle(), u"testwiki - Страница 1 - OutWiker")

        self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
        self.assertEqual (self.wnd.GetTitle(), u"testwiki - Страница 3 - OutWiker")
