# -*- coding: utf-8 -*-

from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.wiki.defines import MENU_WIKI
from outwiker.utilites.actionsguicontroller import (ActionsGUIController,
                                                    ActionGUIInfo)

from .i18n import get_
from .commands import (TitleCommand, DescriptionCommand,
                       KeywordsCommand, CustomHeadsCommand,
                       HtmlAttrsCommand)
from .actions import (TitleAction,
                      DescriptionAction,
                      KeywordsAction,
                      CustomHeadsAction,
                      HtmlAttrsAction)
from . import defines


class Controller(object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__(self, plugin, application):
        """
        plugin - Владелец контроллера(экземпляр класса PluginSource)
        application - экземпляр класса ApplicationParams
        """
        self._plugin = plugin
        self._application = application

        self._commands = (TitleCommand,
                          DescriptionCommand,
                          KeywordsCommand,
                          CustomHeadsCommand,
                          HtmlAttrsCommand)
        self._actions = (TitleAction,
                         DescriptionAction,
                         KeywordsAction,
                         CustomHeadsAction,
                         HtmlAttrsAction)

        self._GUIController = ActionsGUIController(
            self._application,
            WikiWikiPage.getTypeString(),
        )

    def initialize(self):
        """
        Инициализация контроллера при активации плагина.
        Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._initialize_guicontroller()

    def _initialize_guicontroller(self):
        action_gui_info = list(ActionGUIInfo(action(self._application),
                                             defines.MENU_HTMLHEADS,
                                            )
                               for action in self._actions)

        new_menus = [(defines.MENU_HTMLHEADS, _('HTML Headers'), MENU_WIKI)]

        if self._application.mainWindow is not None:
            self._GUIController.initialize(action_gui_info,
                                           new_menus=new_menus)

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._destroy_guicontroller()

    def _destroy_guicontroller(self):
        if self._application.mainWindow is not None:
            self._GUIController.destroy()

    def __onWikiParserPrepare(self, parser):
        """
        Вызывается до разбора викитекста. Добавление команды(:counter:)
        """
        list(parser.addCommand(command(parser)) for command in self._commands)
