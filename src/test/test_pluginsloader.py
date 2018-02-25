# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig


class PluginsLoaderTest(unittest.TestCase):
    def setUp(self):
        self.config = PluginsConfig(Application.config)
        self.config.disabledPlugins.value = []

    def tearDown(self):
        self.config.disabledPlugins.value = []

    def testEmpty(self):
        loader = PluginsLoader(Application)
        self.assertEqual(len(loader), 0)

    def testLoad(self):
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testempty2"]
        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 2)
        self.assertEqual(loader["TestEmpty1"].name, "TestEmpty1")
        self.assertEqual(loader["TestEmpty1"].version, "0.1")
        self.assertEqual(loader["TestEmpty1"].description,
                         "This plugin is empty")
        self.assertEqual(loader["TestEmpty1"].application, Application)

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        # Проверим, как работает итерация
        for plugin in loader:
            self.assertTrue(plugin == loader["TestEmpty1"] or
                            plugin == loader["TestEmpty2"])

        loader.clear()
        self.assertEqual(len(loader), 0)

    def testVersion_01(self):
        dirlist = ["../test/plugins/testempty3"]
        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty3"].name, "TestEmpty3")
        self.assertEqual(loader["TestEmpty3"].version, "0.5")

    def testVersion_02(self):
        dirlist = ["../test/plugins/testempty4"]
        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty4"].name, "TestEmpty4")
        self.assertEqual(loader["TestEmpty4"].version, None)

    def testLoadInvalid_01(self):
        dirlist = ["../test/plugins/testinvalid",            # Нет такой директории
                   "../test/plugins/testinvalid1",
                   "../test/plugins/testinvalid2",
                   "../test/plugins/testinvalid4",
                   "../test/plugins/testinvalid5",
                   "../test/plugins/testinvalid6",
                   "../test/plugins/testinvalid7",
                   "../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testempty2",                # Ссылка на плагин testempty2 повторяется еще раз
                   "../test/plugins/testwikicommand",
                   "../test/plugins/testoutdated",
                   "../test/plugins/testfromfuture",
                   ]

        loader = PluginsLoader(Application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(loader["TestEmpty1"].name, "TestEmpty1")
        self.assertEqual(loader["TestEmpty1"].version, "0.1")
        self.assertEqual(loader["TestEmpty1"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestWikiCommand"].name, "TestWikiCommand")
        self.assertEqual(loader["TestWikiCommand"].version, "0.1")

    def testDisabledPlugins(self):
        # Добавим плагин TestEmpty1 в черный список
        self.config.disabledPlugins.value = ["TestEmpty1"]

        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 2)
        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestWikiCommand"].name, "TestWikiCommand")
        self.assertEqual(loader["TestWikiCommand"].version, "0.1")

        self.assertEqual(len(loader.disabledPlugins), 1)
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].name,
                         "TestEmpty1")
        self.assertEqual(
            loader.disabledPlugins["TestEmpty1"].version, "0.1"
        )
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].description,
                         "This plugin is empty")

    def testOnOffPlugins1(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = ["TestEmpty1"]
        loader.updateDisableList()

        self.assertEqual(len(loader), 2)
        self.assertEqual(len(loader.disabledPlugins), 1)

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].name,
                         "TestEmpty1")

    def testOnOffPlugins2(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Обновим черный список без изменений
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins3(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Добавим в черный список плагины, которые не существуют
        self.config.disabledPlugins.value = ["TestEmpty1111"]
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins4(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = ["TestEmpty1",
                                             "TestEmpty2",
                                             "TestWikiCommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

        # Обновим плагины без изменений
        loader.updateDisableList()

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

    def testOnOffPlugins5(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = ["TestEmpty1",
                                             "TestEmpty2",
                                             "TestWikiCommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

        # Включим все плагины
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins6(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)
        self.assertTrue(loader["TestEmpty1"].enabled)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = ["TestEmpty1"]
        loader.updateDisableList()

        self.assertFalse(loader.disabledPlugins["TestEmpty1"].enabled)

        # Опять включим плагин TestEmpty1
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertTrue(loader["TestEmpty1"].enabled)

    def testLoadInvalid_02(self):
        dirlist = ["../test/plugins/testinvalid1"]

        loader = PluginsLoader(Application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)

        self.assertIn('TypeError', loader.invalidPlugins[0].description)

    def testLoadInvalid_03(self):
        dirlist = ["../test/plugins/testfromfuture"]

        loader = PluginsLoader(Application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)
        # self.assertIn(u'Please, install a new OutWiker version.',
        #               loader.invalidPlugins[0].description)

    def testLoadInvalid_04(self):
        dirlist = ["../test/plugins/testoutdated"]

        loader = PluginsLoader(Application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)
        # self.assertIn(u'Please, update the plug-in.',
        #               loader.invalidPlugins[0].description)
