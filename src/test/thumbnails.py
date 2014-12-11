# -*- coding: UTF-8 -*-

import unittest
import os
import os.path
from tempfile import mkdtemp

from outwiker.pages.wiki.thumbnails import Thumbnails
from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment


class ThumbnailsTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.url1 = u"http://example.com"
        self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

        self.__createWiki()

        self.parser = Parser(self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        removeDir (self.path)

    def testThumbnails1 (self):
        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=False)

        self.assertEqual (thumbDir,
                          os.path.join (Attachment (self.parser.page).getAttachPath(), Thumbnails.thumbDir),
                          thumbDir)


    def testThumbnails2 (self):
        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=False)

        self.assertFalse (os.path.exists (thumbDir))


    def testThumbnails3 (self):
        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=True)

        self.assertTrue (os.path.exists (thumbDir))


    def testThumbnailsClear1 (self):
        thumb = Thumbnails (self.parser.page)
        thumb.clearDir ()

        self.assertFalse (os.path.exists (thumb.getThumbPath (create=False)))


    def testThumbnailsClear2 (self):
        thumb = Thumbnails (self.parser.page)

        eqn = "y = f(x)"

        text = "{$ %s $}" % (eqn)
        self.parser.toHtml (text)

        self.assertFalse (len (os.listdir (thumb.getThumbPath (False))) == 0)

        thumb.clearDir()

        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 0)


    def testThumbnailsClear3 (self):
        thumb = Thumbnails (self.parser.page)

        eqn1 = "y = f(x)"
        eqn2 = "y = f_2(x)"

        self.parser.toHtml ("{$ %s $}" % (eqn1))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)

        self.parser.toHtml ("{$ %s $}" % (eqn2))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)


    def testThumbnails1_attach (self):
        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=False)

        self.assertEqual (thumbDir,
                          os.path.join (Attachment (self.parser.page).getAttachPath(), Thumbnails.thumbDir),
                          thumbDir)


    def testThumbnails2_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=False)

        self.assertFalse (os.path.exists (thumbDir))


    def testThumbnails3_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)
        thumbDir = thumb.getThumbPath (create=True)

        self.assertTrue (os.path.exists (thumbDir))


    def testThumbnailsClear1_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)
        thumb.clearDir ()

        self.assertFalse (os.path.exists (thumb.getThumbPath (create=False)))


    def testThumbnailsClear2_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)

        eqn = "y = f(x)"

        text = "{$ %s $}" % (eqn)
        self.parser.toHtml (text)

        self.assertFalse (len (os.listdir (thumb.getThumbPath (False))) == 0)

        thumb.clearDir()

        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 0)


    def testThumbnailsClear3_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)

        eqn1 = "y = f(x)"
        eqn2 = "y = f_2(x)"

        self.parser.toHtml ("{$ %s $}" % (eqn1))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)

        self.parser.toHtml ("{$ %s $}" % (eqn2))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)
