# -*- coding: utf-8 -*-

import urllib.parse
import subprocess
from io import StringIO

import wx

from outwiker.core.commands import MessageBox

from .commandparams import EXEC_BEGIN, PROTO_COMMAND
from ..config import ExternalToolsConfig
from ..i18n import get_


class CommandController(object):
    def __init__(self, application):
        self._application = application

    def initialize(self):
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onHoverLink += self._onHoverLink
        self._application.onLinkClick += self.onLinkClick

    def destroy(self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onHoverLink -= self._onHoverLink
        self._application.onLinkClick -= self.onLinkClick

    def __onWikiParserPrepare(self, parser):
        """
        Teh event occures before parsing. Add the (:exec:) command
        """
        from externaltools.commandexec.commandexec import CommandExec
        parser.addCommand(CommandExec(parser))

    def _getParams(self, url):
        """
        Return dictionary with params from url.
        Every value in dictionary is list
        """
        if isinstance(url, bytes):
            url = url.decode('utf8')

        if url is None or not url.startswith(EXEC_BEGIN):
            return {}

        startpos = url.find(u'?')

        if startpos == -1 or startpos == len(url) - 1:
            return {}

        params = url[startpos + 1:]

        try:
            paramsDict = urllib.parse.parse_qs(params)
        except ValueError:
            return {}

        return paramsDict

    def _onHoverLink(self, page, params):
        if params.link is None:
            return

        urlparams = self._getParams(params.link)
        if not urlparams:
            return

        commands = self.getCommandsList(urlparams)

        if commands:
            params.text = self.getStatusTitle(commands)

    def getStatusTitle(self, commands):
        """
        command - instance of the ExecInfo class
        """
        assert commands

        buf = StringIO()
        buf.write(u'>>> ')
        buf.write(self._getParamText(commands[0].command))

        for param in commands[0].params:
            buf.write(u' ')
            buf.write(self._getParamText(param))

        if len(commands) > 1:
            buf.write(u' ...')

        return buf.getvalue()

    def _getParamText(self, param):
        """
        Quote param if it contain a space
        """
        return u'"{}"'.format(param) if u' ' in param else param

    def onLinkClick(self, page, params):
        """
        Event handler for clicking on link
        """
        if params.link is None:
            return

        urlparams = self._getParams(params.link)
        if not urlparams:
            return

        params.process = True

        commands = self.getCommandsList(urlparams)
        config = ExternalToolsConfig(self._application.config)

        if len(commands) > 1:
            message = _(u'Run applications by ExternalTools plugin?\nIt may be unsafe.')
        else:
            message = _(u'Run application by ExternalTools plugin?\nIt may be unsafe.')

        if(config.execWarning and
                MessageBox(
                    message,
                    _(u'ExternalTools'),
                    wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT
                ) != wx.YES):
            return

        for command in commands:
            self._execute(command.command, command.params)

    def getCommandsList(self, urlparams):
        """
        Return list of the ExecInfo. Macros will be replaced in params
        urlparams is dictionary with params from url.
        """
        from externaltools.commandexec.execinfo import ExecInfo

        result = []

        comindex = 1
        comparams = PROTO_COMMAND.format(number=comindex)

        while comparams in urlparams:
            command = urlparams[comparams][0]
            params = [param for param in urlparams[comparams][1:]]

            result.append(ExecInfo(command, params))

            comindex += 1
            comparams = PROTO_COMMAND.format(number=comindex)

        return result

    def _execute(self, command, params):
        try:
            subprocess.Popen([command] + params)
        except(OSError, subprocess.CalledProcessError):
            pass
