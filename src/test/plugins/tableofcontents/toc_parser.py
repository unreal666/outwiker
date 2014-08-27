# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class TOC_ParserTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        self.pluginname = u"TableOfContents"
        dirlist = [u"../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testParser_01 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u""

        contents = parser.parse (text)

        self.assertEqual (contents, [])


    def testParser_02 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''  !! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (contents, [])

    def testParser_03 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u"Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")


    def testParser_04 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!!    Абырвалг    '''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u"Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")


    def testParser_05 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг 123'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")


    def testParser_06 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг\\
 123'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, u'''Абырвалг 123''')
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")


    def testParser_07 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг 123
!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_08 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''!! Абырвалг 123

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_09 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_10 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_11 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

[=   
dsfasdf
!! Это не заголовок

asdf
=]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_12 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)


    def testParser_13 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! [[#якорь1]]Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! [[#якорь2]] Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_14 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! [[# якорь1  ]]Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! [[#  якорь2   ]] Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_15 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[[#якорь1]]
!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2]]
!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_16 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[[#якорь1]]   
!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2]]   
!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_17 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123 [[#якорь1]]

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")



    def testParser_18 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123 [[#якорь1]]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]   

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_19 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг [=123=] [[#якорь1]]

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг [=123=]")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2")


    def testParser_20 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

   [=   
dsfasdf
!! Это не заголовок

asdf
   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_21 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

wdsdaf [=   
dsfasdf
!! Это не заголовок

asdf
asdfasdf   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")

    
    def testParser_22 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[= asfsaf fasdg=]

!! Абырвалг 123

wdsdaf [=   
dsfasdf
!! Это не заголовок

asdf
asdfasdf   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_23 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[= asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_24 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

 asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

=]'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_25 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

=]
 asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

=]'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_26 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[[#якорь1_2]]   
!! [[#якорь1_1]] Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2_2]]   
!!! Абырвалг 234 [[#якорь2_3]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"якорь1_1")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"якорь2_2")


    def testParser_27 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

!! Абырвалг 123

[@
!! Это не заголовок
@]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")


    def testParser_28 (self):
        parser = self.loader[self.pluginname].ContentsParser()

        text = u'''ывп ыфвп ваы

[=
!! Это не заголовок
=]

!! Абырвалг 123

[=
[@
!! Это не заголовок
@]
=]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, u"Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, u"")

        self.assertEqual (contents[1].title, u"Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, u"")
