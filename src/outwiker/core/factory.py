# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import os.path

from .exceptions import ReadonlyException


class PageFactory (object):
    """
    Класс для создания страниц
    """
    __metaclass__ = ABCMeta

    def create (self, parent, title, tags):
        """
        Создать страницу. Вызывать этот метод вместо конструктора
        """
        return PageFactory._createPage (self.getPageType(), parent, title, tags)


    @abstractmethod
    def getPageType (self):
        """
        Метод возвращает тип создаваемой страницы (не экземпляр страницы)
        """
        pass


    @abstractproperty
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        pass


    @abstractmethod
    def getPageView (self, parent):
        """
        Метод возвращает контрол, который будет отображать и редактировать страницу
        """
        pass


    @abstractmethod
    def getPrefPanels (self, parent):
        """
        Метод возвращает список страниц для окна настроек (или пустой список)
        """
        pass


    @staticmethod
    def _createPage (pageType, parent, title, tags):
        """
        Создать страницу по ее типу
        """
        if parent.readonly:
            raise ReadonlyException

        path = os.path.join (parent.path, title)

        page = pageType (path, title, parent)
        parent.addToChildren (page)

        try:
            page.initAfterCreating (tags)
        except Exception:
            parent.removeFromChildren (page)
            raise

        return page


    def getTypeString (self):
        return self.getPageType().getTypeString()
