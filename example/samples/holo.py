'''
File: holo.py
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

def holo(autd:AUTD):
    autd.set_silent_mode(True)

    foci = [
        [120., 80., 150.],
        [60., 80., 150.],
    ]
    amps = [1.0, 1.0]

    f = Gain.holo(foci, amps)
    m = Modulation.sine_wave(150)

    autd.append_gain_sync(f)
    autd.append_modulation_sync(m)
    