# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.config import StringOption
from outwiker.pages.text.textpage import TextPageFactory
from .utils import removeDir


class ConfigPagesTest (unittest.TestCase):
    """
    Тесты, связанные с настройками страниц и вики в целом
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])


    def tearDown (self):
        removeDir (self.path)


    def testSetRootParams (self):
        param = StringOption (self.wikiroot.params, u"TestSection_1", u"value1", u"")
        param.value = u"Значение 1"

        self.assertEqual (param.value, u"Значение 1")

        # Прочитаем вики и проверим установленный параметр
        wiki = WikiDocument.create (self.path)

        param_new = StringOption (wiki.params, u"TestSection_1", u"value1", u"")
        self.assertEqual (param_new.value, u"Значение 1")


    def testSetPageParams (self):
        param = StringOption (self.wikiroot[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
        param.value = u"Значение 1"

        param2 = StringOption (self.wikiroot[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
        self.assertEqual (param.value, u"Значение 1")
        self.assertEqual (param2.value, u"Значение 1")

        # Прочитаем вики и проверим установленный параметр
        wiki = WikiDocument.load (self.path)
        param3 = StringOption (wiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")

        self.assertEqual (param3.value, u"Значение 1")


    def testSubwikiParams (self):
        """
        Проверка того, что установка параметров страницы как полноценной вики не портит исходные параметры
        """
        param = StringOption (self.wikiroot[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
        param.value = u"Значение 1"

        path = os.path.join (self.path, u"Страница 1")
        subwiki = WikiDocument.load (path)

        subwikiparam = StringOption (subwiki.params, u"TestSection_1", u"value1", u"")
        self.assertEqual (subwikiparam.value, u"Значение 1")

        # Добавим новый параметр
        subwikiparam1 = StringOption (subwiki.params, u"TestSection_1", u"value1", u"")
        subwikiparam2 = StringOption (subwiki.params, u"TestSection_2", u"value2", u"")
        subwikiparam2.value = u"Значение 2"

        self.assertEqual (subwikiparam1.value, u"Значение 1")
        self.assertEqual (subwikiparam2.value, u"Значение 2")

        # На всякий случай прочитаем вики еще раз
        wiki = WikiDocument.load (self.path)

        wikiparam1 = StringOption (wiki[u"Страница 1"].params, u"TestSection_1", u"value1", u"")
        wikiparam2 = StringOption (wiki[u"Страница 1"].params, u"TestSection_2", u"value2", u"")

        self.assertEqual (wikiparam1.value, u"Значение 1")
        self.assertEqual (wikiparam2.value, u"Значение 2")
