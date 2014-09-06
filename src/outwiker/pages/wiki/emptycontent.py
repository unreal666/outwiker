# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption


class EmptyContent (object):
    """
    Класс для работы с шаблоном, который будет показан вместо пустой страницы
    """
    def __init__ (self, config):
        self.config = config
        self.contentDefault = _(u"""!!! Attachment\n(:attachlist:)\n----\n!!! Child pages\n(:childlist:)""")
        self.configSecton = u"Wiki"
        self.configParam = u"EmptyContent"
        self.option = StringOption (self.config, self.configSecton, self.configParam, self.contentDefault)


    @property
    def content (self):
        return self.option.value


    @content.setter
    def content (self, value):
        self.option.value = value
