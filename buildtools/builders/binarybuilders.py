# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
from pathlib import Path
import shutil

from fabric.api import lcd, local

from buildtools.utilites import remove, print_info


class BaseBinaryBuilder(object, metaclass=ABCMeta):
    """Base class for any binary builders"""

    def __init__(self, src_dir, dest_dir, temp_dir):
        self._src_dir = src_dir
        self._dest_dir = dest_dir
        self._temp_dir = temp_dir

    @abstractmethod
    def build(self):
        pass

    def get_excludes(self):
        """Return modules list to exclude from build. """
        return [
            'Tkinter',
            'PyQt4',
            'PyQt5',
            'unittest',
            'sqlite3',
            'numpy',
            'pydoc',
            'test',
            'pycparser',
            'xmlrpclib',
            'bz2',
            'cffi',
            'bsddb',
            'PIL.SunImagePlugin',
            'PIL.IptcImagePlugin',
            'PIL.McIdasImagePlugin',
            'PIL.DdsImagePlugin',
            'PIL.FpxImagePlugin',
            'PIL.PixarImagePlugin',
        ]

    def get_includes(self):
        """Return modules list to include to build. """
        return [
            'importlib',
            'urllib',
            'outwiker.gui.htmlrenderfactory',
            'outwiker.gui.controls.popupbutton',
            'outwiker.utilites.actionsguicontroller',
            'outwiker.utilites.text',
            'PIL.Image',
            'PIL.ImageFile',
            'PIL.ImageDraw',
            'PIL.ImageDraw2',
            'PIL.ImageFont',
            'PIL.ImageFilter',
            'PIL.IcoImagePlugin',
            'PIL.PngImagePlugin',
            'PIL.BmpImagePlugin',
            'PIL.TiffImagePlugin',
            'PIL.JpegImagePlugin',
            'enchant',
            'xml',
            'json',
            'asyncio',
            'html.parser',
        ]

    def get_additional_files(self):
        return []

    def _copy_additional_files(self):
        root_dir = os.path.join(self._dist_dir, u'outwiker')

        for fname, subpath in self.get_additional_files():
            dest_dir = os.path.join(root_dir, subpath)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            print_info(u'Copy: {} -> {}'.format(fname, dest_dir))
            shutil.copy(fname, dest_dir)


class BasePyInstallerBuilder(BaseBinaryBuilder, metaclass=ABCMeta):
    """Class for binary assimbling creation with PyParsing. """

    def __init__(self, src_dir, dest_dir, temp_dir):
        super(BasePyInstallerBuilder, self).__init__(
            src_dir, dest_dir, temp_dir)

        # The path where the folder with the assembly will be created
        # (before copying to self.dest_dir)
        # build/tmp/build
        self._dist_dir = os.path.join(temp_dir, u'build')

        # The path with the intermediate files (build info)
        # build/tmp/build_tmp
        self._workpath = os.path.join(temp_dir, u'build_tmp')

    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        return []

    def get_params(self):
        params = [u'--log-level WARN',
                  u'--clean',
                  u'--noconfirm',
                  u'--icon images/outwiker.ico',
                  u'--name outwiker',
                  u'--windowed',
                  u'--distpath "{}"'.format(self._dist_dir),
                  u'--workpath "{}"'.format(self._workpath),
                  u'--add-data versions.xml' + os.pathsep + u'.',
                  u'--add-binary help' + os.pathsep + u'help',
                  u'--add-binary iconset' + os.pathsep + u'iconset',
                  u'--add-binary images' + os.pathsep + u'images',
                  u'--add-binary locale' + os.pathsep + u'locale',
                  u'--add-binary spell' + os.pathsep + u'spell',
                  u'--add-binary styles' + os.pathsep + u'styles',
                  u'--add-binary textstyles' + os.pathsep + u'textstyles',
                  u'--add-binary plugins' + os.pathsep + u'plugins',
                  ]

        params += [u' --hiddenimport {}'.format(package)
                   for package
                   in self.get_includes()]

        params += [u' --exclude-module {}'.format(package)
                   for package
                   in self.get_excludes()]

        return params

    def build(self):
        params = self.get_params()
        command = u'pyinstaller runoutwiker.py ' + u' '.join(params)
        with lcd(self._src_dir):
            local(command)

        self._remove_files()
        self._copy_additional_files()

        print_info(u'Copy files to dest path.')
        shutil.copytree(
            os.path.join(self._dist_dir, u'outwiker'),
            self._dest_dir
        )

    def _remove_files(self):
        toRemove = [os.path.join(self._dist_dir, u'outwiker', fname)
                    for fname in self.get_remove_list()]

        for fname in toRemove:
            print_info(u'Remove: {}'.format(fname))
            remove(fname)

    def get_files_by_mask(self, directory, mask):
        return [str(fname.resolve()) for fname in Path(directory).glob(mask)]


class PyInstallerBuilderWindows(BasePyInstallerBuilder):
    def get_remove_list(self):
        """Return list of the files or dirs to remove after build."""
        to_remove = [
            u'_win32sysloader.pyd',
            u'win32com.shell.shell.pyd',
            u'win32trace.pyd',
            u'win32wnet.pyd',
            u'iconv.dll',
            u'_winxptheme.pyd',
            u'enchant/iconv.dll',
            u'enchant/share',
            u'enchant/lib/enchant/README.txt',
            u'mfc140u.dll',
            u'include',
        ]

        to_remove += [fname.name for fname
                      in Path(self._dist_dir, 'outwiker').glob('api-ms-win*.dll')]

        return to_remove


class PyInstallerBuilderLinuxBase(BasePyInstallerBuilder):
    def get_remove_list(self):
        return [
            'lib',
            'include',
            '_codecs_cn.so',
            '_codecs_hk.so',
            '_codecs_iso2022.so',
            '_codecs_jp.so',
            '_codecs_kr.so',
            '_codecs_tw.so',

            # libstdc++.so.6, libgio-2.0.so.0 etc must be excluded
            # else application will be fall
            'libstdc++.so.6',
            'libgio-2.0.so.0',
            'libc.so.6',
            'libgdk_pixbuf-2.0.so.0',
            'libz.so.1',
            'libglib-2.0.so.0',

            # List of excludes from AppImage recomendations
            # https://github.com/AppImage/AppImages/blob/master/excludelist

            'libgobject-2.0.so.0',
            'libGL.so.1',
            'libEGL.so.1',
            'libdrm.so.2',
            'libX11.so.6',
            'libasound.so.2',
            'libfontconfig.so.1',
            'libexpat.so.1',
            'libgcc_s.so.1',
            'libgpg-error.so.0',
            'libICE.so.6',
            'libSM.so.6',
            'libuuid.so.1',
            'libgpg-error.so.0',
            'libX11-xcb.so.1',
            'libfreetype.so.6',

            'libfreetype-550560cb.so',
            # 'libgbm.so.1',
            # 'libglapi.so.0',

            # 'libxcb.so.1',
        ]

    def build(self):
        super(PyInstallerBuilderLinuxBase, self).build()
        self._strip_binary()

    def _strip_binary(self):
        strip_path = Path(self._dest_dir)
        files_for_strip = (list(strip_path.glob('libwx*.so.*')) +
                           list(strip_path.glob('wx.*so')))

        for fname in files_for_strip:
            print_info(u'Strip {}'.format(fname))
            if os.path.exists(str(fname)):
                local(u'strip -s -o "{fname}" "{fname}"'.format(fname=fname))

    def get_includes(self):
        result = super().get_includes()
        result.append('hunspell')
        # result.append('gi')
        # result.append('gi.repository.Gtk')
        # result.append('gi.repository.GdkPixbuf')
        return result

    def append_so_files(self, files, modules_dir, dir_dest):
        so_files = self.get_files_by_mask(modules_dir, '*.so')
        files += [(fname, dir_dest) for fname in so_files]


class PyInstallerBuilderLinuxSimple(PyInstallerBuilderLinuxBase):
    pass

    # def get_additional_files(self):
    #     files = []
    #     self._append_pixbuf_files(files)
    #     self._append_immodules_files(files)
    #     return files
    #
    # def _append_immodules_files(self, files):
    #     dir_dest = u'lib/immodules'
    #     modules_dir = u'/usr/lib/x86_64-linux-gnu/gtk-3.0/3.0.0/immodules/'
    #
    #     files.append(('need_for_build/linux/immodules.cache', dir_dest))
    #     self.append_so_files(files, modules_dir, dir_dest)
    #
    # def _append_pixbuf_files(self, files):
    #     dir_dest = u'lib/gdk-pixbuf'
    #     modules_dir = u'/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders'
    #
    #     files.append(('need_for_build/linux/loaders.cache', dir_dest))
    #     self.append_so_files(files, modules_dir, dir_dest)
    #
    # def get_params(self):
    #     params = super().get_params()
    #     params.append(u'--runtime-hook=linux_runtime_hook.py')
    #     return params
