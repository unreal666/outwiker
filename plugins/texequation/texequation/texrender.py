# -*- coding: UTF-8 -*-

import os
import os.path
import subprocess
import hashlib

from outwiker.core.system import getOS


def getTexRender (thumb_path):
    """
    Возвращает класс для рендеринга формул в зависимости от операционки
    """
    if os.name == "nt":
        return MimeTexWindows(thumb_path)
    else:
        return MimeTexLinux(thumb_path)


class MimeTex (object):
    """
    Базовый класс для рендеринга формул
    В производных классах нужно опеределить свойства mimeTexPath
    """
    def __init__ (self, thumb_path):
        """
        thumb_path - путь до папки, где можно делать временные файлы, и где создается файл с картинкой
        """
        self.thumb_path = thumb_path

        # Имя временного файла
        self.tempFname = "__temp.tmp"

        self.fontsize = 3


    def makeImage (self, eqn):
        """
        eqn - выражение, которое нужно отрендерить
        """
        currentOS = getOS()

        temp_path = os.path.join (self.thumb_path, self.tempFname)

        imageName = self.getImageName (eqn)
        image_path = os.path.join (self.thumb_path, imageName)

        if os.path.exists (image_path):
            # Если такой файл уже есть, значит еще раз геренить такую формулу не надо
            return imageName

        with open (temp_path, "w") as fp:
            fp.write (eqn.encode("utf8"))

        # mimeTexPath нужно определить в производных классах
        mimeTexPath = self.mimeTexPath

        args = [mimeTexPath.encode (currentOS.filesEncoding),
                "-f", temp_path.encode (currentOS.filesEncoding),
                "-e", image_path.encode (currentOS.filesEncoding),
                "-s", str (self.fontsize)]

        self.run (args)
        return imageName


    def getImageName (self, eqn):
        md5 = hashlib.md5 (eqn.encode("utf8")).hexdigest()
        fname = u"eqn_{0}.gif".format (md5)
        return fname



class MimeTexWindows (MimeTex):
    """
    Класс для работы с mimeTex под Windows
    """
    @property
    def mimeTexPath (self):
        return os.path.join (os.path.dirname (__file__), u"tools", u"mimetex.exe")


    def run (self, args):
        """
        Вызов MimeTex
        """
        STARTF_USESHOWWINDOW = 1
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= STARTF_USESHOWWINDOW

        p = subprocess.Popen(args, startupinfo=startupinfo, shell=False)
        p.communicate()


class MimeTexLinux (MimeTex):
    """
    Класс для работы с mimeTex под Linux
    """
    @property
    def mimeTexPath (self):
        return "mimetex"


    def run (self, args):
        """
        Вызов MimeTex
        """
        p = subprocess.Popen(args, shell=False)
        p.communicate()
