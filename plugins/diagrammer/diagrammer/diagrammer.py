# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

__version__ = u"1.0.3"


if getCurrentVersion() < Version (1, 8, 0, 735, status=StatusSet.DEV):
    print ("ChangeUID plugin. OutWiker version requirement: 1.8.0.735")
else:
    from .i18n import set_
    from .controller import Controller


    class PluginDiagrammer (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super (PluginDiagrammer, self).__init__ (application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Diagrammer"


        @property
        def description (self):
            return _(u"Plugin for the construction of diagrams")


        @property
        def version (self):
            return __version__


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/DiagrammerEn")


        def initialize(self):
            self._initlocale(self.name.lower())
            self.__correctSysPath()
            self.__controller.initialize()


        def __correctSysPath (self):
            cmd_folder = os.path.join (unicode (os.path.dirname(os.path.abspath(__file__)),
                                                getOS().filesEncoding),
                                       u"libs")

            syspath = [unicode (item, getOS().filesEncoding)
                       if not isinstance (item, unicode)
                       else item for item in sys.path]

            if cmd_folder not in syspath:
                sys.path.insert(0, cmd_folder)


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
