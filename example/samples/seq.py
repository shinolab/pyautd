'''
File: seq.py
Project: samples
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 30/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

from pyautd3 import AUTD, Modulation, Sequence

def seq(autd:AUTD):
    autd.set_silent_mode(False)

    x = 90.0
    y = 80.0
    z = 150.0

    m = Modulation.static()
    autd.append_modulation_sync(m)
    
    radius = 30.0
    size = 200
    center = [x, y, z]
    normal = [0., 0., 1.]
    seq = Sequence.circum(center, normal, radius, size)
    _ = seq.SetFrequency(200)
    
    autd.append_sequence(seq)
