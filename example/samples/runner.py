'''
File: runner.py
Project: samples
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 30/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

from pyautd3 import AUTD

from . import simple, bessel, holo, stm, seq

def run(autd:AUTD):
    samples = [
        (simple.simple, "Single Focal Point Sample"),
        (bessel.bessel, "Bessel beam Sample"),
        (holo.holo, "Multiple Focal Points Sample"),
        (stm.stm, "Spatio-Temporal Modulation Sample"),
        (seq.seq, "PointSequence (Hardware STM) Sample")
    ]

    autd.clear()
    autd.calibrate()

    autd.set_wavelength(8.5)

    firm_info_list = autd.firmware_info_list()
    for i, firm in enumerate(firm_info_list):
        print(f'[{i}]: CPU: {firm[0]}, FPGA: {firm[1]}')

    while True:
        for i, (_, name) in enumerate(samples):
            print(f'[{i}]: {name}')
        print('[Other]: finish')
        print('Choose number: ')
        
        idx = input()
        idx = int(idx) if idx.isdigit() else None
        if idx is None or idx >= len(samples):
            break

        (fn, _) = samples[idx]
        fn(autd)

        print('press enter to finish...')

        _ = input()

        print('finish.')
        autd.stop()

    autd.clear()
    autd.dispose()
