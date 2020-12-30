'''
File: simple.py
Project: samples
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 30/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

from pyautd3 import AUTD, Gain, Modulation


def simple(autd: AUTD):
    autd.set_silent(True)

    f = Gain.focal_point([90., 80., 150.])
    m = Modulation.sine_wave(150)

    autd.append_gain_sync(f)
    autd.append_modulation_sync(m)
