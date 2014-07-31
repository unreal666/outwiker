# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertNodeTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]


    def tearDown(self):
        self.loader.clear()


    def testName_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testName_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг 111"

        result = controller.getResult ()

        self.assertEqual (result, u'"Абырвалг 111"')


    def testShapeSelection_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (0)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг")


    def testShapeSelection_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (1)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = actor];")


    def testShapeSelection_03 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setShapeSelection (10)

        result = controller.getResult ()

        self.assertEqual (result, u"Абырвалг [shape = flowchart.database];")


    def testBorderStyle_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex = 0

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex (1)

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_03 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setBorderStyleIndex (2)

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = dotted];")


    def testBorderStyle_04 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u""

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг")


    def testBorderStyle_05 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"solid"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_06 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"Solid"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_07 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u" Solid "

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [style = solid];")


    def testBorderStyle_08 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"1,2,3"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_09 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u"1, 2, 3"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_10 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u" 1, 2, 3 "

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_11 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.borderStyle = u'"1,2,3"'

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [style = "1,2,3"];')


    def testBorderStyle_12 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        dlg.setShapeSelection (1)
        dlg.borderStyle = u"dotted"

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [shape = actor, style = dotted];")


    def testStacked_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.stacked = True

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [stacked];")


    def testStacked_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.stacked = True
        dlg.setShapeSelection (1)

        result = controller.getResult ()
        self.assertEqual (result, u"Абырвалг [shape = actor, stacked];")


    def testLabel_01 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.label = u"Превед"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [label = "Превед"];')


    def testLabel_02 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.setShapeSelection (1)
        dlg.label = u"Превед"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг [shape = actor, label = "Превед"];')


    def testLabel_03 (self):
        dlg = self.plugin.InsertNodeDialog(None)
        controller = self.plugin.InsertNodeController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"
        dlg.label = u"Абырвалг"

        result = controller.getResult ()
        self.assertEqual (result, u'Абырвалг')
