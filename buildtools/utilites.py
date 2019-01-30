# -*- coding: UTF-8 -*-

from functools import wraps
import sys
import os
import os.path
import shutil

from fabric.api import local
from .libs.colorama import Fore


def addToSysPath(path):
    """
    Add path to sys.path to use outwiker modules
    """
    cmd_folder = os.path.abspath(path)

    syspath = [item
               if not isinstance(item, str)
               else item for item in sys.path]

    if cmd_folder not in syspath:
        sys.path.insert(0, cmd_folder)


def getPython():
    if os.name == 'posix':
        return u'python3'
    else:
        return u'python'


def execute(command):
    local(command)


def getCurrentUbuntuDistribName():
    with open('/etc/lsb-release') as fp:
        for line in fp:
            line = line.strip()
            if line.startswith(u'DISTRIB_CODENAME'):
                codename = line.split(u'=')[1].strip()
                return codename


def getPathToPlugin(plugin_name):
    return os.path.join(u'plugins', plugin_name, plugin_name)


def tobool(value):
    if isinstance(value, bool):
        return value

    true_list = [u'1', '1', u'true', 'true']

    if isinstance(value, str):
        return value.lower() in true_list

    return bool(value)


def remove(path):
    """
    Remove the fname file if it exists.
    The function not catch any exceptions.
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def print_info(text):
    print(Fore.GREEN + text)


def print_warning(text):
    print(Fore.YELLOW + text)


def print_error(text):
    print(Fore.RED + text)


def get_linux_distrib_info():
    fname = '/etc/lsb-release'
    with open(fname) as fp:
        lines = fp.readlines()

    result = {}
    for line in lines:
        if '=' not in line:
            continue

        line = line.strip()
        key, value = line.split('=')
        result[key] = value

    return result


def _os_only(func, os_str, name):
    '''
    Create decorator to mark task what it can be run in specified OS only.
        os_str - internal OS name from
            https://docs.python.org/2/library/sys.html#sys.platform
        name - OS name for users.
    '''
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not sys.platform.startswith(os_str):
            print_error(u'Error. This task can only be run on {name}.'.format(
                name=name
            ))
            sys.exit(1)
        else:
            return func(*args, **kwargs)

    return wrapped


def windows_only(func):
    '''
    Decorator to mark task what it can only be run on Windows.
    This decorator must be after @task decorator
    '''
    return _os_only(func, 'win32', u'Windows')


def linux_only(func):
    '''
    Decorator to mark task what it can onnly be run on Linux.
    This decorator must be after @task decorator
    '''
    return _os_only(func, 'linux', u'Linux')
