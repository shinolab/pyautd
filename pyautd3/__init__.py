'''
File: __init__.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 21/05/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import os.path
import platform

from pyautd3.autd import LinkType, Link, AUTD
from pyautd3.nativemethods import Nativemethods

PLATFORM = platform.system()
PREFIX = ''
EXT = ''
if PLATFORM == 'Windows':
    EXT = '.dll'
elif PLATFORM == 'Darwin':
    PREFIX = 'lib'
    EXT = '.dylib'
elif PLATFORM == 'Linux':
    PREFIX = 'lib'
    EXT = '.so'

__all__ = ['LinkType', 'AUTD', 'Link']
__version__ = '0.4.1'

LIB_PATH = os.path.join(os.path.dirname(__file__), 'bin', PREFIX + 'autd3capi' + EXT)
Nativemethods().init_dll(LIB_PATH)
