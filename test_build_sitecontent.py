# -*- coding: UTF-8 -*-

import unittest

from buildtools.contentgenerators import (SiteChangelogGenerator,
                                          SitePluginsTableGenerator)
from outwiker.core.appinfo import AppInfo, VersionInfo, RequirementsInfo
from outwiker.core.version import Version


class SitePluginsTableGeneratorTest (unittest.TestCase):
    def test_empty(self):
        appInfoList = []
        generator = SitePluginsTableGenerator(appInfoList)
        text = generator.make()

        self.assertEqual(text, u'')

    def test_single_01(self):
        appInfoList = []

        requirements_1 = RequirementsInfo(Version(1, 2, 3, 199),
                                          [u'Windows', u'Linux'])
        appInfo_1 = AppInfo(u'Плагин 1',
                            None,
                            description=u'Описание плагина 1.',
                            appwebsite=u'http://example.com/plugin_1/',
                            requirements=requirements_1)

        appInfoList.append(appInfo_1)
        generator = SitePluginsTableGenerator(appInfoList)
        text = generator.make()

        self.assertEqual(text, u'''||[[Плагин 1 -> http://example.com/plugin_1/]] ||Описание плагина 1. || Windows, Linux || 1.2.3 ||''')

    def test_pair_01(self):
        appInfoList = []

        requirements_1 = RequirementsInfo(Version(1, 2, 3, 199),
                                          [u'Linux', u'Windows'])
        appInfo_1 = AppInfo(u'Плагин 1',
                            None,
                            description=u'Описание плагина 1.',
                            appwebsite=u'http://example.com/plugin_1/',
                            requirements=requirements_1)

        requirements_2 = RequirementsInfo(Version(3, 4, 5, 255),
                                          [u'Linux', u'Windows'])
        appInfo_2 = AppInfo(u'Плагин 2',
                            None,
                            description=u'Описание плагина 2.',
                            appwebsite=u'http://example.com/plugin_2/',
                            requirements=requirements_2)

        appInfoList.append(appInfo_1)
        appInfoList.append(appInfo_2)
        generator = SitePluginsTableGenerator(appInfoList)
        text = generator.make()

        self.assertEqual(text, u'''||[[Плагин 1 -> http://example.com/plugin_1/]] ||Описание плагина 1. || Windows, Linux || 1.2.3 ||
||[[Плагин 2 -> http://example.com/plugin_2/]] ||Описание плагина 2. || Windows, Linux || 3.4.5 ||''')

    def test_pair_02(self):
        appInfoList = []

        requirements_1 = RequirementsInfo(Version(1, 2, 3, 199),
                                          [u'Linux', u'Windows'])
        appInfo_1 = AppInfo(u'Плагин 1',
                            None,
                            description=u'Описание плагина 1.',
                            appwebsite=u'http://example.com/plugin_1/',
                            requirements=requirements_1)

        requirements_2 = RequirementsInfo(Version(3, 4, 5, 255),
                                          [u'Linux', u'Windows'])
        appInfo_2 = AppInfo(u'Плагин 2',
                            None,
                            description=u'Описание плагина 2.',
                            appwebsite=u'http://example.com/plugin_2/',
                            requirements=requirements_2)

        appInfoList.append(appInfo_2)
        appInfoList.append(appInfo_1)
        generator = SitePluginsTableGenerator(appInfoList)
        text = generator.make()

        self.assertEqual(text, u'''||[[Плагин 1 -> http://example.com/plugin_1/]] ||Описание плагина 1. || Windows, Linux || 1.2.3 ||
||[[Плагин 2 -> http://example.com/plugin_2/]] ||Описание плагина 2. || Windows, Linux || 3.4.5 ||''')

    def test_single_02(self):
        appInfoList = []

        requirements_1 = RequirementsInfo(Version(1, 2, 3, 199),
                                          [u'Linux', u'Windows'])
        appInfo_1 = AppInfo(u'Плагин 1',
                            None,
                            description=u'Описание плагина 1.',
                            appwebsite=u'http://example.com/plugin_1/',
                            requirements=requirements_1)

        appInfoList.append(appInfo_1)
        generator = SitePluginsTableGenerator(appInfoList)
        text = generator.make()

        self.assertEqual(text, u'''||[[Плагин 1 -> http://example.com/plugin_1/]] ||Описание плагина 1. || Windows, Linux || 1.2.3 ||''')


class ChangelogContentTest (unittest.TestCase):
    def setUp(self):
        self._appname = u'Test'
        self._author = None

    def test_changelog_None(self):
        appinfo = None
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()
        self.assertEqual(changelog, u'')

    def test_changelog_empty(self):
        changelog = []
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()
        self.assertEqual(changelog, u'')

    def test_changelog_single_01(self):
        version_1 = VersionInfo(Version(1))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1'''

        self.assertEqual(changelog, right_result)

    def test_changelog_single_02(self):
        version_1 = VersionInfo(Version(1, 0))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_03(self):
        version_1 = VersionInfo(Version.parse(u'1.2.3 beta'))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.2.3 beta'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_date(self):
        version_1 = VersionInfo(Version.parse(u'1.2.3 beta'),
                                date_str=u'13.06.2016')
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.2.3 beta (13.06.2016)'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_01(self):
        changes = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_02(self):
        changes = [u'Исправление ошибок.',
                   u'Добавлена новая возможность.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0

* Исправление ошибок.
* Добавлена новая возможность.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_date(self):
        changes = [u'Исправление ошибок.',
                   u'Добавлена новая возможность.']
        version_1 = VersionInfo(Version(1, 0),
                                date_str=u'1 мая 2016',
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0 (1 мая 2016)

* Исправление ошибок.
* Добавлена новая возможность.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_versions_01(self):
        changes_1 = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes_1)

        changes_2 = [u'Исправление ошибок.',
                     u'Добавлена новая возможность.']
        version_2 = VersionInfo(Version(1, 1),
                                changes=changes_2)
        changelog = [version_1, version_2]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.1

* Исправление ошибок.
* Добавлена новая возможность.


!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result, changelog)

    def test_changelog_versions_02(self):
        changes_1 = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes_1)

        changes_2 = [u'Исправление ошибок.',
                     u'Добавлена новая возможность.']
        version_2 = VersionInfo(Version(1, 1),
                                changes=changes_2)
        changelog = [version_2, version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.1

* Исправление ошибок.
* Добавлена новая возможность.


!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result, changelog)


if __name__ == '__main__':
    unittest.main()
