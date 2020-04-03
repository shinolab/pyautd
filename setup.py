import shutil
import zipfile
import tarfile
import os

import setuptools
import requests


def _get_version():
    with open('readme.md', 'r') as f:
        for line in f.readlines():
            if line.startswith('version: '):
                return line.replace('version: ', '')
    raise LookupError('version info is not found in readme.md')


def _set_package_version(version):
    init_py = ''
    with open('pyautd3/__init__.py', 'r') as f:
        for line in f.readlines():
            if line.startswith('__version__'):
                line = '__version__ = \'' + version.strip() + '\'\n'
            init_py = init_py + line

    with open('pyautd3/__init__.py', 'w') as f:
        f.write(init_py)


support_os = ['win-x64', 'macos-x64', 'linux-x64']

for target_os in support_os:
    _lib_ext = ''
    _archive_ext = ''
    if target_os.startswith('win'):
        _lib_ext = ".dll"
        _archive_ext = '.zip'
    elif target_os.startswith('mac'):
        _lib_ext = ".dylib"
        _archive_ext = '.tar.gz'
    elif target_os.startswith('linux'):
        _lib_ext = ".so"
        _archive_ext = '.tar.gz'
    else:
        raise ImportError('Not supported OS')

    _AssetsBaseURL = 'https://github.com/shinolab/autd3-library-software/releases/download/'
    _Version = 'v' + '.'.join(_get_version().split('.')[0:3])
    _Version = _Version.strip()
    _set_package_version(_get_version())

    module_path = './pyautd3/'
    url = _AssetsBaseURL + _Version + '/autd3-' + \
        _Version + '-' + target_os + _archive_ext

    tmp_archive_path = module_path + 'tmp' + _archive_ext

    res = requests.get(url, stream=True)
    with open(tmp_archive_path, 'wb') as fp:
        shutil.copyfileobj(res.raw, fp)

    if _archive_ext == '.zip':
        with zipfile.ZipFile(tmp_archive_path) as zfile:
            for info in zfile.infolist():
                if info.filename.startswith('bin') and info.filename.endswith(_lib_ext):
                    zfile.extract(info, module_path)
    elif _archive_ext == '.tar.gz':
        with tarfile.open(tmp_archive_path) as tarfile:
            libraries = []
            for i in tarfile.getmembers():
                if i.name.startswith('bin') and i.name.endswith(_lib_ext):
                    libraries.append(i)
            tarfile.extractall(path=module_path, members=libraries)

    os.remove(tmp_archive_path)

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyautd3',
    version=_get_version(),
    author='Shun Suzuki',
    author_email='suzuki@hapis.k.u-tokyo.ac.jp',
    description='AUTD3 library wrapper for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    url='https://github.com/shinolab/pyautd',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_dir={'pyautd3': 'pyautd3'},
    packages=['pyautd3'],
    package_data={
        'pyautd3': ['bin/*'],
    },
    python_requires='>=3.6',
)
