import setuptools
import shutil
import requests
import platform
import zipfile
import os
import tarfile

_pf = platform.system()
_os = ''
_lib_ext = ''
if _pf == 'Windows':
    _os = 'win-x64'
    _lib_ext = ".dll"
elif _pf == 'Darwin':
    _os = 'macos-x64'
    _lib_ext = ".dylib"
elif _pf == 'Linux':
    _os = 'linux-x64'
    _lib_ext = ".so"
else:
    raise ImportError('Not supported OS')

_AssetsBaseURL = 'https://github.com/shinolab/autd3-library-software/releases/download/'
_Version = 'v0.3.0'

module_path = './pyautd3/'
ext = '.zip' if _os.startswith('win') else '.tar.gz'
url = _AssetsBaseURL + _Version + '/autd3-' + _Version + '-' + _os + ext
print(url)

tmp_archive_path = module_path + 'tmp' + ext

res = requests.get(url, stream=True)
with open(tmp_archive_path, 'wb') as fp:
    shutil.copyfileobj(res.raw, fp)

if ext == '.zip':
    with zipfile.ZipFile(tmp_archive_path) as zfile:
        for info in zfile.infolist():
            if info.filename.startswith('bin') and info.filename.endswith(_lib_ext):
                zfile.extract(info, module_path)
elif ext == '.tar.gz':
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
    version='0.3.0',
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
        'pyautd3': ['bin/*' + _lib_ext],
    },
    python_requires='>=3.6',
)
