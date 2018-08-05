# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.parser.tokenwikistyle import StyleGenerator
from outwiker.pages.wiki.wikistyleutils import (getCustomStylesNames,
                                                loadCustomStyles)
from outwiker.utilites.textfile import writeTextFile


class WikiStylesBlockTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create(self.path)
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница", [])
        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)

    def test_block_01(self):
        text = '''текст
%class-red%
бла-бла-бла
%%
'''
        result = '''текст
<div class="class-red">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_block_02(self):
        text = '''текст
%_class-red%
бла-бла-бла
%%
'''
        result = '''текст
<div class="_class-red">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_01_space(self):
        text = '''текст
% class-red%
бла-бла-бла
%%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_02_name(self):
        text = '''текст
%1class-red%
бла-бла-бла
%%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_03_name(self):
        text = '''текст
%абырвалг-class-red%
бла-бла-бла
%%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_04_space_begin(self):
        text = '''текст
 %class-red%
бла-бла-бла
%%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_05_space_end(self):
        text = '''текст
%class-red%
бла-бла-бла
 %%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_block_standard(self):
        text = '''текст
%red%
бла-бла-бла
%%
'''
        result = '''текст
<div style="color: red;">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_block_space_begin_right(self):
        text = '''текст
%red%  
бла-бла-бла
%%
'''
        result = '''текст
<div style="color: red;">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_block_space_end_right(self):
        text = '''текст
%red%
бла-бла-бла
%%   
текст
'''
        result = '''текст
<div style="color: red;">бла-бла-бла</div>текст
'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_block_space(self):
        text = '''текст
%red%    
бла-бла-бла
%%   
текст
'''
        result = '''текст
<div style="color: red;">бла-бла-бла</div>текст
'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_noparse_01(self):
        text = '''текст
%class-red%
бла-бла-бла
[=%%=]
'''
        result = '''текст
%class-red%
бла-бла-бла
%%
'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_with_thumbnails_before(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])
        text = '''текст %thumb width=32%Attach:icon.png%%
%class-red%
бла-бла-бла
%%
'''
        result = '''текст <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a>
<div class="class-red">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_with_thumbnails_after(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])
        text = '''текст
%class-red%
бла-бла-бла
%%
%thumb width=32%Attach:icon.png%%'''
        result = '''текст
<div class="class-red">бла-бла-бла</div><a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_with_thumbnails_inside(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])
        text = '''текст
%class-red%
бла-бла-бла %thumb width=32%Attach:icon.png%%
%%'''
        result = '''текст
<div class="class-red">бла-бла-бла <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a></div>'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_with_thumbnails_between(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])
        text = '''текст
%class-red%
бла-бла-бла
%%

%thumb width=32%Attach:icon.png%%

%class-red%
бла-бла-бла
%%'''
        result = '''текст
<div class="class-red">бла-бла-бла</div>
<a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a>

<div class="class-red">бла-бла-бла</div>'''
        self.assertEqual(result, self.parser.toHtml(text))


class WikiStylesInlineTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create(self.path)
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница", [])
        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def tearDown(self):
        removeDir(self.path)

    def test_style_01(self):
        text = "текст %class-red%бла-бла-бла%% текст"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_02(self):
        text = "текст %_class-red%бла-бла-бла%% текст"
        result = 'текст <span class="_class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_space_01(self):
        text = "текст %class-red% бла-бла-бла %% текст"
        result = 'текст <span class="class-red"> бла-бла-бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_01(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% бла%% текст"
        result = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_01_space(self):
        text = "текст %class-red% бла_class-red %class-blue% бла_class-blue %% бла %% текст"
        result = 'текст <span class="class-red"> бла_class-red <span class="class-blue"> бла_class-blue </span> бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_02(self):
        text = "текст %class-red%%class-blue%бла_class-blue%%%% текст"
        result = 'текст <span class="class-red"><span class="class-blue">бла_class-blue</span></span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_02_space(self):
        text = "текст %class-red% %class-blue% бла_class-blue %% %% текст"
        result = 'текст <span class="class-red"> <span class="class-blue"> бла_class-blue </span> </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_03(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% %class-yellow%бла_class-yellow%% бла-бла %% текст"
        result_valid = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> <span class="class-yellow">бла_class-yellow</span> бла-бла </span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_01(self):
        text = "текст %class-red%абыр валг [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абыр валг %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_02(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_03(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% 111 [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> 111 %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_04(self):
        text = "текст %class-red%абырвалг [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_05(self):
        text = "текст %class-red%абырвалг %class-yellow%текст class-yellow%% [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-yellow">текст class-yellow</span> %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_many_styles_01(self):
        text = "текст %class-red class-my%бла-бла-бла%% текст"
        result = 'текст <span class="class-red class-my">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_many_styles_02(self):
        text = "текст %class-my class-red%бла-бла-бла%% текст"
        result = 'текст <span class="class-my class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color(self):
        text = "текст %red%бла-бла-бла%% текст"
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color_upper(self):
        text = "текст %RED%бла-бла-бла%% текст"
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color_param_upper(self):
        text = "текст %color=RED%бла-бла-бла%% текст"
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color_param(self):
        text = "текст %color=red%бла-бла-бла%% текст"
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color_param_quote_single(self):
        text = "текст %color='red'%бла-бла-бла%% текст"
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color_param_quote_double(self):
        text = 'текст %color="red"%бла-бла-бла%% текст'
        result = 'текст <span style="color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_value_01(self):
        text = 'текст %color="#11AA55"%бла-бла-бла%% текст'
        result = 'текст <span style="color: #11aa55;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_value_02(self):
        text = 'текст %color="#11AA55"%бла-бла-бла%% текст %color="#22BB66"%бла-бла-бла%%'
        result = 'текст <span style="color: #11aa55;">бла-бла-бла</span> текст <span style="color: #22bb66;">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_value_repeat_01(self):
        text = 'текст %color=#11AA55%бла-бла-бла%% текст %color="#11AA55"%бла-бла-бла%%'
        result = 'текст <span style="color: #11aa55;">бла-бла-бла</span> текст <span style="color: #11aa55;">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_value_number(self):
        text = 'текст %#11AA55%бла-бла-бла%% текст'
        result = 'текст <span style="color: #11aa55;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_bgcolor_value_number_01(self):
        text = 'текст %bgcolor=#11AA55%бла-бла-бла%% текст'
        result = 'текст <span style="background-color: #11aa55;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_bgcolor_value_number_02(self):
        text = 'текст %bgcolor="#11AA55"%бла-бла-бла%% текст'
        result = 'текст <span style="background-color: #11aa55;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_bgcolor_value_name(self):
        text = 'текст %bgcolor="red"%бла-бла-бла%% текст'
        result = 'текст <span style="background-color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_bgcolor_standard_name_01(self):
        text = 'текст %bg-red%бла-бла-бла%% текст'
        result = 'текст <span style="background-color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_bgcolor_standard_name_02(self):
        text = 'текст %bg_red%бла-бла-бла%% текст'
        result = 'текст <span style="background-color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_bgcolor_standard(self):
        text = 'текст %blue bg_red%бла-бла-бла%% текст'
        result = 'текст <span style="color: blue; background-color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_color_bgcolor_01(self):
        text = 'текст %blue bgcolor=red%бла-бла-бла%% текст'
        result = 'текст <span style="color: blue; background-color: red;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_user_style_01(self):
        text = 'текст %style="font-weight: bold;"%бла-бла-бла%% текст'
        result = 'текст <span style="font-weight: bold;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_user_style_02(self):
        text = 'текст %blue style="font-weight: bold"%бла-бла-бла%% текст'
        result = 'текст <span style="color: blue; font-weight: bold;">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_multiline_01(self):
        text = '''текст
%class-red%
бла-бла-бла
бла-бла-бла
%% текст
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_multiline_02(self):
        text = '''текст
%class-red% текст
бла-бла-бла
%%
'''
        result = '''текст
<span class="class-red"> текст
бла-бла-бла
</span>
'''
        self.assertEqual(result, self.parser.toHtml(text))

    def test_multiline_03_space_line_start(self):
        text = '''текст
   %class-red%
бла-бла-бла
%%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_multiline_04_space_line_start(self):
        text = '''текст
%class-red%
бла-бла-бла
    %%
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_multiparagraph_01(self):
        text = '''текст
%class-red%
бла-бла-бла

бла-бла-бла
%% текст
'''
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_noparse_01(self):
        text = 'текст %class-red%бла-бла-бла[=%%=] текст'
        result = 'текст %class-red%бла-бла-бла%% текст'
        self.assertEqual(result, self.parser.toHtml(text))

    def test_noparse_02(self):
        text = 'текст %class-red%бла-бла-бла [= =]%% текст'
        result = 'текст <span class="class-red">бла-бла-бла  </span> текст'
        self.assertEqual(result, self.parser.toHtml(text))

    def test_noparse_03(self):
        text = 'текст %class-red%бла-бла-бла [= =]%% текст %class-red%бла-бла-бла%%'
        result = 'текст <span class="class-red">бла-бла-бла  </span> текст <span class="class-red">бла-бла-бла</span>'
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_01_space(self):
        text = 'текст % class-red%бла-бла-бла%% текст'
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_02_space(self):
        text = 'текст %1class-red%бла-бла-бла%% текст'
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_invalid_03_space(self):
        text = 'текст %русс-red%бла-бла-бла%% текст'
        result = text
        self.assertEqual(result, self.parser.toHtml(text))

    def test_thumbnail_before(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])

        text = "текст %thumb width=32%Attach:icon.png%% %class-red%бла-бла-бла%% текст"
        result = 'текст <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a> <span class="class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_thumbnail_after(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])

        text = "текст %class-red%бла-бла-бла%% текст %thumb width=32%Attach:icon.png%%"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a>'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_thumbnail_inside(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])

        text = "текст %class-red%бла-бла-бла %thumb width=32%Attach:icon.png%%%% текст"
        result = 'текст <span class="class-red">бла-бла-бла <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a></span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_thumbnail_between(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])

        text = "текст %class-red%бла-бла-бла%% текст %thumb width=32%Attach:icon.png%% %class-red%бла-бла-бла%%"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a> <span class="class-red">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_thumbnail_serial(self):
        Attachment(self.testPage).attach(['../test/images/icon.png'])

        text = "текст %class-red%бла-бла-бла%% текст %thumb width=32%Attach:icon.png%% %class-red%бла-бла-бла%% %thumb width=32%Attach:icon.png%%"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a> <span class="class-red">бла-бла-бла</span> <a href="__attach/icon.png"><img src="__attach/__thumb/th_width_32_icon.png"/></a>'

        self.assertEqual(result, self.parser.toHtml(text))


class StyleGeneratorTest(unittest.TestCase):
    def test_style_color_name(self):
        style_generator = StyleGenerator({})
        params = [('red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red;')

    def test_style_color_name_param(self):
        style_generator = StyleGenerator({})
        params = [('color', 'red')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red;')

    def test_style_color_value_01(self):
        style_generator = StyleGenerator({})
        params = [('color', '#1A5')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: #1A5;')

    def test_style_color_value_02(self):
        style_generator = StyleGenerator({})
        params = [('color', '#11AA55')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: #11AA55;')

    def test_style_color_value_many(self):
        style_generator = StyleGenerator({})

        params_1 = [('color', '#11AA55')]
        classes, css_list, style = style_generator.getStyle(params_1)
        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: #11AA55;')

        params_2 = [('color', '#22BB66')]
        classes, css_list, style = style_generator.getStyle(params_2)
        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: #22BB66;')

    def test_style_bgcolor_name(self):
        style_generator = StyleGenerator({})
        params = [('bgcolor', 'red')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'background-color: red;')

    def test_style_bgcolor_value(self):
        style_generator = StyleGenerator({})
        params = [('bgcolor', '#10AA30')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'background-color: #10AA30;')

    def test_style_bgcolor_name_01(self):
        style_generator = StyleGenerator({})
        params = [('bg-red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'background-color: red;')

    def test_style_bgcolor_name_02(self):
        style_generator = StyleGenerator({})
        params = [('bg_red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'background-color: red;')

    def test_style_color_name_repeat_01(self):
        style_generator = StyleGenerator({})
        params = [('bg-red', '')]

        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'background-color: red;')

    def test_style_color_bgcolor_name_01(self):
        style_generator = StyleGenerator({})
        params = [('red', ''), ('bg_blue', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red; background-color: blue;')

    def test_style_color_bgcolor_name_02(self):
        style_generator = StyleGenerator({})
        params = [('red', ''), ('bgcolor', '#10aa30')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red; background-color: #10aa30;')

    def test_user_style__01(self):
        style_generator = StyleGenerator({})
        params = [('style', 'font-weight: bold;')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'font-weight: bold;')

    def test_user_style_02(self):
        style_generator = StyleGenerator({})
        params = [('style', 'font-weight: bold;'), ('red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red; font-weight: bold;')

    def test_user_style_03(self):
        style_generator = StyleGenerator({})
        params = [('style', 'font-weight: bold'), ('red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red; font-weight: bold;')

    def test_user_style_04(self):
        style_generator = StyleGenerator({})
        params = [
            ('style', 'font-weight: bold;'),
            ('red', ''),
            ('bg-blue', '')
        ]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, [])
        self.assertEqual(css_list, [])
        self.assertEqual(style, 'color: red; background-color: blue; font-weight: bold;')

    def test_custom_style_01_empty(self):
        style_generator = StyleGenerator({})
        params = [('my-red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, ['my-red'])
        self.assertEqual(css_list, [])
        self.assertEqual(style, '')

    def test_custom_style_02(self):
        style_generator = StyleGenerator({'my-red': 'test'})
        params = [('my-red', '')]
        classes, css_list, style = style_generator.getStyle(params)

        self.assertEqual(classes, ['my-red'])
        self.assertEqual(css_list, ['test'])
        self.assertEqual(style, '')


class WikiStyleUtilsTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dirs = []

    def tearDown(self):
        for dirname in self._tmp_dirs:
            removeDir(dirname)

    def test_getCustomStylesNames_empty(self):
        styles = getCustomStylesNames(self._tmp_dirs)
        self.assertEqual(styles, [])

    def test_getCustomStylesNames_empty_dirs(self):
        for n in range(5):
            dirname = mkdtemp()
            self._tmp_dirs.append(dirname)

        styles = getCustomStylesNames(self._tmp_dirs)
        self.assertEqual(styles, [])

    def test_getCustomStylesNames_single_dir(self):
        dirname = mkdtemp()
        self._tmp_dirs.append(dirname)

        writeTextFile(os.path.join(dirname, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname, 'style-3.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3'])

    def test_getCustomStylesNames_more_dirs(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), '')

        writeTextFile(os.path.join(dirname_2, 'style-4.css'), '')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3',
                                  'style-4', 'style-5'])

    def test_getCustomStylesNames_more_dirs_repeat_names(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), '')

        writeTextFile(os.path.join(dirname_2, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3', 'style-5'])

    def test_loadCustomStyles_empty(self):
        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {})

    def test_loadCustomStyles_empty_dirs(self):
        for n in range(5):
            dirname = mkdtemp()
            self._tmp_dirs.append(dirname)

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {})

    def test_loadCustomStyles_single_dir(self):
        dirname = mkdtemp()
        self._tmp_dirs.append(dirname)

        writeTextFile(os.path.join(dirname, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname, 'style-3.css'), 'test-3')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  })

    def test_loadCustomStyles_more_dirs(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), 'test-3')

        writeTextFile(os.path.join(dirname_2, 'style-4.css'), 'test-4')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), 'test-5')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  'style-4': 'test-4',
                                  'style-5': 'test-5',
                                  })

    def test_loadCustomStyles_more_dirs_repeat_names(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), 'test-3')

        writeTextFile(os.path.join(dirname_2, 'style-1.css'), 'test-1-new')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), 'test-5')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1-new',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  'style-5': 'test-5',
                                  })
