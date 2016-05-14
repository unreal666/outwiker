# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

__version__ = u'1.1.1'


if getCurrentVersion() < Version (1, 9, 0, 765, status=StatusSet.DEV):
    print ("HtmlFormatter plugin. OutWiker version requirement: 1.9.0.765")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginName (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"HtmlFormatter"


        @property
        def description (self):
            return _(u"Plugin for more punctual HTML generation")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/HtmlFormatterEn")


        def initialize(self):
            self._initlocale(u"htmlformatter")
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_(_)
