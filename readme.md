![build](https://github.com/shinolab/pyautd/workflows/build/badge.svg)
![Publish to PyPI](https://github.com/shinolab/pyautd/workflows/Publish%20to%20PyPI/badge.svg)

# pyautd3

[autd3 library](https://github.com/shinolab/autd3-library-software) for python3.6+

version: 0.8.0

## Install

```
pip install pyautd3
```
or from this repository
```
pip install git+https://github.com/shinolab/pyautd.git
```

## Requirements

If you are using Windows, install [Npcap](https://nmap.org/npcap/) with WinPcap API-compatible mode (recomennded) or [WinPcap](https://www.winpcap.org/).

If you are using Linux/MacOS, you may need to install and run pyautd3 as root. 
```
sudo pip install pyautd3
sudo python
>>> import pyautd3
``` 

## Exmaple

```python
import sys

from pyautd3 import AUTD, Link, Gain, Modulation, Sequence  # NOQA


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

    autd.clear()
    autd.calibrate()

    firm_info_list = autd.firmware_info_list()
    for i, firm in enumerate(firm_info_list):
        print('[' + str(i) + ']: CPU: ' + firm[0] + ', FPGA: ' + firm[1])

    f = Gain.focal_point([90., 80., 150.])
    m = Modulation.sine_wave(150)

    autd.append_gain_sync(f)
    autd.append_modulation_sync(m)

    print('press enter to start stm...')
    sys.stdin.readline()

    m = Modulation.static(255)
    autd.append_modulation_sync(m)

    f1 = Gain.focal_point([87.5, 80., 150.])
    f2 = Gain.focal_point([92.5, 80., 150.])
    autd.append_stm_gain(f1)
    autd.append_stm_gain(f2)

    autd.start_stm(50)

    print('press enter to exit...')
    sys.stdin.readline()

    autd.dispose()
```

# Author

Shun Suzuki, 2020
