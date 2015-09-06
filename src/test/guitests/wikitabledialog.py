# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.wiki.tabledialogcontroller import TableDialogController


class WikiTableDialogTest (BaseMainWndTest):
    def setUp (self):
        super (WikiTableDialogTest, self).setUp()
        self._application = Application

        factory = WikiPageFactory()
        self._testpage = factory.create (self.wikiroot, u"Страница 1", [])


    def tearDown (self):
        super (WikiTableDialogTest, self).tearDown()


    def testDictToStr_01_empty (self):
        params = {}
        result = TableDialogController.dictToStr (params)

        validResult = u''

        self.assertEqual (result, validResult)


    def testDictToStr_02 (self):
        params = {
            u'param1': 10
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10"'

        self.assertEqual (result, validResult)


    def testDictToStr_03 (self):
        params = {
            u'param1': 10,
            u'Параметр2': u'абырвалг',
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10", Параметр2="абырвалг"'

        self.assertEqual (result, validResult)


    def testDictToStr_04 (self):
        params = {
            u'param1': 10,
            u'Параметр2': u"абыр'валг",
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10", Параметр2="абыр\'валг"'

        self.assertEqual (result, validResult)


    def testDictToStr_05 (self):
        params = {
            u'param1': 10,
            u'Параметр2': u'абыр"валг',
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10", Параметр2=\'абыр"валг\''

        self.assertEqual (result, validResult)


    def testDictToStr_06 (self):
        params = {
            u'param1': 10,
            u'Параметр2': u'аб\'ыр"валг',
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10", Параметр2="аб\'ыр\\"валг"'

        self.assertEqual (result, validResult, result)


    def testDictToStr_07 (self):
        params = {
            u'param1': 10,
            u'Параметр2': u'',
        }
        result = TableDialogController.dictToStr (params)

        validResult = u'param1="10", Параметр2=""'

        self.assertEqual (result, validResult, result)


    def testDefault (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testDefault_suffix (self):
        suffix = u'20'
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table20 border="1":)
(:row20:)
(:cell20:)
(:table20end:)'''

        self.assertEqual (result, validResult, result)


    def testCells (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)

        dlg.colsCount = 5
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testRowsCells (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)

        dlg.colsCount = 5
        dlg.rowsCount = 3
        Tester.dialogTester.appendOk()

        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="1":)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:row:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)


    def testBorder (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        controller = TableDialogController (dlg, suffix, self._application.config)
        Tester.dialogTester.appendOk()

        dlg.borderWidth = 10
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table border="10":)
(:row:)
(:cell:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)
