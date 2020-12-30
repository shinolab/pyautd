'''
File: stm.py
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

def stm(autd:AUTD):
    autd.set_silent_mode(False)

    x = 90.0
    y = 80.0
    z = 150.0

    m = Modulation.static()
    autd.append_modulation_sync(m)
    
    radius = 30.0
    size = 200
    for i in range(size):
        theta = 2 * math.pi * i / size
        r = [x + radius * math.cos(theta), y + radius * math.sin(theta), z]
        f = Gain.focal_point(r)
        autd.append_stm_gain(f)
        
    autd.start_stm(1)
    