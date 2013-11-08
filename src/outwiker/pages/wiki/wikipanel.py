#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import os

from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.config import Config, StringOption
from outwiker.core.tree import RootWikiPage
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style

from .wikieditor import WikiEditor
from .wikitoolbar import WikiToolBar
from .thumbdialogcontroller import ThumbDialogController
from .linkcreator import LinkCreator
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator


class WikiPagePanel (BaseHtmlPanel):
    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1


    def __init__ (self, parent, *args, **kwds):
        super (WikiPagePanel, self).__init__ (parent, *args, **kwds)

        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7

        self._wikiPanelName = "wiki"
        self._fontSizeList = [u"20%", u"40%", u"60%", u"80%", u"120%", u"140%", u"160%", u"180%", u"200%"]
        self._fontSizeFormat = [(u"[----", u"----]"),
                (u"[---", u"---]"),
                (u"[--", u"--]"),
                (u"[-", u"-]"),
                (u"[+", u"+]"),
                (u"[++", u"++]"),
                (u"[+++", u"+++]"),
                (u"[++++", u"++++]"),
                (u"[+++++", u"+++++]")]

        self.mainWindow.toolbars[self._wikiPanelName] = WikiToolBar(self.mainWindow, self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._wikiPanelName].UpdateToolBar()

        self.notebook.SetPageText (0, _(u"Wiki"))

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self.config = WikiConfig (Application.config)

        self.__createCustomTools()
        Application.mainWindow.updateShortcuts()

        if self.config.showHtmlCodeOptions.value:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()


    def onClose (self, event):
        if self._wikiPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._wikiPanelName)

        super (WikiPagePanel, self).onClose (event)


    @property
    def toolsMenu (self):
        return self.__wikiMenu


    def __createHtmlCodePanel (self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
        self.htmlCodeWindow.SetReadOnly (True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
        
        self.addPage (self.htmlCodeWindow, _("HTML"))
        return self.pageCount - 1
    

    def GetTextEditor(self):
        return WikiEditor


    def GetSearchPanel (self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self.selectedPageIndex == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

        return None


    def onTabChanged(self, event):
        if self._currentpage == None:
            return

        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            self._onSwitchToCode()

        elif self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()

        elif self.selectedPageIndex == self.htmlcodePageIndex:
            self._onSwitchCodeHtml()

        self.savePageTab(self._currentpage)


    def _onSwitchCodeHtml (self):
        assert self._currentpage != None

        self.Save()
        status_item = 0
        setStatusText (_(u"Page rendered. Please wait…"), status_item)
        Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

        try:
            self.currentHtmlFile = self.generateHtml (self._currentpage)
            self._showHtmlCode(self.currentHtmlFile)
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
        except OSError as e:
            MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)

        setStatusText (u"", status_item)
        Application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)

        self._enableAllTools ()
        self.htmlCodeWindow.SetFocus()
        self.htmlCodeWindow.Update()


    def _showHtmlCode (self, path):
        try:
            with open (path) as fp:
                text = unicode (fp.read(), "utf8")

                self.htmlCodeWindow.SetReadOnly (False)
                self.htmlCodeWindow.SetText (text)
                self.htmlCodeWindow.SetReadOnly (True)
        except IOError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)
        except OSError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        self.addTool (self.__fontMenu, 
                "ID_BOLD", 
                lambda event: self.codeEditor.turnText (u"'''", u"'''"), 
                _(u"Bold") + "\tCtrl+B", 
                _(u"Bold") + "  (Ctrl+B)", 
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_ITALIC", 
                lambda event: self.codeEditor.turnText (u"''", u"''"), 
                _(u"Italic") + "\tCtrl+I", 
                _(u"Italic") + "  (Ctrl+I)", 
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_BOLD_ITALIC", 
                lambda event: self.codeEditor.turnText (u"''''", u"''''"), 
                _(u"Bold italic") + "\tCtrl+Shift+I", 
                _(u"Bold italic") + "  (Ctrl+Shift+I)", 
                os.path.join (self.imagesDir, "text_bold_italic.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_UNDERLINE", 
                lambda event: self.codeEditor.turnText (u"{+", u"+}"), 
                _(u"Underline") + "\tCtrl+U", 
                _(u"Underline") + "  (Ctrl+U)", 
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_STRIKE", 
                lambda event: self.codeEditor.turnText (u"{-", u"-}"), 
                _(u"Strikethrough") + "\tCtrl+K", 
                _(u"Strikethrough") + "  (Ctrl+K)", 
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_SUBSCRIPT", 
                lambda event: self.codeEditor.turnText (u"'_", u"_'"), 
                _(u"Subscript") + "\tCtrl+=", 
                _(u"Subscript") + "  (Ctrl+=)", 
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__fontMenu, 
                "ID_SUPERSCRIPT", 
                lambda event: self.codeEditor.turnText (u"'^", u"^'"), 
                _(u"Superscript") + "\tCtrl++", 
                _(u"Superscript") + "  (Ctrl++)", 
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__fontMenu, 
                "ID_BIGFONT", 
                self.__onBigFont, 
                _(u"Big") + "\tCtrl+.", 
                _(u"Big font") + "  (Ctrl+.)", 
                os.path.join (self.imagesDir, "text_big.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__fontMenu, 
                "ID_SMALLFONT", 
                self.__onSmallFont, 
                _(u"Small") + "\tCtrl+,", 
                _(u"Small font") + "  (Ctrl+,)", 
                os.path.join (self.imagesDir, "text_small.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__fontMenu, 
                "ID_MONOSPACED", 
                lambda event: self.codeEditor.turnText (u"@@", u"@@"), 
                _(u"Monospaced") + "\tCtrl+7", 
                _(u"Monospaced") + "  (Ctrl+7)", 
                os.path.join (self.imagesDir, "text_monospace.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addAlignTools (self):
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_LEFT", 
                lambda event: self.codeEditor.turnText (u"%left%", u""), 
                _(u"Left align") + "\tCtrl+Alt+L", 
                _(u"Left align") + "  (Ctrl+Alt+L)", 
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_CENTER", 
                lambda event: self.codeEditor.turnText (u"%center%", u""), 
                _(u"Center align") + "\tCtrl+Alt+C", 
                _(u"Center align") + "  (Ctrl+Alt+C)", 
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_RIGHT", 
                lambda event: self.codeEditor.turnText (u"%right%", u""), 
                _(u"Right align") + "\tCtrl+Alt+R", 
                _(u"Right align") + "  (Ctrl+Alt+R)", 
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False,
                panelname="wiki")
    
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_JUSTIFY", 
                lambda event: self.codeEditor.turnText (u"%justify%", u""), 
                _(u"Justify align") + "\tCtrl+Alt+J", 
                _(u"Justify align") + "  (Ctrl+Alt+J)", 
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False,
                panelname="wiki")


    def __addFormatTools (self):
        self.addTool (self.__formatMenu, 
                "ID_PREFORMAT", 
                lambda event: self.codeEditor.turnText (u"[@", u"@]"), 
                _(u"Preformat [@…@]") + "\tCtrl+Alt+F", 
                _(u"Preformat [@…@]") + "  (Ctrl+Alt+F)",
                None,
                fullUpdate=False)

        self.addTool (self.__formatMenu, 
                "ID_NONFORMAT", 
                lambda event: self.codeEditor.turnText (u"[=", u"=]"), 
                _(u"Non-parsed [=…=]"), 
                _(u"Non-parsed [=…=]"), 
                None,
                fullUpdate=False,
                panelname="wiki")

    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__listMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'* '), 
                _(u"Bullets list") + "\tCtrl+G", 
                _(u"Bullets list") + "  (Ctrl+G)", 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__listMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'# '), 
                _(u"Numbers list") + "\tCtrl+J", 
                _(u"Numbers list") + "  (Ctrl+J)", 
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        self.addTool (self.__headingMenu, 
                "ID_H1", 
                lambda event: self.codeEditor.turnText (u"\n!! ", u""), 
                _(u"H1") + "\tCtrl+1", 
                _(u"H1") + "  (Ctrl+1)", 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"!!! ", u""), 
                _(u"H2") + "\tCtrl+2", 
                _(u"H2") + "  (Ctrl+2)", 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False,
                panelname="wiki")
        
        self.addTool (self.__headingMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"!!!! ", u""), 
                _(u"H3") + "\tCtrl+3", 
                _(u"H3") + "  (Ctrl+3)", 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"!!!!! ", u""), 
                _(u"H4") + "\tCtrl+4", 
                _(u"H4") + "  (Ctrl+4)", 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"!!!!!! ", u""), 
                _(u"H5") + "\tCtrl+5", 
                _(u"H5") + "  (Ctrl+5)", 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"!!!!!!! ", u""), 
                _(u"H6") + "\tCtrl+6", 
                _(u"H6") + "  (Ctrl+6)", 
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        self.addTool (self.__wikiMenu, 
                "ID_THUMB", 
                self.__onThumb,
                _(u"Thumbnail") + "\tCtrl+M", 
                _(u"Thumbnail") + "  (Ctrl+M)", 
                os.path.join (self.imagesDir, "images.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINK", 
                self.__onInsertLink, 
                _(u"Link") + "\tCtrl+L", 
                _(u'Link') + "  (Ctrl+L)", 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'[[#', u']]'), 
                _(u"Anchor") + "\tCtrl+Alt+N",
                _(u'Anchor') + "  (Ctrl+Alt+N)", 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'----'), 
                _(u"Horizontal line") + "\tCtrl+H", 
                _(u"Horizontal line") + "  (Ctrl+H)", 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINEBREAK", 
                lambda event: self.codeEditor.replaceText (u'[[<<]]'), 
                _(u"Line break") + "\tCtrl+Return", 
                _(u"Line break") + "  (Ctrl+Return)", 
                os.path.join (self.imagesDir, "linebreak.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_EQUATION", 
                lambda event: self.codeEditor.turnText (u'{$', u'$}'), 
                _(u"Equation") + "\tCtrl+Q", 
                _(u'Equation') + "  (Ctrl+Q)", 
                os.path.join (self.imagesDir, "equation.png"),
                fullUpdate=False,
                panelname="wiki")

        self.__wikiMenu.AppendSeparator()

        self.addTool (self.__wikiMenu, 
                "ID_ESCAPEHTML", 
                self.codeEditor.escapeHtml, 
                _(u"Convert HTML Symbols"), 
                _(u"Convert HTML Symbols"), 
                None,
                fullUpdate=False,
                panelname="wiki")


    def __createCustomTools (self):
        assert self.mainWindow != None

        self.__wikiMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__commandsMenu = wx.Menu()

        self.mainWindow.Freeze()

        self._addRenderTools()

        self.addTool (self.__wikiMenu, 
                "ID_HTMLCODE", 
                self.__openHtmlCode, 
                _(u"HTML Code") + "\tShift+F4", 
                _(u"HTML Code") + "  (Shift+F4)", 
                os.path.join (self.imagesDir, "html.png"),
                True,
                fullUpdate=False,
                panelname=self.mainWindow.GENERAL_TOOLBAR_STR)

        self.addTool (self.__wikiMenu, 
                "ID_UPDATE_HTML", 
                self.__updateHtml, 
                _(u"Update HTML Code") + "\tCtrl+F4", 
                _(u"Update HTML Code") + "  (Ctrl+F4)", 
                None,
                True,
                fullUpdate=False,
                panelname="wiki")

        self.toolsMenu.AppendSeparator()

        self.__wikiMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__wikiMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__wikiMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__wikiMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__wikiMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__wikiMenu.AppendSubMenu (self.__commandsMenu, _(u"Commands"))

        self.__addCommandsTools()
        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()

        self.mainWindow.mainMenu.Insert (self.__WIKI_MENU_INDEX, 
                self.__wikiMenu, 
                _(u"Wiki") )

        self.mainWindow.Thaw()


    @property
    def commandsMenu (self):
        """
        Свойство возвращает меню с вики-командами
        """
        return self.__commandsMenu

    
    def __addCommandsTools (self):
        self.addTool (self.commandsMenu, 
                "ID_ATTACHLIST", 
                lambda event: self.codeEditor.replaceText (u"(:attachlist:)"), 
                _(u"Attachment (:attachlist:)"), 
                _(u"Attachment (:attachlist:)"), 
                None,
                fullUpdate=False)

        self.addTool (self.commandsMenu, 
                "ID_CHILDLIST", 
                lambda event: self.codeEditor.replaceText (u"(:childlist:)"), 
                _(u"Children (:childlist:)"), 
                _(u"Children (:childlist:)"), 
                None,
                fullUpdate=False)

        self.addTool (self.commandsMenu, 
                "ID_INCLUDE", 
                lambda event: self.codeEditor.turnText (u"(:include ", u":)"), 
                _(u"Include (:include ...:)"), 
                _(u"Include (:include ...:)"), 
                None,
                fullUpdate=False)


    @BaseHtmlPanel.selectedPageIndex.setter
    def selectedPageIndex (self, index):
        """
        Устанавливает выбранную страницу (код, просмотр или полученный HTML)
        """
        if index == self.HTML_RESULT_PAGE_INDEX and self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
            selectedPage = self.htmlcodePageIndex
        else:
            selectedPage = index

        BaseHtmlPanel.selectedPageIndex.fset (self, selectedPage)


    def __openHtmlCode (self, event):
        self.selectedPageIndex = self.HTML_RESULT_PAGE_INDEX

    
    def generateHtml (self, page):
        style = Style()
        stylepath = style.getPageStyle (page)
        generator = HtmlGenerator (page)

        try:
            html = generator.makeHtml(stylepath)
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),  
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

            html = generator.makeHtml (style.getDefaultStyle())

        return html


    def removeGui (self):
        super (WikiPagePanel, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__WIKI_MENU_INDEX - 1)

    
    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений

        Перегрузка метода из BaseTextPanel
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += "Attach:" + fnames[n]
            if n != count -1:
                text += "\n"

        return text


    def __onInsertLink (self, event):
        linkController = LinkDialogContoller (self, self.codeEditor.GetSelectedText())
        if linkController.showDialog() == wx.ID_OK:
            linkCreator = LinkCreator (self.config)
            text = linkCreator.create (linkController.link, linkController.comment)
            self.codeEditor.replaceText (text)


    def __onThumb (self, event):
        dlgController = ThumbDialogController (self, 
                self._currentpage, 
                self.codeEditor.GetSelectedText())

        if dlgController.showDialog() == wx.ID_OK:
            self.codeEditor.replaceText (dlgController.result)


    def __onBigFont (self, event):
        self.__selectFontSize (4)


    def __onSmallFont (self, event):
        self.__selectFontSize (3)


    def __selectFontSize (self, selIndex):
        dlg = wx.SingleChoiceDialog (self, 
                _(u"Select font size"),
                _(u"Font size"),
                self._fontSizeList)

        selectedText = self.codeEditor.GetSelectedText()

        dlg.SetSelection (selIndex)
        if dlg.ShowModal() == wx.ID_OK:
            sizeIndex = dlg.GetSelection()
            self.codeEditor.turnText (self._fontSizeFormat[sizeIndex][0], self._fontSizeFormat[sizeIndex][1])

        dlg.Destroy()


    def __updateHtml (self, event):
        """
        Сбросить кэш для того, чтобы заново сделать HTML
        """
        HtmlGenerator (self._currentpage).resetHash()
        if self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        elif self.selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            self._onSwitchCodeHtml()

