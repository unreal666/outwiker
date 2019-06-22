#!/usr/bin/python
# -*- coding: utf-8 -*-


import builtins
import os
import os.path
import glob
import sys
import urllib.request
import urllib.error
import urllib.parse
import shutil

from fabric.api import local, lcd, settings, task, cd, put, hosts
from buildtools.libs.colorama import Fore
from buildtools.buildfacts import BuildFacts

from buildtools.utilites import (getPython,
                                 execute,
                                 tobool,
                                 print_info,
                                 print_warning,
                                 print_error,
                                 windows_only,
                                 linux_only
                                 )
from buildtools.defines import (
    BUILD_DIR,
    BUILD_LIB_DIR,
    DEB_BINARY_BUILD_DIR,
    PLUGINS_DIR,
    PLUGINS_LIST,
    PLUGIN_VERSIONS_FILENAME,
    FILES_FOR_UPLOAD_UNSTABLE_WIN,
    FILES_FOR_UPLOAD_STABLE_WIN,
    FILES_FOR_UPLOAD_UNSTABLE_LINUX,
    FILES_FOR_UPLOAD_STABLE_LINUX,
    NEED_FOR_BUILD_DIR,
    VM_BUILD_PARAMS,
    LINUX_BUILD_DIR,
    WINDOWS_BUILD_DIR,
    COVERAGE_PARAMS,
    LANGUAGES,
    SITE_CONTENT_BUILD_DIR,
    SITE_CONTENT_DIR,
)
from buildtools.versions import (getOutwikerVersion,
                                 getOutwikerVersionStr,
                                 downloadAppInfo,
                                 getLocalAppInfoList,
                                 )
from buildtools.builders import (BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderDebBinaryFactory,
                                 BuilderAppImage,
                                 BuilderSnap,
                                 SiteContentBuilder,
                                 SiteContentSource,
                                 )

from outwiker.utilites.textfile import readTextFile
from outwiker.core.xmlversionparser import XmlVersionParser

try:
    from buildtools.serverinfo import (DEPLOY_SERVER_NAME,
                                       DEPLOY_UNSTABLE_PATH,
                                       DEPLOY_STABLE_PATH,
                                       DEPLOY_HOME_PATH,
                                       DEPLOY_SITE,
                                       DEPLOY_PLUGINS_PACK_PATH,
                                       PATH_TO_WINDOWS_DISTRIBS,
                                       )
except ImportError:
    shutil.copyfile(u'buildtools/serverinfo.py.example',
                    u'buildtools/serverinfo.py')
    from buildtools.serverinfo import (DEPLOY_SERVER_NAME,
                                       DEPLOY_UNSTABLE_PATH,
                                       DEPLOY_STABLE_PATH,
                                       DEPLOY_HOME_PATH,
                                       DEPLOY_SITE,
                                       DEPLOY_PLUGINS_PACK_PATH,
                                       PATH_TO_WINDOWS_DISTRIBS,
                                       )

from buildtools.uploaders import BinaryUploader


@task
def plugins(updatedonly=False):
    '''
    Create an archive with plugins (7z required)
    '''
    builder = BuilderPlugins(updatedOnly=updatedonly)
    builder.build()


@task
def plugins_clear():
    '''
    Remove an archive with plugins (7z required)
    '''
    builder = BuilderPlugins()
    builder.clear()


@task
def sources(is_stable=False):
    '''
    Create the sources archives
    '''
    builder = BuilderSources(is_stable=tobool(is_stable))
    builder.build()


@task
def sources_clear():
    '''
    Remove the sources archives.
    '''
    builder = BuilderSources()
    builder.clear()


@task
@windows_only
def win(is_stable=False, skipinstaller=False, skiparchives=False):
    '''
    Build OutWiker for Windows
    '''
    builder = BuilderWindows(is_stable=tobool(is_stable),
                             create_archives=not tobool(skiparchives),
                             create_installer=not tobool(skipinstaller)
                             )
    builder.build()


@task
@windows_only
def win_clear():
    '''
    Remove assemblies under Windows
    '''
    builder = BuilderWindows()
    builder.clear()


@task
@linux_only
def linux_binary(is_stable=False, skiparchives=False):
    '''
    Assemble binary builds for Linux
    '''
    builder = BuilderLinuxBinary(is_stable=tobool(is_stable),
                                 create_archive=not tobool(skiparchives)
                                 )
    builder.build()


@task
@linux_only
def linux_clear():
    '''
    Remove binary builds for Linux
    '''
    builder = BuilderLinuxBinary()
    builder.clear()


@task
@linux_only
def locale():
    '''
    Update the localization file (outwiker.pot)
    '''
    with lcd("src"):
        local(r'find . -iname "*.py" | xargs xgettext -o locale/outwiker.pot')


@task(alias='plugin_locale')
@linux_only
def locale_plugin(pluginname=None):
    '''
    Create or update the localization file for pluginname plug-in
    '''
    plugins = [pluginname] if pluginname else PLUGINS_LIST

    for name in plugins:
        print_info(name)
        with lcd(os.path.join("plugins", name, name)):
            local(r'find . -iname "*.py" | xargs xgettext -o locale/{}.pot'.format(name))

            for lang in LANGUAGES:
                if os.path.exists(os.path.join('plugins', name, name, 'locale', lang)):
                    local(r'msgmerge -U -N --backup=none locale/{lang}/LC_MESSAGES/{pluginname}.po locale/{pluginname}.pot'.format(
                        pluginname=name, lang=lang))


@task
def run(args=u''):
    '''
    Run OutWiker from sources
    '''
    with lcd("src"):
        execute(u'{} runoutwiker.py {}'.format(getPython(), args))


@task
def test(*args):
    '''
    Run the unit tests
    '''
    command = getPython() if args else 'coverage run {}'.format(COVERAGE_PARAMS)

    with lcd('src'):
        local('{command} runtests.py {args}'.format(
            command=command, args=' '.join(args)))

    if len(args) == 0:
        test_build()


@task
def test_build(*args):
    '''
    Run the build unit tests
    '''
    _runTests(u'.', u'test_build_', '', *args)


def _runTests(testdir, prefix, section=u'', *args):
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob(u'{path}/{prefix}*.py'.format(path=testdir,
                                                        prefix=prefix))]
    files.sort()

    with lcd(testdir):
        if section:
            execute("{python} {prefix}{section}.py {params}".format(
                python=getPython(),
                prefix=prefix,
                section=section,
                params=u' '.join(args))
            )
        else:
            with settings(warn_only=True):
                for fname in files:
                    execute("{python} {fname} {params}".format(
                        python=getPython(),
                        fname=fname,
                        params=u' '.join(args))
                    )


@task
@linux_only
def deb_binary(is_stable=False):
    '''
    Create binary deb package
    '''
    builder = BuilderDebBinaryFactory.get_default(DEB_BINARY_BUILD_DIR,
                                                  tobool(is_stable))
    builder.build()
    print_info('Deb created: {}'.format(builder.get_deb_files()))


@task
@linux_only
def deb_binary_clear():
    '''
    Remove binary deb package
    '''
    builder = BuilderDebBinaryFactory.get_default()
    builder.clear()


@task
def clear():
    '''
    Remove artifacts after all assemblies
    '''
    plugins_clear()
    sources_clear()

    if sys.platform.startswith('linux'):
        linux_clear()
        # deb_clear()
        deb_binary_clear()
    elif sys.platform.startswith('win32'):
        win_clear()


@task
def site_versions():
    '''
    Compare current OutWiker and plugins versions with versions on the site
    '''
    app_list = getLocalAppInfoList()

    # Downloading versions info
    print(u'Downloading version info files...\n')
    print(u'{: <20}{: <20}{}'.format(u'Title',
                                     u'Deployed version',
                                     u'Dev. version'))
    print(u'-' * 60)
    for localAppInfo in app_list:
        url = localAppInfo.updatesUrl
        name = localAppInfo.appname

        print(u'{:.<20}'.format(name), end=u'')
        try:
            appinfo = downloadAppInfo(url)
            if appinfo.currentVersion == localAppInfo.currentVersion:
                font = Fore.GREEN
            else:
                font = Fore.RED

            print(u'{siteversion:.<20}{devversion}'.format(
                siteversion=str(appinfo.currentVersion),
                devversion=font + str(localAppInfo.currentVersion)
                ))
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print(Fore.RED + u'Error')
            print(str(e))
            print(url)
            print('')


@task
def create_tree(maxlevel, nsiblings, path):
    '''
    Create wiki tree for the tests
    '''
    from outwiker.core.tree import WikiDocument

    builtins._ = _empty
    wikiroot = WikiDocument.create(path)
    _create_tree(1, int(maxlevel), int(nsiblings), wikiroot)


def _empty(param):
    return param


def _create_tree(level, maxlevel, nsiblings, parent):
    from outwiker.pages.wiki.wikipage import WikiPageFactory

    if level <= maxlevel:
        for n in range(nsiblings):
            pagename = u'page_{:03g}_{:03g}'.format(level, n)
            print(u'Create page {}'.format(pagename))

            newpage = WikiPageFactory().create(parent, pagename, [])
            newpage.content = u'Абырвалг'
            newpage.icon = u'images/outwiker_16.png'
            _create_tree(level + 1, maxlevel, nsiblings, newpage)


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_plugin(*args):
    '''
    Upload plugin to site
    '''
    if len(args) == 0:
        args = PLUGINS_LIST

    version_str = getOutwikerVersionStr()

    for pluginname in args:
        path_to_plugin_local = os.path.join(BUILD_DIR,
                                            version_str,
                                            PLUGINS_DIR,
                                            pluginname)

        if not os.path.exists(path_to_plugin_local):
            continue

        path_to_xml_local = os.path.join(path_to_plugin_local,
                                         PLUGIN_VERSIONS_FILENAME)

        xml_content_local = readTextFile(path_to_xml_local)
        appinfo_local = XmlVersionParser().parse(xml_content_local)

        url = appinfo_local.updatesUrl
        try:
            appinfo_remote = downloadAppInfo(url)
        except Exception:
            appinfo_remote = None

        if (appinfo_remote is not None and
                appinfo_local.currentVersion < appinfo_remote.currentVersion):
            print_error(u'Error. New version < Prev version')
            sys.exit(1)
        elif (appinfo_remote is not None and
                appinfo_local.currentVersion == appinfo_remote.currentVersion):
            print_warning(u'Warning: Uploaded the same version')
        print_info(u'Uploading...')

        path_to_upload = os.path.dirname(appinfo_local.updatesUrl.replace(DEPLOY_SITE + u'/', DEPLOY_HOME_PATH))
        version_local = str(appinfo_local.currentVersion)
        archive_name = u'{}-{}.zip'.format(pluginname, version_local)
        path_to_archive_local = os.path.join(path_to_plugin_local, archive_name)

        with cd(path_to_upload):
            put(path_to_archive_local, archive_name)
            put(path_to_xml_local, PLUGIN_VERSIONS_FILENAME)
    site_versions()


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_binary(is_stable=False):
    '''
    Upload binary version to site
    '''
    facts = BuildFacts()

    if is_stable:
        win_tpl_files = FILES_FOR_UPLOAD_STABLE_WIN
        linux_tpl_files = FILES_FOR_UPLOAD_STABLE_LINUX
        deploy_path = DEPLOY_STABLE_PATH
    else:
        win_tpl_files = FILES_FOR_UPLOAD_UNSTABLE_WIN
        linux_tpl_files = FILES_FOR_UPLOAD_UNSTABLE_LINUX
        deploy_path = DEPLOY_UNSTABLE_PATH

    versions_file = facts.versions_file
    windows_result_path = os.path.join(PATH_TO_WINDOWS_DISTRIBS,
                                       facts.version,
                                       WINDOWS_BUILD_DIR)

    binary_uploader = BinaryUploader(win_tpl_files,
                                     linux_tpl_files,
                                     windows_result_path,
                                     versions_file,
                                     deploy_path)
    binary_uploader.deploy()


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_plugins_pack():
    '''
    Upload archive with all plugins to site
    '''
    pluginsBuilder = BuilderPlugins()
    pack_path = pluginsBuilder.get_plugins_pack_path()
    with cd(DEPLOY_PLUGINS_PACK_PATH):
        basename = os.path.basename(pack_path)
        put(pack_path, basename)


def _add_git_tag(tagname):
    local(u'git checkout master')
    local(u'git tag {}'.format(tagname))
    local(u'git push --tags')


@task
def build(is_stable=False):
    '''
    Create artifacts for current version.
    '''
    if is_stable:
        build(False)

    sources(is_stable)
    plugins(True)

    if sys.platform.startswith('linux'):
        vm_linux_binary(is_stable)
        # deb_sources_included(is_stable)
    elif sys.platform.startswith('win32'):
        win(is_stable)


@hosts(DEPLOY_SERVER_NAME)
@task
@linux_only
def deploy(is_stable=False):
    '''
    Upload to site
    '''
    if is_stable:
        deploy(False)
    else:
        # To upload only once
        upload_plugin()
        upload_plugins_pack()

    # ppa_path = PPA_STABLE_PATH if is_stable else PPA_UNSTABLE_PATH
    #
    # deb_path = BuilderDebSourcesIncluded(DEB_SOURCE_BUILD_DIR,
    #                                      UBUNTU_RELEASE_NAMES,
    #                                      tobool(is_stable)).getResultPath()
    # _ppa_upload(ppa_path, deb_path)

    upload_binary(is_stable)

    version_str = getOutwikerVersionStr()
    if is_stable:
        tagname = u'release_{}'.format(version_str)
    else:
        tagname = u'unstable_{}'.format(version_str)

    _add_git_tag(tagname)


@task
def doc():
    '''
    Build documentation
    '''
    doc_path = u'doc/_build'
    if os.path.exists(doc_path):
        shutil.rmtree(doc_path)

    with lcd('doc'):
        local('make html')


@task
@linux_only
def prepare_virtual():
    '''
    Prepare virtual machine
    '''
    with lcd(os.path.join(NEED_FOR_BUILD_DIR, u'virtual')):
        local(u'ansible-playbook virtual_prepare.yml -k --ask-sudo-pass')


@task
@linux_only
def vm_run():
    '''
    Run virtual machines for build
    '''
    for host_param in VM_BUILD_PARAMS.values():
        with lcd(host_param[u'vagrant_path']):
            local(u'vagrant up')


@task
@linux_only
def vm_update():
    '''
    Update the virtual machines
    '''
    for host_param in VM_BUILD_PARAMS.values():
        with lcd(host_param[u'vagrant_path']):
            local(u'vagrant box update')


@task(alias='vm_halt')
@linux_only
def vm_stop():
    '''
    Stop virtual machines for build
    '''
    for host_param in VM_BUILD_PARAMS.values():
        with lcd(host_param[u'vagrant_path']):
            local(u'vagrant halt')


@task
@linux_only
def vm_remove_keys():
    '''
    Remove local SSH keys for remote virtual machines
    '''
    for host_param in VM_BUILD_PARAMS.values():
        host = host_param[u'host']
        local(u'ssh-keygen -f ~/.ssh/known_hosts -R {}'.format(host))


@task
@linux_only
def vm_prepare():
    '''
    Prepare virtual machines for build
    '''
    vm_run()
    with lcd(u'need_for_build/virtual/build_machines'):
        local(u'ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook prepare_build_machines.yml')


@task
@linux_only
def vm_linux_binary(is_stable=0):
    '''
    Create 64-bit assembly on virtual machines
    '''
    vm_run()
    version_str = getOutwikerVersionStr()
    version = getOutwikerVersion()

    path_to_result = os.path.abspath(
        os.path.join(BUILD_DIR, version_str, LINUX_BUILD_DIR)
    )

    if not os.path.exists(path_to_result):
        os.makedirs(path_to_result)

    with lcd(u'need_for_build/virtual/build_machines'):
        local(u'ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook build_linux_binaries.yml --extra-vars "version={version} build={build} save_to={save_to} is_stable={is_stable}"'.format(
            version=version[0],
            build=version[1],
            save_to=path_to_result,
            is_stable=is_stable)
        )


@task(alias='linux_appimage')
@linux_only
def appimage(is_stable=0):
    '''
    Build AppImage package
    '''
    builder = BuilderAppImage(is_stable=tobool(is_stable))
    builder.build()
    print_info('AppImage created: {}'.format(builder.get_appimage_files()))


@task
def coverage():
    '''
    Create test coverage statistics
    '''
    with lcd('src'):
        local('coverage report {} -i'.format(COVERAGE_PARAMS))
        local('coverage html {} -i'.format(COVERAGE_PARAMS))


@task
@linux_only
def docker_build_create():
    '''
    Create a Docker image to build process
    '''
    with lcd('need_for_build/build_docker'):
        local('docker build -t outwiker/build_linux .')


@task
@linux_only
def docker_build(*args):
    '''
    Run the build process inside the Docker container
    '''
    docker_build_create()

    tasks_str = ' '.join(args)
    current_dir = os.path.abspath('.')
    command = 'docker run -v "{path}:/home/user/project" --user $(id -u):$(id -g) -i -t outwiker/build_linux {tasks}'.format(
        path=current_dir,
        tasks=tasks_str
    )
    local(command)


@task
@linux_only
def docker_build_wx(ubuntu_version: str, wx_version: str):
    '''
    Build a wxPython library from sources
    '''
    # Create dest dir
    build_dir = os.path.abspath(os.path.join(BUILD_DIR, BUILD_LIB_DIR))
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    # Create Docker image
    docker_image = 'wxpython/ubuntu_{ubuntu_version}_webkit1'.format(ubuntu_version=ubuntu_version)

    dockerfile_path = os.path.join(
        NEED_FOR_BUILD_DIR,
        'build_wxpython',
        'ubuntu_{ubuntu_version}'.format(ubuntu_version=ubuntu_version)
    )

    with lcd(dockerfile_path):
        local('docker build -t {docker_image} .'.format(docker_image=docker_image))

    # Build wxPython
    command = 'docker run -v "{path}:/home/user/build" --rm --user $(id -u):$(id -g) -i -t -e "WX_VERSION={wx_version}" {docker_image}'.format(
        path=build_dir,
        docker_image=docker_image,
        wx_version=wx_version
    )
    local(command)


@task(alias='linux_snap')
@linux_only
def snap(is_stable=0):
    '''
    Build clean snap package
    '''
    is_stable = tobool(is_stable)
    builder = BuilderSnap(is_stable)
    builder.build()


@task(alias='linux_snap_publish')
@linux_only
def snap_publish():
    '''
    Publish created snap package
    '''
    builder = BuilderSnap(False)
    snap_files = builder.get_snap_files()

    for snap_file in snap_files:
        print_info('Publish snap: {fname}'.format(fname=snap_file))
        local('snapcraft push "{fname}"'.format(fname=snap_file))
        local('snapcraft sign-build "{fname}"'.format(fname=snap_file))


@task
def site_content(is_stable=False):
    path_to_templates = os.path.join(NEED_FOR_BUILD_DIR,
                                     SITE_CONTENT_DIR)
    # List of SiteContentSource
    apps = []
    apps.append(SiteContentSource(
        os.path.join('src', 'versions.xml'),
        'ru',
        'outwiker_unstable.ru.txt'))

    apps.append(SiteContentSource(
        os.path.join('src', 'versions.xml'),
        'en',
        'outwiker_unstable.en.txt'))

    apps.append(SiteContentSource(
        os.path.join('src', 'versions_stable.xml'),
        'ru',
        'outwiker_stable.ru.txt'))

    apps.append(SiteContentSource(
        os.path.join('src', 'versions_stable.xml'),
        'en',
        'outwiker_stable.en.txt'))

    for plugin in PLUGINS_LIST:
        item_ru = SiteContentSource(
            os.path.join('plugins', plugin, plugin, 'plugin.xml'),
            'ru',
            '{}.ru.txt'.format(plugin))

        item_en = SiteContentSource(
            os.path.join('plugins', plugin, plugin, 'plugin.xml'),
            'en',
            '{}.en.txt'.format(plugin))

        apps.append(item_ru)
        apps.append(item_en)

    builder = SiteContentBuilder(SITE_CONTENT_BUILD_DIR,
                                 apps,
                                 path_to_templates)
    builder.build()


@task
def snap_restart():
    '''
    Restart snap daemons
    '''
    local('sudo systemctl stop snap.lxd.daemon.unix.socket')
    local('sudo systemctl restart snap.lxd.daemon')
