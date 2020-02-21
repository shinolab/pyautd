'''
File: __init__.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 21/02/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

from pyautd.autd import LinkType
from pyautd.nativemethods import init_autd3
from pyautd.autd import AUTD
import os.path

__all__ = ['LinkType', 'AUTD']

lib_path = os.path.join(os.path.dirname(__file__), 'autd3capi.dll')
init_autd3(lib_path)
