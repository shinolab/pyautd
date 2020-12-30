'''
File: bessel.py
Project: samples
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 30/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import math

from pyautd3 import AUTD, Gain, Modulation

def bessel(autd:AUTD):
    autd.set_silent_mode(True)

    f = Gain.bessel_beam([90., 80., 150.], [0., 0., 1.], 13. / 180 * math.pi)
    m = Modulation.sine_wave(150)

    autd.append_gain_sync(f)
    autd.append_modulation_sync(m)
    