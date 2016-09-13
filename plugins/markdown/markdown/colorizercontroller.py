# -*- coding: UTF-8 -*-

import threading

from outwiker.gui.basetextstylingcontroller import BaseTextStylingController
from outwiker.pages.wiki.wikieditor import WikiEditor

from .colorizer import MarkdownColorizer


class ColorizerController(BaseTextStylingController):
    """Controller for colorize text in Markdown editor"""

    def getColorizingThread(self, page, params, runEvent):
        if isinstance(params.editor, WikiEditor):
            return threading.Thread(
                None,
                self._colorizeThreadFunc,
                args=(params.text,
                      params.editor,
                      params.editor.colorizeSyntax,
                      params.editor.enableSpellChecking,
                      runEvent)
            )
        else:
            return None

    def _colorizeThreadFunc(self,
                            text,
                            editor,
                            colorizeSyntax,
                            enableSpellChecking,
                            runEvent):
        colorizer = MarkdownColorizer(editor,
                                      colorizeSyntax,
                                      enableSpellChecking,
                                      runEvent)
        stylebytes = colorizer.colorize(text)

        if self._runColorizingEvent.is_set():
            self.updateStyles(editor,
                              text,
                              stylebytes,
                              stylebytes,
                              0,
                              len(text))
