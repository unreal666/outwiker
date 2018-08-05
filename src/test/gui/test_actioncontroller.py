# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.actioncontroller import ActionController
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.hotkey import HotKey
from outwiker.gui.hotkeyparser import HotKeyParser
from outwiker.gui.hotkeyoption import HotKeyOption
from outwiker.gui.defines import MENU_FILE, TOOLBAR_PLUGINS
from test.basetestcases import BaseOutWikerGUIMixin


class ExampleAction(BaseAction):
    stringId = "test_action"

    def __init__(self):
        self.runCount = 0

    @property
    def title(self):
        return "Тестовый Action"

    @property
    def description(self):
        return "Тестовый Action"

    def run(self, params):
        self.runCount += 1


class ExampleCheckAction(BaseAction):
    stringId = "test_check_action"

    def __init__(self):
        self.runCount = 0

    @property
    def title(self):
        return "Тестовый CheckAction"

    @property
    def description(self):
        return "Тестовый CheckAction"

    def run(self, params):
        if params:
            self.runCount += 1
        else:
            self.runCount -= 1


class ActionControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

        self.actionController = ActionController(self.mainWindow, self.application.config)
        self.application.config.remove_section(self.actionController.configSection)
        self.fileMenu = self.mainWindow.menuController[MENU_FILE]

    def tearDown(self):
        self.application.config.remove_section(self.actionController.configSection)
        self.destroyApplication()

    def testRegisterAction(self):
        action = ExampleAction()

        self.assertEqual(len(self.actionController.getActionsStrId()), 0)

        self.actionController.register(action)

        self.assertEqual(len(self.actionController.getActionsStrId()), 1)

    def testHotKeys(self):
        hotkey1 = HotKey("F1")
        action1 = ExampleAction()

        hotkey2 = HotKey("F2", ctrl=True)
        action2 = ExampleCheckAction()

        self.actionController.register(action1, hotkey1)
        self.actionController.register(action2, hotkey2)

        self.assertEqual(self.actionController.getHotKey(action1.stringId),
                         hotkey1)
        self.assertEqual(self.actionController.getHotKey(action2.stringId),
                         hotkey2)

    def testTitles(self):
        action1 = ExampleAction()
        action2 = ExampleCheckAction()

        self.actionController.register(action1)
        self.actionController.register(action2)

        self.assertEqual(self.actionController.getTitle(action1.stringId),
                         action1.title)
        self.assertEqual(self.actionController.getTitle(action2.stringId),
                         action2.title)

    def testAppendMenu(self):
        action = ExampleAction()
        menu = self.fileMenu

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self._assertMenuItemExists(menu, action.title, None)

    def testAppendCheckMenu(self):
        action = ExampleCheckAction()
        menu = self.fileMenu

        self.actionController.register(action)
        self.actionController.appendMenuCheckItem(action.stringId, menu)
        self._assertMenuItemExists(menu, action.title, None)

    def testRemoveAction(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(len(self.actionController.getActionsStrId()), 1)
        self._assertMenuItemExists(menu, action.title, None)
        self.assertEqual(toolbar.GetToolsCount(), 1)

        self.actionController.removeAction(action.stringId)
        toolbar.Realize()

        self.assertEqual(len(self.actionController.getActionsStrId()), 0)
        self.assertEqual(menu.FindItem(action.title), wx.NOT_FOUND)
        self.assertEqual(toolbar.GetToolsCount(), 0)

    def testRemoveActionAndRun(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        menuItemId = self._getMenuItemId(action.stringId)
        toolItemId = self._getToolItemId(action.stringId)

        self._emulateMenuClick(menuItemId)
        self.assertEqual(action.runCount, 1)

        self._emulateButtonClick(toolItemId)
        self.assertEqual(action.runCount, 2)

        self.actionController.removeAction(action.stringId)

        self._emulateMenuClick(menuItemId)
        self.assertEqual(action.runCount, 2)

        self._emulateButtonClick(toolItemId)
        self.assertEqual(action.runCount, 2)

    def testRunAction(self):
        action = ExampleAction()
        menu = self.fileMenu

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)

        menuItemId = self._getMenuItemId(action.stringId)

        self._emulateMenuClick(menuItemId)

        self.assertEqual(action.runCount, 1)

        self.actionController.removeAction(action.stringId)

        # Убедимся, что после удаления пункта меню,
        # событие больше не срабатывает
        self._emulateMenuClick(menuItemId)
        self.assertEqual(action.runCount, 1)

    def testAppendToolbarButton(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)

        self.actionController.removeAction(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 0)

    def testAppendToolbarCheckButton(self):
        action = ExampleCheckAction()
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)

        self.actionController.removeAction(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 0)

    def testAppendToolbarCheckButtonAndRun(self):
        action = ExampleCheckAction()
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)

        toolItemId = self._getToolItemId(action.stringId)

        self._emulateCheckButtonClick(toolItemId)
        self.assertEqual(action.runCount, 1)

        self._emulateCheckButtonClick(toolItemId)
        self.assertEqual(action.runCount, 0)

        self._emulateCheckButtonClick(toolItemId)
        self.assertEqual(action.runCount, 1)

        self.actionController.removeAction(action.stringId)

    def testCheckButtonAndMenuWithEvents(self):
        action = ExampleCheckAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)
        self.actionController.appendMenuCheckItem(action.stringId, menu)

        menuItem = self._getMenuItem(action.stringId)
        toolItem = self._getToolItem(toolbar, action.stringId)
        toolItemId = self._getToolItemId(action.stringId)

        self.assertFalse(menuItem.IsChecked())
        self.assertFalse(toolItem.IsToggled())

        self._emulateCheckButtonClick(toolItemId)

        self.assertTrue(menuItem.IsChecked())
        self.assertTrue(toolItem.IsToggled())

        self._emulateCheckButtonClick(toolItemId)

        self.assertFalse(menuItem.IsChecked())
        self.assertFalse(toolItem.IsToggled())

    def testCheckButtonAndMenu(self):
        action = ExampleCheckAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)
        self.actionController.appendMenuCheckItem(action.stringId, menu)

        menuItem = self._getMenuItem(action.stringId)
        toolItem = self._getToolItem(toolbar, action.stringId)

        self.assertFalse(menuItem.IsChecked())
        self.assertFalse(toolItem.IsToggled())
        self.assertEqual(action.runCount, 0)

        self.actionController.check(action.stringId, True)

        self.assertTrue(menuItem.IsChecked())
        self.assertTrue(toolItem.IsToggled())
        self.assertEqual(action.runCount, 1)

        self.actionController.check(action.stringId, True)

        self.assertTrue(menuItem.IsChecked())
        self.assertTrue(toolItem.IsToggled())
        self.assertEqual(action.runCount, 2)

        self.actionController.check(action.stringId, False)

        self.assertFalse(menuItem.IsChecked())
        self.assertFalse(toolItem.IsToggled())
        self.assertEqual(action.runCount, 1)

        self.actionController.check(action.stringId, False)

        self.assertFalse(menuItem.IsChecked())
        self.assertFalse(toolItem.IsToggled())
        self.assertEqual(action.runCount, 0)

    def testRemoveCheckMenu(self):
        action = ExampleCheckAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)

        self.actionController.appendMenuCheckItem(action.stringId, menu)
        self.actionController.removeMenuItem(action.stringId)

        toolItem = self._getToolItem(toolbar, action.stringId)
        toolItemId = self._getToolItemId(action.stringId)

        self.assertFalse(toolItem.IsToggled())

        self._emulateCheckButtonClick(toolItemId)

        self.assertTrue(toolItem.IsToggled())

        self._emulateCheckButtonClick(toolItemId)

        self.assertFalse(toolItem.IsToggled())

    def testAppendToolbarButtonOnly(self):
        action = ExampleAction()
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)

        self.actionController.removeAction(action.stringId)

        self.assertEqual(toolbar.GetToolsCount(), 0)
        toolbar.Realize()

    def testAppendToolbarButtonAndRun(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        menuItemId = self._getMenuItemId(action.stringId)

        self._emulateMenuClick(menuItemId)
        self.assertEqual(action.runCount, 1)

        self.actionController.removeAction(action.stringId)

        self._emulateMenuClick(menuItemId)
        self.assertEqual(action.runCount, 1)

    def testAppendToolbarButtonOnlyAndRun(self):
        action = ExampleAction()
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        toolItemId = self._getToolItemId(action.stringId)

        self._emulateButtonClick(toolItemId)
        self.assertEqual(action.runCount, 1)

        self.actionController.removeAction(action.stringId)

        self._emulateButtonClick(toolItemId)
        self.assertEqual(action.runCount, 1)

    def testRemoveToolButton(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self._assertMenuItemExists(menu, action.title, None)

        self.actionController.removeToolbarButton(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 0)
        self._assertMenuItemExists(menu, action.title, None)

    def testRemoveToolButtonInvalid(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 0)
        self._assertMenuItemExists(menu, action.title, None)

        self.actionController.removeToolbarButton(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 0)
        self._assertMenuItemExists(menu, action.title, None)

    def testRemoveMenuItemInvalid(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(menu.FindItem(action.title), wx.NOT_FOUND)

        self.actionController.removeMenuItem(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(menu.FindItem(action.title), wx.NOT_FOUND)

    def testRemoveMenuItem(self):
        action = ExampleAction()
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action)
        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self._assertMenuItemExists(menu, action.title, None)

        self.actionController.removeMenuItem(action.stringId)
        toolbar.Realize()

        self.assertEqual(toolbar.GetToolsCount(), 1)
        self.assertEqual(menu.FindItem(action.title), wx.NOT_FOUND)

    def testHotKeysDefaultMenu(self):
        action = ExampleAction()
        menu = self.fileMenu
        hotkey = HotKey("T", ctrl=True)

        self.actionController.register(action, hotkey=hotkey)
        self.assertEqual(self.actionController.getHotKey(action.stringId),
                         hotkey)

        self.actionController.appendMenuItem(action.stringId, menu)

        self._assertMenuItemExists(menu, action.title, hotkey)

    def testHotKeysDefaultToolBar(self):
        action = ExampleAction()
        hotkey = HotKey("T", ctrl=True)
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action, hotkey=hotkey)
        self.assertEqual(self.actionController.getHotKey(action.stringId),
                         hotkey)

        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        self.assertEqual(self._getToolItemLabel(toolbar, action.stringId),
                         "{0} ({1})".format(action.title,
                                            HotKeyParser.toString(hotkey)))

    def testDisableTools(self):
        action = ExampleAction()
        hotkey = HotKey("T", ctrl=True)
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        self.actionController.register(action, hotkey=hotkey)

        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        toolid = self._getToolItemId(action.stringId)

        self.actionController.enableTools(action.stringId, False)
        self.assertFalse(toolbar.GetToolEnabled(toolid))

        self.actionController.enableTools(action.stringId, True)
        self.assertTrue(toolbar.GetToolEnabled(toolid))

    def testDisableMenuItem(self):
        action = ExampleAction()
        hotkey = HotKey("T", ctrl=True)
        menu = self.fileMenu

        self.actionController.register(action, hotkey=hotkey)

        self.actionController.appendMenuItem(action.stringId, menu)

        menuItemId = self._getMenuItemId(action.stringId)

        self.actionController.enableTools(action.stringId, False)
        self.assertFalse(menu.IsEnabled(menuItemId))

        self.actionController.enableTools(action.stringId, True)
        self.assertTrue(menu.IsEnabled(menuItemId))

    def testDidableToolsAll(self):
        action = ExampleAction()
        hotkey = HotKey("T", ctrl=True)
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"
        menu = self.fileMenu

        self.actionController.register(action, hotkey=hotkey)

        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        menuItemId = self._getMenuItemId(action.stringId)
        toolid = self._getToolItemId(action.stringId)

        self.actionController.enableTools(action.stringId, False)
        self.assertFalse(toolbar.GetToolEnabled(toolid))
        self.assertFalse(menu.IsEnabled(menuItemId))

        self.actionController.enableTools(action.stringId, True)
        self.assertTrue(toolbar.GetToolEnabled(toolid))
        self.assertTrue(menu.IsEnabled(menuItemId))

    def testDisableToolsNone(self):
        action = ExampleAction()
        hotkey = HotKey("T", ctrl=True)

        self.actionController.register(action, hotkey=hotkey)
        self.actionController.enableTools(action.stringId, False)

    def testGetActions1(self):
        action1 = ExampleAction()
        action2 = ExampleCheckAction()

        self.actionController.register(action1)
        self.actionController.register(action2)

        self.assertEqual(self.actionController.getAction(action1.stringId),
                         action1)
        self.assertEqual(self.actionController.getAction(action2.stringId),
                         action2)

    def testGetActions2(self):
        action1 = ExampleAction()
        action2 = ExampleCheckAction()
        self.actionController.register(action1)

        self.assertRaises(KeyError, self.actionController.getAction,
                          action2.stringId)

    def testHotKeyLoadConfig(self):
        action = ExampleAction()
        hotKeyFromConfig = HotKey("F11")
        HotKeyOption(self.application.config,
                     self.actionController.configSection,
                     action.stringId, None).value = hotKeyFromConfig

        self.actionController.register(action, HotKey("F12", ctrl=True))

        self.assertEqual(self.actionController.getHotKey(action.stringId).key,
                         "F11")
        self.assertFalse(self.actionController.getHotKey(action.stringId).ctrl)
        self.assertFalse(self.actionController.getHotKey(action.stringId).shift)
        self.assertFalse(self.actionController.getHotKey(action.stringId).alt)

    def testHotKeySaveConfig1(self):
        action = ExampleAction()
        hotkey = HotKey("F11", ctrl=True)

        self.actionController.register(action, hotkey)
        self.actionController.saveHotKeys()

        otherActionController = ActionController(self.mainWindow, self.application.config)
        otherActionController.register(action)

        self.assertEqual(otherActionController.getHotKey(action.stringId).key,
                         "F11")
        self.assertTrue(otherActionController.getHotKey(action.stringId).ctrl)
        self.assertFalse(otherActionController.getHotKey(action.stringId).shift)
        self.assertFalse(otherActionController.getHotKey(action.stringId).alt)

    def testHotKeySaveConfig2(self):
        action = ExampleAction()
        hotkey = HotKey("F11", ctrl=True)

        self.actionController.register(action, hotkey)
        self.actionController.saveHotKeys()

        otherActionController = ActionController(self.mainWindow, self.application.config)
        otherActionController.register(action, HotKey("F1", shift=True))

        self.assertEqual(otherActionController.getHotKey(action.stringId).key,
                         "F11")
        self.assertTrue(otherActionController.getHotKey(action.stringId).ctrl)
        self.assertFalse(otherActionController.getHotKey(action.stringId).shift)
        self.assertFalse(otherActionController.getHotKey(action.stringId).alt)

    def testHotKeySaveConfig3(self):
        action = ExampleAction()

        self.actionController.register(action)
        self.actionController.saveHotKeys()

        otherActionController = ActionController(self.mainWindow, self.application.config)
        otherActionController.register(action)

        self.assertEqual(otherActionController.getHotKey(action.stringId).key,
                         "")
        self.assertFalse(otherActionController.getHotKey(action.stringId).ctrl)
        self.assertFalse(otherActionController.getHotKey(action.stringId).shift)
        self.assertFalse(otherActionController.getHotKey(action.stringId).alt)

    def testSetHotKey(self):
        action = ExampleAction()
        self.actionController.register(action, None)

        hotkey = HotKey("F11", ctrl=True)
        self.actionController.setHotKey(action.stringId, hotkey)
        self.assertEqual(self.actionController.getHotKey(action.stringId),
                         hotkey)

    def testChangeHotkeyGui(self):
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleAction()
        self.actionController.register(action, None)

        self.actionController.appendMenuItem(action.stringId, menu)
        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        self.actionController.setHotKey(action.stringId, hotkey)

        self.assertEqual(self._getToolItemLabel(toolbar, action.stringId),
                         "{} ({})".format(action.title, "Ctrl+F11"))

        self.assertEqual(self._getMenuItem(action.stringId).GetItemLabel(),
                         "{}\t{}".format(action.title, "Ctrl+F11"))

    def testChangeHotkeyGuiMenu(self):
        menu = self.fileMenu

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleAction()
        self.actionController.register(action, None)

        self.actionController.appendMenuItem(action.stringId, menu)

        self.actionController.setHotKey(action.stringId, hotkey)

        self.assertEqual(self._getMenuItem(action.stringId).GetItemLabel(),
                         "{}\t{}".format(action.title, "Ctrl+F11"))

    def testChangeHotkeyToolbar(self):
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleAction()
        self.actionController.register(action, None)

        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        self.actionController.setHotKey(action.stringId, hotkey)

        self.assertEqual(self._getToolItemLabel(toolbar, action.stringId),
                         "{} ({})".format(action.title, "Ctrl+F11"))

    def testDelayChangeHotkeyToolbar(self):
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleAction()
        self.actionController.register(action, HotKey("F11"))

        self.actionController.appendToolbarButton(action.stringId,
                                                  toolbar,
                                                  image)

        self.actionController.setHotKey(action.stringId, hotkey, False)

        self.assertEqual(self._getToolItemLabel(toolbar, action.stringId),
                         "{} ({})".format(action.title, "F11"))

        otherActionController = ActionController(self.mainWindow, self.application.config)
        otherActionController.register(action, None)

        self.assertEqual(otherActionController.getHotKey(action.stringId),
                         hotkey)

    def testChangeHotkeyGuiChecked1(self):
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleCheckAction()
        self.actionController.register(action, None)

        self.actionController.appendMenuCheckItem(action.stringId, menu)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)

        self.actionController.setHotKey(action.stringId, hotkey)

        self.assertEqual(self._getToolItemLabel(toolbar, action.stringId),
                         "{} ({})".format(action.title, "Ctrl+F11"))

        self.assertEqual(self._getMenuItem(action.stringId).GetItemLabel(),
                         "{}\t{}".format(action.title, "Ctrl+F11"))

    def testChangeHotkeyGuiChecked2(self):
        menu = self.fileMenu
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        image = "../test/images/save.png"

        hotkey = HotKey("F11", ctrl=True)

        action = ExampleCheckAction()
        self.actionController.register(action, None)

        self.actionController.appendMenuCheckItem(action.stringId, menu)
        self.actionController.appendToolbarCheckButton(action.stringId,
                                                       toolbar,
                                                       image)

        menuItem = self._getMenuItem(action.stringId)
        toolItem = self._getToolItem(toolbar, action.stringId)

        self.actionController.setHotKey(action.stringId, hotkey)
        self.actionController.check(action.stringId, True)

        self.assertTrue(menuItem.IsChecked())
        self.assertTrue(toolItem.IsToggled())

    def _assertMenuItemExists(self, menu, title, hotkey):
        """
        Проверить, что в меню есть элемент с заголовком(title + '\t' + hotkey)
        """
        menuItemId = menu.FindItem(title)
        self.assertNotEqual(menuItemId, wx.NOT_FOUND)

        menuItem = menu.FindItemById(menuItemId)

        if hotkey is not None:
            self.assertEqual(menuItem.GetItemLabel(),
                             title + "\t" + HotKeyParser.toString(hotkey))
        else:
            self.assertEqual(menuItem.GetItemLabel(), title)

    def _emulateMenuClick(self, menuItemId):
        """
        Эмуляция события выбора пункта меню
        """
        event = wx.CommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED, menuItemId)
        self.mainWindow.ProcessEvent(event)

    def _emulateButtonClick(self, toolitemId):
        """
        Эмуляция события выбора пункта меню
        """
        event = wx.CommandEvent(wx.wxEVT_COMMAND_TOOL_CLICKED, toolitemId)
        self.mainWindow.ProcessEvent(event)

    def _emulateCheckButtonClick(self, toolitemId):
        """
        Эмуляция события выбора пункта меню
        """
        toolbar = self.mainWindow.toolbars[TOOLBAR_PLUGINS]
        toolitem = toolbar.FindById(toolitemId)
        newState = not toolitem.IsToggled()
        toolbar.ToggleTool(toolitemId, newState)

        event = wx.CommandEvent(wx.wxEVT_COMMAND_TOOL_CLICKED, toolitemId)
        event.SetInt(newState)
        self.mainWindow.ProcessEvent(event)

    def _getMenuItemId(self, strid):
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.menuItem.GetId()

        return result

    def _getMenuItem(self, strid):
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.menuItem

        return result

    def _getToolItemId(self, strid):
        """
        Получить идентификатор кнопки с панели инструментов
        """
        result = None

        actionInfo = self.actionController.getActionInfo(strid)
        if actionInfo is not None:
            result = actionInfo.toolItemId

        return result

    def _getToolItemLabel(self, toolbar, strid):
        result = None

        item = self._getToolItem(toolbar, strid)

        if item is not None:
            result = item.GetShortHelp()

        return result

    def _getToolItem(self, toolbar, strid):
        result = None

        itemId = self._getToolItemId(strid)
        if itemId is not None:
            result = toolbar.FindById(itemId)

        return result
