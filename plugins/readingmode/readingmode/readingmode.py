# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version


__version__ = u"1.0.2"

if getCurrentVersion() < Version (1, 8, 0, 742):
    print ("ReadingMode. OutWiker version requirement: 1.8.0.742")
else:
    from outwiker.core.system import getOS
    from controller import Controller
    from .i18n import set_

    class PluginReadingMode (Plugin):
        """
        ReadingMode Plugin
        """
        def __init__ (self, application):
            super (PluginReadingMode, self).__init__ (application)
            self._controller = Controller (application)


        @property
        def name (self):
            return u"ReadingMode"


        @property
        def description (self):
            return _(u'''Plugin disables the panel "Tree", "Tag", "Attach Files" without changing the geometry of the main window.''')


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/ReadingModeEn")


        @property
        def version (self):
            return __version__


        def initialize (self):
            if self._application.mainWindow is not None:
                self._initlocale(u"readingmode")

            self._controller.initialize()


        def destroy (self):
            self._controller.destroy()


        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException, e:
                print e

            set_(_)
