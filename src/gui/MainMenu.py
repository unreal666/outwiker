# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Feb  8 21:41:42 2011

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class MainMenu(wx.MenuBar):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MainMenu.__init__
		wx.MenuBar.__init__(self, *args, **kwds)
		self.fileMenu = wx.Menu()
		self.fileMenu.Append(self.ID_NEW, _("&New\tCtrl+N"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN, _(u"&Open…\tCtrl+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_OPEN_READONLY, _("Open &Read-only...\tCtrl+Shift+O"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_SAVE, _("&Save\tCtrl+S"), "", wx.ITEM_NORMAL)
		self.fileMenu.Append(self.ID_EXIT, _(u"&Exit…\tAlt+F4"), "", wx.ITEM_NORMAL)
		self.fileMenu.AppendSeparator()
		self.Append(self.fileMenu, _("&File"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(wx.ID_UNDO, _("&Undo\tCtrl+Z"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_REDO, _("&Redo\tCtrl+Y"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(wx.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_PREFERENCES, _("Pr&eferences...\tCtrl+F8"), "", wx.ITEM_NORMAL)
		self.Append(wxglade_tmp_menu, _("&Edit"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_ADDPAGE, _(u"Add &Sibling Page…\tCtrl+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ADDCHILD, _(u"Add &Child Page…\tCtrl+Shift+T"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_MOVE_PAGE_UP, _("Move Page Up\tCtrl+Shift+Up"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_MOVE_PAGE_DOWN, _("Move Page Down\tCtrl+Shift+Down"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_RENAME, _("Re&name Page\tF2"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_REMOVE_PAGE, _(u"Rem&ove Page…\tCtrl+Shift+Del"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_SORT_CHILDREN_ALPHABETICAL, _("Sort Children Pages Alphabetical"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_SORT_SIBLINGS_ALPHABETICAL, _("Sort Siblings Pages Alphabetical"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.AppendSeparator()
		wxglade_tmp_menu.Append(self.ID_EDIT, _(u"&Edit Page Properties…\tCtrl+E"), "", wx.ITEM_NORMAL)
		self.Append(wxglade_tmp_menu, _("&Tree"))
		self.toolsMenu = wx.Menu()
		self.toolsMenu.Append(self.ID_GLOBAL_SEARCH, _(u"&Global Search…\tCtrl+Shift+F"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_ATTACH, _(u"&Attach Files…\tCtrl+Alt+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_COPY_TITLE, _("Copy Page &Title to Clipboard\tCtrl+Shift+D"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPYPATH, _("Copy &Page Path to Clipboard\tCtrl+Shift+P"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_ATTACH_PATH, _("Copy Atta&ches Path to Clipboard\tCtrl+Shift+A"), "", wx.ITEM_NORMAL)
		self.toolsMenu.Append(self.ID_COPY_LINK, _("Copy Page &Link to Clipboard\tCtrl+Shift+L"), "", wx.ITEM_NORMAL)
		self.toolsMenu.AppendSeparator()
		self.toolsMenu.Append(self.ID_RELOAD, _("&Reload Wiki...\tCtrl+R"), "", wx.ITEM_NORMAL)
		self.Append(self.toolsMenu, _("T&ools"))
		self.bookmarksMenu = wx.Menu()
		self.bookmarksMenu.Append(self.ID_ADDBOOKMARK, _("&Add/Remove Bookmark\tCtrl+D"), "", wx.ITEM_NORMAL)
		self.bookmarksMenu.AppendSeparator()
		self.Append(self.bookmarksMenu, _("&Bookmarks"))
		wxglade_tmp_menu = wx.Menu()
		self.viewNotes = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_TREE, _("Notes &Tree"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewNotes)
		self.viewAttaches = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_ATTACHES, _("Attaches"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewAttaches)
		wxglade_tmp_menu.AppendSeparator()
		self.viewFullscreen = wx.MenuItem(wxglade_tmp_menu, self.ID_VIEW_FULLSCREEN, _("Fullscreen\tF11"), "", wx.ITEM_CHECK)
		wxglade_tmp_menu.AppendItem(self.viewFullscreen)
		self.Append(wxglade_tmp_menu, _("&View"))
		wxglade_tmp_menu = wx.Menu()
		wxglade_tmp_menu.Append(self.ID_HELP, _("&Help\tF1"), "", wx.ITEM_NORMAL)
		wxglade_tmp_menu.Append(self.ID_ABOUT, _(u"&About…\tCtrl+F1"), "", wx.ITEM_NORMAL)
		self.Append(wxglade_tmp_menu, _("&Help"))

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.onNew, id=self.ID_NEW)
		self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.onOpenReadOnly, id=self.ID_OPEN_READONLY)
		self.Bind(wx.EVT_MENU, self.onSave, id=self.ID_SAVE)
		self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_REDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_CUT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_COPY)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.onPreferences, id=self.ID_PREFERENCES)
		self.Bind(wx.EVT_MENU, self.onAddSiblingPage, id=self.ID_ADDPAGE)
		self.Bind(wx.EVT_MENU, self.onAddChildPage, id=self.ID_ADDCHILD)
		self.Bind(wx.EVT_MENU, self.onMovePageUp, id=self.ID_MOVE_PAGE_UP)
		self.Bind(wx.EVT_MENU, self.onMovePageDown, id=self.ID_MOVE_PAGE_DOWN)
		self.Bind(wx.EVT_MENU, self.onRename, id=self.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.onRemovePage, id=self.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_MENU, self.onSortChildrenAlphabetical, id=self.ID_SORT_CHILDREN_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onSortSiblingAlphabetical, id=self.ID_SORT_SIBLINGS_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onEditPage, id=self.ID_EDIT)
		self.Bind(wx.EVT_MENU, self.onGlobalSearch, id=self.ID_GLOBAL_SEARCH)
		self.Bind(wx.EVT_MENU, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.onCopyTitle, id=self.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.onCopyPath, id=self.ID_COPYPATH)
		self.Bind(wx.EVT_MENU, self.onCopyAttaches, id=self.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyLink, id=self.ID_COPY_LINK)
		self.Bind(wx.EVT_MENU, self.onReload, id=self.ID_RELOAD)
		self.Bind(wx.EVT_MENU, self.onBookmark, id=self.ID_ADDBOOKMARK)
		self.Bind(wx.EVT_MENU, self.onViewTree, self.viewNotes)
		self.Bind(wx.EVT_MENU, self.onViewAttaches, self.viewAttaches)
		self.Bind(wx.EVT_MENU, self.onFullscreen, self.viewFullscreen)
		self.Bind(wx.EVT_MENU, self.onHelp, id=self.ID_HELP)
		self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: MainMenu.__set_properties
		pass
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: MainMenu.__do_layout
		pass
		# end wxGlade

	def onNew(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onNew' not implemented!"
		event.Skip()

	def onOpen(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onOpen' not implemented!"
		event.Skip()

	def onOpenReadOnly(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onOpenReadOnly' not implemented!"
		event.Skip()

	def onSave(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onSave' not implemented!"
		event.Skip()

	def onExit(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onExit' not implemented!"
		event.Skip()

	def onStdEvent(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onStdEvent' not implemented!"
		event.Skip()

	def onPreferences(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onPreferences' not implemented!"
		event.Skip()

	def onAddSiblingPage(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onAddSiblingPage' not implemented!"
		event.Skip()

	def onAddChildPage(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onAddChildPage' not implemented!"
		event.Skip()

	def onMovePageUp(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onMovePageUp' not implemented!"
		event.Skip()

	def onMovePageDown(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onMovePageDown' not implemented!"
		event.Skip()

	def onRename(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onRename' not implemented!"
		event.Skip()

	def onRemovePage(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onRemovePage' not implemented!"
		event.Skip()

	def onSortChildrenAlphabetical(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onSortChildrenAlphabetical' not implemented!"
		event.Skip()

	def onSortSiblingAlphabetical(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onSortSiblingAlphabetical' not implemented!"
		event.Skip()

	def onEditPage(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onEditPage' not implemented!"
		event.Skip()

	def onGlobalSearch(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onGlobalSearch' not implemented!"
		event.Skip()

	def onAttach(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onAttach' not implemented!"
		event.Skip()

	def onCopyTitle(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onCopyTitle' not implemented!"
		event.Skip()

	def onCopyPath(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onCopyPath' not implemented!"
		event.Skip()

	def onCopyAttaches(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onCopyAttaches' not implemented!"
		event.Skip()

	def onCopyLink(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onCopyLink' not implemented!"
		event.Skip()

	def onReload(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onReload' not implemented!"
		event.Skip()

	def onBookmark(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onBookmark' not implemented!"
		event.Skip()

	def onViewTree(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onViewTree' not implemented!"
		event.Skip()

	def onViewAttaches(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onViewAttaches' not implemented!"
		event.Skip()

	def onFullscreen(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onFullscreen' not implemented!"
		event.Skip()

	def onHelp(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onHelp' not implemented!"
		event.Skip()

	def onAbout(self, event): # wxGlade: MainMenu.<event_handler>
		print "Event handler `onAbout' not implemented!"
		event.Skip()

# end of class MainMenu

