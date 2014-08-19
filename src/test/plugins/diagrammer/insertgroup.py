# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class InsertGroupTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"Diagrammer"]


    def tearDown(self):
        self.loader.clear()


    def testDefault (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testName_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.name = u"Абырвалг"

        begin, end = controller.getResult ()

        valid_begin = u'''group Абырвалг {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = True
        dlg.backColor = u"blue"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    color = "blue";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = False
        dlg.backColor = u"blue"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBackColor_03 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBackColorChanged = True
        dlg.backColor = u"#AAAAAA"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    color = "#AAAAAA";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testOrientation_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isOrientationChanged = True
        dlg.orientationIndex = 0

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    orientation = landscape;

    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isOrientationChanged = True
        dlg.orientationIndex = 1

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    orientation = portrait;

    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_03 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isOrientationChanged = False
        dlg.orientationIndex = 1

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testOrientation_04 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isOrientationChanged = True
        dlg.orientationIndex = 1
        dlg.isBackColorChanged = True
        dlg.backColor = u"blue"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    color = "blue";
    orientation = portrait;

    '''

        self.assertEqual (begin, valid_begin)


    def testLabel_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.label = u"Абырвалг"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    label = "Абырвалг";

    '''

        self.assertEqual (begin, valid_begin)


    def testLabel_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.label = u""

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testTextColor_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = True
        dlg.textColor = u"blue"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    textcolor = "blue";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testTextColor_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = False
        dlg.textColor = u"blue"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testTextColor_03 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isTextColorChanged = True
        dlg.textColor = u"#AAAAAA"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    textcolor = "#AAAAAA";

    '''

        self.assertEqual (begin, valid_begin)
        self.assertEqual (end, u"\n}")


    def testBorderShape_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 0

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = box;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderShape_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderShape_03 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = False
        dlg.borderShapeIndex = 1

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_01 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        dlg.setStyleIndex (1)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = solid;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_02 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = False
        dlg.borderShapeIndex = 1

        dlg.setStyleIndex (1)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_03 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 0

        dlg.setStyleIndex (1)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = box;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_04 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        dlg.setStyleIndex (2)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = dotted;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_05 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        dlg.setStyleIndex (3)

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = dashed;

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_06 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        dlg.style = u"1,2,3,4"

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual (begin, valid_begin)


    def testBorderStyle_07 (self):
        dlg = self.plugin.InsertGroupDialog(None)
        controller = self.plugin.InsertGroupController (dlg)

        dlg.SetModalResult (wx.ID_OK)
        dlg.isBorderShapeChanged = True
        dlg.borderShapeIndex = 1

        dlg.style = u" 1, 2, 3, 4 "

        begin, end = controller.getResult ()

        valid_begin = u'''group {
    shape = line;
    style = "1,2,3,4";

    '''

        self.assertEqual (begin, valid_begin)
