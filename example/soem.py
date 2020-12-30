'''
File: soem.py
Project: example
Created Date: 30/12/2020
Author: Shun Suzuki
-----
Last Modified: 30/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import sys

from pyautd3 import AUTD, Link, Gain, Modulation, Sequence  # NOQA

from samples import runner 

def get_adapter_name():
    adapters = Link.enumerate_adapters()
    for i, adapter in enumerate(adapters):
        print('[' + str(i) + ']: ' + adapter[0] + ', ' + adapter[1])

    index = int(input('choose number: '))
    return adapters[index][0]


if __name__ == '__main__':
    autd = AUTD()

    autd.add_device([0., 0., 0.], [0., 0., 0.])
    # autd.add_device([0., 0., 0.], [0., 0., 0.])

    ifname = get_adapter_name()
    link = Link.soem_link(ifname, autd.num_devices())
    autd.open_with(link)

    runner.run(autd)
