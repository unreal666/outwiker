# -*- coding: UTF-8 -*-
"""Classes for parsing data"""

from abc import ABCMeta, abstractmethod
import re
import codecs


class BaseSource (object):
    __meta__ = ABCMeta


    def __init__ (self, colsep, skiprows=0):
        # colsep - reg. exp. for separate the columns
        self._colsep = colsep
        self._rowSeparator = r'(?:\r\n)|(?:\n)|(?:\r)'
        self._skipRows = skiprows

        self._colRegExp = re.compile (self._colsep, re.I | re.M)
        self._rowRegExp = re.compile (self._rowSeparator, re.I | re.M)


    @abstractmethod
    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        pass


    def splitItems (self, line):
        """Return list of the row elements
        line - line (row) of the data"""
        items = [item.strip() for item in self._colRegExp.split (line) if len (item.strip()) != 0]

        return items


class StringSource (BaseSource):
    """
    Get data from command context
    """
    def __init__ (self, text, colsep=r'\s+', skiprows=0):
        super (StringSource, self).__init__(colsep, skiprows)
        self._text = text


    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        colsCount = None
        start = 0
        finish = False

        if len (self._text.strip()) == 0:
            raise StopIteration

        linenumber = -1
        while not finish:
            linenumber += 1

            match = self._rowRegExp.search (self._text, start)

            if match is None:
                line = self._text[start:].strip()
                finish = True
            else:
                line = self._text[start: match.start()].strip()
                start = match.end()

            if linenumber < self._skipRows:
                continue

            # Skip empty lines
            if len (line) == 0:
                if finish:
                    break
                else:
                    continue

            # All rows must contain the same columns count
            items = self.splitItems (line)
            if colsCount is None:
                colsCount = len (items)
            elif len (items) != colsCount:
                break

            yield items



class FileSource (BaseSource):
    """
    Get data from text file
    """
    def __init__ (self, filename, colsep=r'\s+', skiprows=0):
        super (FileSource, self).__init__(colsep, skiprows)
        self._filename = filename


    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        colsCount = None

        try:
            linenumber = -1
            with codecs.open (self._filename, 'r', 'utf8') as fp:
                while True:
                    linenumber += 1

                    line = fp.readline()
                    if len (line) == 0:
                        break

                    if linenumber < self._skipRows:
                        continue

                    # Skip empty lines
                    if len (line.strip()) == 0:
                        continue

                    # All rows must contain the same columns count
                    items = self.splitItems (line.strip())
                    if colsCount is None:
                        colsCount = len (items)
                    elif len (items) != colsCount:
                        break

                    yield items
        except (IOError, SystemError, UnicodeDecodeError):
            pass
