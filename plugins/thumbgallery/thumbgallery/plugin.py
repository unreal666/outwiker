# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginThumbGallery(Plugin):
    """
    Плагин, добавляющий обработку команды (:thumblist:) и (:thumbgallery:)
        в википарсер
    """
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self._controller = Controller(self, application)

    @property
    def name(self):
        return u"ThumbGallery"

    @property
    def description(self):
        return self._loadDescription()

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()

    @property
    def url(self):
        return _(u"https://jenyay.net/Outwiker/ThumbGalleryEn")

    def _loadDescription(self):
        """
        Загрузить описание плагина из файла
        """
        path = _(u"locale/description.html")
        fullpath = os.path.join(self.pluginPath, path)

        try:
            with open(fullpath, encoding='utf8') as fp:
                return fp.read()
        except IOError:
            return _(u"Can't load description")
