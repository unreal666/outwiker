# -*- coding: utf-8 -*-

from outwiker.core.i18n import init_i18n, getLanguageFromConfig
from outwiker.core.config import Config
from outwiker.core.event import Event, CustomEvents
from outwiker.core.recent import RecentWiki
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.pageuiddepot import PageUidDepot


class ApplicationParams(object):
    def __init__(self):
        # Current at given time wiki
        self.__wikiroot = None

        # Application's main window
        self.__mainWindow = None

        # Application's global config
        self.config = None
        self.recentWiki = None
        self.actionController = None
        self.plugins = PluginsLoader(self)
        self.pageUidDepot = PageUidDepot()

        # Anchor for transition during the opening other page
        self._anchor = None

        self.customEvents = CustomEvents()

        # Events

        # Opening wiki event
        # Parameters:
        #     root - opened wiki root(it may be None)
        self.onWikiOpen = Event()

        # Closing wiki event
        # Parameters:
        #     root - closed wiki root(it may be None)
        self.onWikiClose = Event()

        # Updating page wiki event
        # Parameters:
        #     sender - updated page
        #     **kwargs
        # kwargs contain 'change' key, which contain changing flags
        self.onPageUpdate = Event()

        # Creating new wiki page
        # Parameters:
        #     sender - new page
        self.onPageCreate = Event()

        # Tree updating event
        # Parameters:
        #     sender - Page, because of which the tree is updated.
        self.onTreeUpdate = Event()

        # Other page selection event
        # Parameters:
        #     sender - selected page
        self.onPageSelect = Event()

        # User want insert link to selected attached files to page
        # Parameters:
        #     fnames - selected file names(names only, without full paths)
        self.onAttachmentPaste = Event()

        # Changings in the bookmarks list event
        # Parameters:
        #     bookmark - Bookmarks class instance
        self.onBookmarksChanged = Event()

        # Removing the page event
        # Parameters:
        #     page - page is removed
        self.onPageRemove = Event()

        # Renaming page event
        # Parameters:
        #     page - page is renamed,
        #     oldSubpath - previous relative path to page
        self.onPageRename = Event()

        # Beginning complex tree updating(updating of several steps) event
        # Parameters:
        #     root - wiki tree root
        self.onStartTreeUpdate = Event()

        # Finishing complex tree updating(updating of several steps) event
        # Parameters:
        #     root - wiki tree root
        self.onEndTreeUpdate = Event()

        # Beginning HTML rendering event
        # Parameters:
        #   page - rendered page
        #   htmlView - window for HTML view
        self.onHtmlRenderingBegin = Event()

        # Finishing HTML rendering event
        # Parameters:
        #   page - rendered page
        #   htmlView - window for HTML view
        self.onHtmlRenderingEnd = Event()

        # Changing page order event
        # Parameters:
        #     page - page with changed order
        self.onPageOrderChange = Event()

        # Evont for forced saving page state
        # (e.g. by the loss the focus or by timer)
        # Parameters:
        #     --
        self.onForceSave = Event()

        # The event occurs after wiki parser(Parser cllass) creation,
        # but before it using
        # Parameter:
        #     parser - Parser class instance
        self.onWikiParserPrepare = Event()

        # Event occurs during preferences dialog creation
        # Parameters:
        #     dialog - outwiker.gui.preferences.prefdialog.PrefDialog
        #              class instance
        self.onPreferencesDialogCreate = Event()

        # Event occurs after preferences dialog closing.
        # Parameters:
        #     dialog - outwiker.gui.preferences.prefdialog.PrefDialog
        #              class instance
        self.onPreferencesDialogClose = Event()

        # Event occurs after(!) the page view creation
        # (inside CurrentPagePanel instance)
        # Parameters:
        #     page - new selected page
        self.onPageViewCreate = Event()

        # Event occurs before(!) the page view removing
        # (inside CurrentPagePanel instance)
        # Parameters:
        #     page - Current selected page
        self.onPageViewDestroy = Event()

        # Event occurs after the popup menu creation by right mouse click
        # on the notes tree
        # Parameters:
        #     menu - created popup menu,
        #     page - the page on which was right clicked in the notes tree
        self.onTreePopupMenu = Event()

        # Event occurs after the popup menu creation by right mouse click
        # on the tree
        # Parameters:
        #     menu - created popup menu,
        #     tray - the OutwikerTrayIcon class instance
        self.onTrayPopupMenu = Event()

        # Event occurs before HTML generation(for wiki and HTML pages)
        # Order of the calling preprocessing events is not regulated
        # Parameters:
        #    page - page for which HTML is generated
        #    params - instance of the outwiker.core.events.PreprocessingParams
        #             class
        self.onPreprocessing = Event()

        # Event occurs after HTML generation(for wiki and HTML pages)
        # Order of the calling preprocessing events is not regulated
        # Parameters:
        #    page - page for which HTML is generated
        #    params - instance of the outwiker.core.events.PostprocessingParams
        #             class
        self.onPostprocessing = Event()

        # Event occurs during HtmlImproverFactory instance creation
        # Parameters:
        #     factory - HtmlImproverFactory instance in which can add
        #     the new HtmlImprover instances by add() method
        self.onPrepareHtmlImprovers = Event()

        # Event occurs after wiki parsing but before HTML improveing
        # Parameters:
        #     page - page for which HTML is generated
        #     params - instance of the
        #              outwiker.core.events.PreHtmlImprovingParams class
        self.onPreHtmlImproving = Event()

        # Event occurs when cursor hovers under link on preview tab
        # Parameters:
        #     page - current page
        #     params - instance of the outwiker.core.events.HoverLinkParams
        #              class
        self.onHoverLink = Event()

        # Event occurs when user click to link on a page
        # Parameters:
        #     page - current page
        #     params - instance of the outwiker.core.events.LinkClickParams
        #              class
        self.onLinkClick = Event()

        # Event occurs when user click with right button in text editor
        # Parameters:
        #     page - current page
        #     params - instance of the the
        #              outwiker.core.events.EditorPopupMenuParams class
        self.onEditorPopupMenu = Event()

        # Event occurs after page dialog creation
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogInitParams class
        self.onPageDialogInit = Event()

        # Event occurs before page dialog will be destroyed
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogDestroyParams class
        self.onPageDialogDestroy = Event()

        # Event occurs after page type changing
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageTypeChangedParams class
        self.onPageDialogPageTypeChanged = Event()

        # Event occurs after page type changing
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageTitleChangedParams class
        self.onPageDialogPageTitleChanged = Event()

        # Event occurs after page style changing
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageStyleChangedParams class
        self.onPageDialogPageStyleChanged = Event()

        # Event occurs after page icon changing
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageIconChangedParams class
        self.onPageDialogPageIconChanged = Event()

        # Event occurs after page tag list changing
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageTagsChangedParams class
        self.onPageDialogPageTagsChanged = Event()

        # Event occurs during page dialog initialization,
        # during general panel creation. Evens sender expect what event
        # handlers will fill the page factories list with addPageFactory method
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageDialogPageFactoriesNeededParams
        #              class
        self.onPageDialogPageFactoriesNeeded = Event()

        # Event occurs by TextEditor when it needs styles
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the EditorStyleNeededParams class
        self.onEditorStyleNeeded = Event()

        # Event forces update and render current page
        # Parameters:
        #     page - current(selected) page
        #     params - instance of the PageUpdateNeededParams class
        self.onPageUpdateNeeded = Event()

        # Event occurs before wiki opening
        # Parameters:
        #    page - current(selected) page
        #    params - instance of the PreWikiOpenParams class
        self.onPreWikiOpen = Event()

        # Event occurs before wiki opening
        # Parameters:
        #    page - current(selected) page
        #    params - instance of the PostWikiOpenParams class
        self.onPostWikiOpen = Event()

    def init(self, configFilename):
        """
        Initialize config and locale
        """
        self.config = Config(configFilename)
        self.recentWiki = RecentWiki(self.config)
        self.__initLocale()

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value

    @property
    def wikiroot(self):
        """
        Возвращает корень открытой в данный момент вики или None,
        если нет открытой вики
        """
        return self.__wikiroot

    @wikiroot.setter
    def wikiroot(self, value):
        """
        Установить текущую вики
        """
        self.onWikiClose(self.__wikiroot)

        if self.__wikiroot is not None:
            self.__unbindWikiEvents(self.__wikiroot)

        self.__wikiroot = value

        if self.__wikiroot is not None:
            self.__bindWikiEvents(self.__wikiroot)

        self.pageUidDepot = PageUidDepot(self.__wikiroot)
        self.onWikiOpen(self.__wikiroot)

    @property
    def mainWindow(self):
        """
        Возвращает главное окно программы или None, если оно еще не создано
        """
        return self.__mainWindow

    @mainWindow.setter
    def mainWindow(self, value):
        """
        Установить главное окно программы
        """
        self.__mainWindow = value

    def __bindWikiEvents(self, wiki):
        """
        Подписка на события, связанные с открытой вики для передачи их дальше
        """
        wiki.onPageSelect += self.onPageSelect
        wiki.onPageUpdate += self.onPageUpdate
        wiki.onTreeUpdate += self.onTreeUpdate
        wiki.onStartTreeUpdate += self.onStartTreeUpdate
        wiki.onEndTreeUpdate += self.onEndTreeUpdate
        wiki.onPageOrderChange += self.onPageOrderChange
        wiki.onPageRename += self.onPageRename
        wiki.onPageCreate += self.onPageCreate
        wiki.onPageRemove += self.onPageRemove
        wiki.bookmarks.onBookmarksChanged += self.onBookmarksChanged

    def __unbindWikiEvents(self, wiki):
        """
        Отписаться от события, связанных с открытой вики
        """
        wiki.onPageSelect -= self.onPageSelect
        wiki.onPageUpdate -= self.onPageUpdate
        wiki.onTreeUpdate -= self.onTreeUpdate
        wiki.onStartTreeUpdate -= self.onStartTreeUpdate
        wiki.onEndTreeUpdate -= self.onEndTreeUpdate
        wiki.onPageOrderChange -= self.onPageOrderChange
        wiki.onPageRename -= self.onPageRename
        wiki.onPageCreate -= self.onPageCreate
        wiki.onPageRemove -= self.onPageRemove
        wiki.bookmarks.onBookmarksChanged -= self.onBookmarksChanged

    @property
    def selectedPage(self):
        """
        Вернуть текущую страницу или None,
        если страница не выбрана или вики не открыта
        """
        if self.__wikiroot is None:
            return None

        return self.__wikiroot.selectedPage

    @selectedPage.setter
    def selectedPage(self, page):
        """
        Установить текущую страницу
        """
        if (self.__wikiroot is not None and
                self.__wikiroot.selectedPage != page):
            self.__wikiroot.selectedPage = page

    def __initLocale(self):
        """
        Инициализации локализаций интерфейса
        """
        language = getLanguageFromConfig(self.config)

        try:
            init_i18n(language)
        except IOError:
            print u"Can't load language: {}".format(language)

    def getEvent (self, name):
        """Return build-in event or custom event"""
        if hasattr (self, name) and isinstance (getattr (self, name), Event):
            return getattr (self, name)
        return self.customEvents.get(name)


Application = ApplicationParams()
