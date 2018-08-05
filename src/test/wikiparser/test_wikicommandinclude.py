# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class WikiIncludeCommandTest(unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["text_utf8.txt", "text_utf8.txt2", "image.gif",
                 "текст_utf8.txt", "text_1251.txt", "html.txt",
                 "html_1251.txt", "wiki.txt"]

        fullFilesPath = [os.path.join(self.filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.testPage).attach(fullFilesPath)

    def tearDown(self):
        removeDir(self.path)

    def testIncludeCommand1(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand2(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt param param1="www" :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand3(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt2:)"""

        result_right = """бла-бла-бла
Текст2 в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand4(self):
        text = """бла-бла-бла
(:include Attach:text_utf8.txt2 param param1="www":)"""

        result_right = """бла-бла-бла
Текст2 в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand5(self):
        text = """бла-бла-бла
(:include Attach:текст_utf8.txt param param1="www":)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand6(self):
        text = """бла-бла-бла
(:include Attach:текст_utf8.txt :)"""

        result_right = """бла-бла-бла
Текст в 
кодировке UTF-8"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand7(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding=cp1251 :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand8(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding = "cp1251" :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand9(self):
        text = """бла-бла-бла
(:include Attach:text_1251.txt encoding="cp1251" :)"""

        result_right = """бла-бла-бла
Это текст
в кодировке 1251"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand10(self):
        text = """бла-бла-бла (:include Attach:html.txt htmlescape:)"""

        result_right = """бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand11(self):
        text = """бла-бла-бла (:include Attach:html_1251.txt htmlescape encoding="cp1251":)"""

        result_right = """бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommand12(self):
        text = """бла-бла-бла (:include Attach:wiki.txt wikiparse:)"""

        result_right = """бла-бла-бла <b>Этот текст содержит вики-нотацию</b>"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommandInvalid1(self):
        text = """бла-бла-бла(:include Attach:text_utf8_1.txt :)"""

        result_right = """бла-бла-бла"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommandInvalid2(self):
        text = """бла-бла-бла(:include Attach:image.gif :)"""

        result_right = """бла-бла-бла""" + "<b>Encoding error in file image.gif</b>"

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommandInvalid3(self):
        text = """бла-бла-бла(:include Attach:image.gif encoding=base64 :)"""

        result_right = """бла-бла-бла""" + "<b>Encoding error in file image.gif</b>"

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)

    def testIncludeCommandInvalid4(self):
        text = """бла-бла-бла (:include text_utf8.txt :) абырвалг"""

        result_right = """бла-бла-бла  абырвалг"""

        result = self.parser.toHtml(text)
        self.assertEqual(result, result_right, result)
