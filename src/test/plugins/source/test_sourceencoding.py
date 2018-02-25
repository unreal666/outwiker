# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeDir


class SourceEncodingPluginTest(unittest.TestCase):
    """
    Тесты на работу с разными кодировками в плагине Source
    """
    def setUp(self):
        self.__pluginname = "Source"

        self.__createWiki()

        dirlist = ["../plugins/source"]

        # Путь, где лежат примеры исходников в разных кодировках
        self.samplefilesPath = "../test/samplefiles/sources"

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.config = self.loader[self.__pluginname].config
        self.config.tabWidth.value = 4
        self.config.defaultLanguage.remove_option()

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def testHighlightFileEncoding1(self):
        """
        Явное задание кодировки
        """
        Attachment(self.testPage).attach([os.path.join(self.samplefilesPath, "source_cp1251.cs")])
        content = '(:source file="source_cp1251.cs"  encoding="cp1251":)'
        self.testPage.content = content

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue('<span class="k">using</span> <span class="nn">System.Collections.Generic</span><span class="p">;</span>' in result)
        self.assertTrue('Ошибка соединения с сервером' in result)

    def testHighlightFileEncoding2(self):
        """
        Явное задание неправильной кодировки
        """
        Attachment(self.testPage).attach([os.path.join(self.samplefilesPath, "source_cp1251.cs")])
        content = '(:source file="source_cp1251.cs"  encoding="utf8":)'
        self.testPage.content = content

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue('<span class="k">using</span> <span class="nn">System.Collections.Generic</span><span class="p">;</span>' not in result)
        self.assertTrue('Ошибка соединения с сервером' not in result)

        self.assertTrue('Source' in result)

    def testHighlightFileEncoding3(self):
        """
        Явное задание неправильной кодировки(которой нет в списке кодировок)
        """
        Attachment(self.testPage).attach([os.path.join(self.samplefilesPath, "source_cp1251.cs")])
        content = '(:source file="source_cp1251.cs"  encoding="blablabla":)'
        self.testPage.content = content

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue('<span class="k">using</span> <span class="nn">System.Collections.Generic</span><span class="p">;</span>' not in result)
        self.assertTrue('Ошибка соединения с сервером' not in result)

        self.assertTrue('Source' in result)

    def testHighlightFileEncoding4(self):
        """
        Явное задание неправильной кодировки(которой нет в списке кодировок)
        """
        Attachment(self.testPage).attach([os.path.join(self.samplefilesPath, "source_utf8.py")])
        content = '(:source file="source_utf8.py"  encoding="blablabla":)'
        self.testPage.content = content

        generator = HtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue('<span class="kn">import</span> <span class="nn">os.path</span>' not in result)

        self.assertTrue('<span class="bp">self</span><span class="o">.</span><span class="n">__correctSysPath</span><span class="p">()</span>' not in result)

        self.assertTrue('Уничтожение(выгрузка) плагина.' not in result)

        self.assertTrue('Source' in result)
