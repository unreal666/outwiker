# -*- coding: UTF-8 -*-

import os


# Supported Ubuntu releases
UBUNTU_RELEASE_NAMES = [u"wily", u"trusty", u"xenial"]

# List of the supported plugins
PLUGINS_LIST = [
    u"autorenamer",
    u"changepageuid",
    u"counter",
    u"diagrammer",
    u"datagraph",
    u"export2html",
    u"externaltools",
    u"htmlformatter",
    u"htmlheads",
    u"lightbox",
    u"livejournal",
    # u"markdown",
    u"pagetypecolor",
    u"readingmode",
    u"sessions",
    u"source",
    u"spoiler",
    u"statistics",
    u"style",
    u"thumbgallery",
    u"tableofcontents",
    u"texequation",
    u"updatenotifier",
    u"webpage",
]

BUILD_DIR = u'build'
LINUX_BUILD_DIR = u"outwiker_linux"
WINDOWS_BUILD_DIR = u"outwiker_win"
DEB_BINARY_BUILD_DIR = u'deb_binary'
DEB_SOURCE_BUILD_DIR = u'deb_source'
SOURCES_DIR = u'sources'
PLUGINS_DIR = u'plugins'
PLUGIN_VERSIONS_FILENAME = u'plugin.xml'
OUTWIKER_VERSIONS_FILENAME = u'versions.xml'

FILES_FOR_UPLOAD_UNSTABLE_WIN = [
    u'outwiker_win_unstable.7z',
    u'outwiker_win_unstable.exe',
    u'outwiker_win_unstable_all_plugins.7z',
    u'outwiker_win_unstable_all_plugins.zip',
    u'outwiker_win_unstable.zip',
]

# Timeout in seconds
DOWNLOAD_TIMEOUT = 15

# Parameters for deb building
TIMEZONE = '+0300'
try:
    DEB_MAINTAINER = os.environ['DEBFULLNAME']
except KeyError:
    DEB_MAINTAINER = u'Eugeniy Ilin'

try:
    DEB_MAINTAINER_EMAIL = os.environ['DEBEMAIL']
except KeyError:
    DEB_MAINTAINER_EMAIL = u'jenyay.ilin@gmail.com'
