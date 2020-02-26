'''
File: __init__.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 26/02/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

from pyautd3.autd import LinkType
from pyautd3.nativemethods import init_autd3
from pyautd3.autd import AUTD
import os.path
import platform

pf = platform.system()
prefix = ''
ext = ''
if pf == 'Windows':
    ext = '.dll'
elif pf == 'Darwin':
    prefix = 'lib'
    ext = '.dylib'
elif pf == 'Linux':
    prefix = 'lib'
    ext = '.so'

__all__ = ['LinkType', 'AUTD']

lib_path = os.path.join(os.path.dirname(__file__),
                        'bin', prefix + 'autd3capi' + ext)
init_autd3(lib_path)
