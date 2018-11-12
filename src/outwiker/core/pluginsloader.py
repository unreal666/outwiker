# -*- coding: utf-8 -*-

import os
import os.path
import sys
import traceback
import logging
import importlib
import pkgutil
import collections

import outwiker.core
import outwiker.gui
import outwiker.pages
import outwiker.actions
import outwiker.utilites
import outwiker.libs

import outwiker.core.packageversion as pv

from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.pluginbase import Plugin, InvalidPlugin
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.utilites.textfile import readTextFile

logger = logging.getLogger('outwiker.core.pluginsloader')


class EnabledPlugins(collections.UserDict):
    """
    Container for enabled plugins
    value.initialize() is called when new key is added.
    value.destroy() is called when key is deleted.
    """
    def __setitem__(self, key, value):
        value.initialize()
        super(EnabledPlugins, self).__setitem__(key, value)

    def __delitem__(self, key):
        if key in self:
            self[key].destroy()
        super(EnabledPlugins, self).__delitem__(key)


class PluginsLoader(object):
    """
    Load and keep plugins.
    for loading all plugins packages from folder 'foo'
        plugins = PluginsLoader(wx.app).load(['foo'])
    """

    def __init__(self, application):
        self.__application = application

        # Dict with enable plugins
        # {<plugin name>: <object implementing Plugin interface>}
        self.__plugins = EnabledPlugins()

        # Dict with enable plugins
        # {<plugin name>: <object implementing Plugin interface>}
        self.__disabledPlugins = {}

        # View for all successful loaded plugins
        self.__loadedPlugins = collections.ChainMap(self.__plugins,
                                                    self.__disabledPlugins)

        # The list of the InvalidPlugin instance.
        self.__invalidPlugins = []

        # if True - the errors will be printed
        self.enableOutput = True

        # aliases
        self.get = self.__loadedPlugins.get

    def _print(self, text):
        if self.enableOutput:
            logger.error(text)

    #############################
    # plugin's repository methods
    #############################
    @property
    def loadedPlugins(self):
        """
        Return dict with successful loaded plugins
        """
        return self.__loadedPlugins

    @property
    def disabledPlugins(self):
        """
        Return dict with disabled plugins
        """
        return self.__disabledPlugins

    @property
    def invalidPlugins(self):
        """
        Return list with invalid plugins
        """
        return self.__invalidPlugins

    def remove(self, pluginName):
        """
        Remove pluginName instance

        :return:
            True - if plugin was removed
            None - if plugin name is absent in plugin list
        """
        if pluginName in self.loadedPlugins:
            if not self.__disabledPlugins.pop(pluginName, None):
                del self.__plugins[pluginName]
            return True

    def clear(self):
        """
        Uninstall all active plugins and clear plugins list
        """
        self.__plugins.clear()
        self.__disabledPlugins.clear()
        self.__invalidPlugins.clear()

    def disable(self, plugin_name):
        """ Disable plugin_name """
        if plugin_name in self.__plugins:
            assert plugin_name not in self.__disabledPlugins
            self.__disabledPlugins[plugin_name] = self.__plugins.pop(plugin_name)

    def enable(self, plugin_name):
        """ Enable plugin_name """
        if plugin_name in self.__disabledPlugins:
            assert plugin_name not in self.__plugins
            self.__plugins[plugin_name] = self.__disabledPlugins.pop(plugin_name)

    def updateDisableList(self):
        """
        Enable/Disable plugins according to application.config: "disabledPlugins"
        """
        options = PluginsConfig(self.__application.config)
        disable_list = options.disabledPlugins.value

        for plugin_name in self.loadedPlugins:
            if plugin_name in disable_list:
                self.disable(plugin_name)
            else:
                self.enable(plugin_name)

    def __len__(self):
        return len(self.__plugins)

    def __getitem__(self, pluginname):
        return self.__plugins[pluginname]

    def __iter__(self):
        return iter(self.__plugins.values())

    ############################
    # import plugins methods
    ###########################

    def load(self, dirlist):
        """
        :param dirlist:
            List of paths from where plugins packages should be loaded.
            For example to load 3 plugins the dirlist should be ['/path1', '/path2']
            /path1/
                plugin1/
                    plugin.py
                    plugin.xml
                plugin2/
                    plugin.py
                    plugin.xml
            /path2/
                plugin3/
                    plugin.py
                    plugin.xml
        :return:
            function return None
            the installed plugins can be get by properties
        """
        assert dirlist is not None

        logger.debug(u'Plugins loading started')

        for currentDir in reversed(dirlist):
            if os.path.exists(currentDir):

                # Add currentDir to sys.path
                fullpath = os.path.abspath(currentDir)
                if fullpath not in sys.path:
                    sys.path.insert(0, fullpath)

                # Get list of submodules in currentDir
                # only folders with __init__.py can be submodules
                packagesList = [pkg_name for _, pkg_name, is_pkg in
                                pkgutil.iter_modules([currentDir]) if is_pkg]

                for packageName in packagesList:
                    packagePath = os.path.join(currentDir, packageName)
                    self.__importPackage(packagePath)

        logger.debug(u'Plugins loading ended')

    def __loadPluginInfo(self, plugin_fname):
        if not os.path.exists(plugin_fname):
            return None

        xml_content = readTextFile(plugin_fname)
        appinfo = XmlVersionParser().parse(xml_content)
        return appinfo

    def __checkPackageVersions(self, appinfo):
        if appinfo is None:
            return pv.PLUGIN_MUST_BE_UPGRADED

        api_required_version = appinfo.requirements.api_version
        if not api_required_version:
            api_required_version = [(0, 0)]

        return pv.checkVersionAny(outwiker.core.__version__,
                                  api_required_version)

    def __importPackage(self, packagePath):
        """
        Try to load plugin from packagePath

        :param packagePath:
            path to python package from where the plugin should be import
        :return:
            add packagePath to one of the following lists:
            - self.__plugins
            - self.__disabledPlugins
            - self.__invalidPlugins
        """
        # aliases
        join = os.path.join
        packageName = os.path.basename(packagePath)

        logger.debug(u'Trying to load the plug-in: {}'.format(
            packageName))

        # Check module 'plugin.py' name in package
        modules = [module for __, module, is_pkg
                   in pkgutil.iter_modules([packagePath])
                   if not is_pkg]

        if 'plugin' not in modules:
            logger.error('plugin.py was not found in the package {}'.format(
                packagePath))
            return

        # Checking information from plugin.xml file
        plugin_fname = join(packagePath,
                            PLUGIN_VERSION_FILE_NAME)
        try:
            appinfo = self.__loadPluginInfo(plugin_fname)
        except EnvironmentError:
            error = _(u'Plug-in "{}". Can\'t read "{}" file').format(
                packageName, PLUGIN_VERSION_FILE_NAME)

            self._print(error)
            self.__invalidPlugins.append(InvalidPlugin(packageName,
                                                       error))
            return

        versions_result = self.__checkPackageVersions(appinfo)

        pluginname = (appinfo.appname
                      if (appinfo is not None and
                          appinfo.appname is not None)
                      else packageName)

        pluginversion = (appinfo.currentVersionStr
                         if appinfo is not None
                         else None)

        if versions_result == pv.PLUGIN_MUST_BE_UPGRADED:
            error = _(u'Plug-in "{}" is outdated. Please, update the plug-in.').format(pluginname)
            self._print(error)

            self.__invalidPlugins.append(
                InvalidPlugin(pluginname,
                              error,
                              pluginversion)
            )
            return
        elif versions_result == pv.OUTWIKER_MUST_BE_UPGRADED:
            error = _(
                u'Plug-in "{}" is designed for a newer version OutWiker. Please, install a new OutWiker version.').format(
                pluginname)
            self._print(error)

            self.__invalidPlugins.append(
                InvalidPlugin(pluginname,
                              error,
                              pluginversion))
            return

        # List of import errors strings
        # Should be displayed only if a plugin was not loaded
        errors = []

        # Try to find plugin in package and
        # add the instance of the class list
        plugin = self.__loadPlugin(packageName + '.plugin', errors)
        if plugin:
            plugin.version = pluginversion

        # The errors should be printed if no plugins in the package
        if not plugin and errors:
            error = u"\n\n".join(errors)
            self._print(error)
            self._print(u"**********\n")

            self.__invalidPlugins.append(
                InvalidPlugin(appinfo.appname,
                              error,
                              appinfo.currentVersionStr))
        else:
            logger.debug(u'Successfully loaded plug-in: {}'.format(
                packageName))

    def __loadPlugin(self, module, errors):
        """
        Find Plugin class in module and try to make instance for it

        :param module:
            python module or package where can be a plugin
        :param errors:
            list where the errors will be saved
        :return:
            The instance of loaded plugin or None
        """
        rez = None
        try:
            module = importlib.import_module(module)

            options = PluginsConfig(self.__application.config)

            # del magic attributes to save time
            attributes = [attr for attr in dir(module)
                          if not attr.startswith("__")]

            for name in attributes:
                plugin = self.__createPlugin(module, name)

                if plugin and plugin.name not in self.loadedPlugins:
                    if plugin.name not in options.disabledPlugins.value:
                        self.__plugins[plugin.name] = plugin
                    else:
                        self.__disabledPlugins[plugin.name] = plugin
                    rez = plugin

        except BaseException as e:
            errors.append("*** Plug-in {package} loading error ***\n{package}/\n{error}\n{traceback}".format(
                package=module,
                error=str(e),
                traceback=traceback.format_exc()
            ))

        return rez

    def __createPlugin(self, module, name):
        """
        Create plugin instance if name is a subclass of Plugin

        :param module:
            module name
        :param name:
            attribute from the module
        :return:
            instance of name class or None
        """
        obj = getattr(module, name)
        if (isinstance(obj, type) and
                issubclass(obj, Plugin) and
                obj != Plugin):
            return obj(self.__application)

    def reload(self, pluginname):
        """
        Reload plugin module and plugin instance

        :param pluginname:
            name of the actual plugin
        :return:
            None
        """
        if pluginname in self.loadedPlugins:
            plugin = self.loadedPlugins[pluginname]

            plug_path = plugin.pluginPath
            module = sys.modules[plugin.__class__.__module__]

            # destroy plugin
            self.remove(pluginname)

            # reload module
            importlib.invalidate_caches()
            importlib.reload(module)

            # import plugin again
            self.__importPackage(plug_path)

    #######
    # Other
    # Seems the method should be move to outwiker.core.pluginbase
    #######
    def getInfo(self, pluginname, langlist=["en"]):
        """
        Retrieve a AppInfo for plugin_name

        :param pluginname:
            name of the loaded plugin
        :param lang:
            langlist - list of the languages name ("en", "ru_RU" etc)
        :return:
            AppInfo for pluginname
            if pluginname cannot be located, then None is returned.
        :exception IOError:
            if plugin.xml cannot be read
        """
        if pluginname in self.loadedPlugins:
            module = self.loadedPlugins[pluginname].__class__.__module__
        else:
            module = ''

        xml_content = pkgutil.get_data(module, PLUGIN_VERSION_FILE_NAME)
        if xml_content:
            return XmlVersionParser(langlist).parse(xml_content)
