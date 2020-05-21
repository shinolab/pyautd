'''
File: autd.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 21/05/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import ctypes
from ctypes import c_void_p, byref
from enum import IntEnum
import warnings

from .nativemethods import Nativemethods

NATIVE_METHODDS = Nativemethods()


class LinkType(IntEnum):
    ETHERCAT = 0
    TwinCAT = 1
    SOEM = 2


class Gain:
    def __init__(self):
        self.gain_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.dll.AUTDDeleteGain(self.gain_ptr)


class Modulation:
    def __init__(self):
        self.modulation_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.dll.AUTDDeleteModulation(self.modulation_ptr)


class Link:
    def __init__(self):
        self.link_ptr = c_void_p()

    @staticmethod
    def soem_link(ifname, dev_num):
        link = Link()
        NATIVE_METHODDS.dll.AUTDSOEMLink(byref(link.link_ptr), ifname.encode('utf-8'), dev_num)
        return link

    @staticmethod
    def ethercat_link(ipaddr, ams_net_id):
        link = Link()
        NATIVE_METHODDS.dll.AUTDEtherCATLink(byref(link.link_ptr), ipaddr.encode('utf-8'), ams_net_id.encode('utf-8'))
        return link

    @staticmethod
    def local_ethercat_link(ipaddr, ams_net_id):
        link = Link()
        NATIVE_METHODDS.dll.AUTDLocalEtherCATLink(byref(link.link_ptr))
        return link


class AUTD:
    def __init__(self):
        self.autd = c_void_p()
        NATIVE_METHODDS.dll.AUTDCreateController(byref(self.autd))

        self.__disposed = False

    def __del__(self):
        self.dispose()

    def open(self, linktype=LinkType.SOEM, location=""):
        warn_msg = "`open` is deprecated, use open_with instead."
        warnings.warn(warn_msg, UserWarning)
        NATIVE_METHODDS.dll.AUTDOpenController(self.autd, int(linktype), location.encode('utf-8'))

    def open_with(self, link: Link):
        NATIVE_METHODDS.dll.AUTDOpenControllerWith(self.autd, link.link_ptr)

    @staticmethod
    def enumerate_adapters():
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.dll.AUTDGetAdapterPointer(byref(handle))

        for i in range(size):
            sb_desc = ctypes.create_string_buffer(128)
            sb_name = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.dll.AUTDGetAdapter(handle, i, sb_desc, sb_name)
            res.append([sb_name.value.decode('utf-8'), sb_desc.value.decode('utf-8')])

        NATIVE_METHODDS.dll.AUTDFreeAdapterPointer(handle)

        return res

    def firmware_info_list(self):
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.dll.AUTDGetFirmwareInfoListPointer(self.autd, byref(handle))

        for i in range(size):
            sb_cpu = ctypes.create_string_buffer(128)
            sb_fpga = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.dll.AUTDGetFirmwareInfo(handle, i, sb_cpu, sb_fpga)
            res.append([sb_cpu.value.decode('utf-8'), sb_fpga.value.decode('utf-8')])

        NATIVE_METHODDS.dll.AUTDFreeFirmwareInfoListPointer(handle)

        return res

    def close(self):
        NATIVE_METHODDS.dll.AUTDCloseController(self.autd)

    def free(self):
        NATIVE_METHODDS.dll.AUTDFreeController(self.autd)

    def dispose(self):
        if not self.__disposed:
            self.close()
            self.free()
            self.__disposed = True

    def set_silent(self, silent: bool):
        NATIVE_METHODDS.dll.AUTDSetSilentMode(self.autd, silent)

    def calibrate_modulation(self):
        return NATIVE_METHODDS.dll.AUTDCalibrateModulation(self.autd)

    def add_device(self, pos, rot, group_id=0):
        NATIVE_METHODDS.dll.AUTDAddDevice(self.autd, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2], group_id)

    @staticmethod
    def focal_point_gain(x, y, z, amp=255):
        gain = Gain()
        NATIVE_METHODDS.dll.AUTDFocalPointGain(byref(gain.gain_ptr), x, y, z, amp)
        return gain

    @staticmethod
    def modulation(amp=255):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDModulation(byref(mod.modulation_ptr), amp)
        return mod

    @staticmethod
    def sine_modulation(freq, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDSineModulation(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    def append_modulation(self, mod: Modulation):
        NATIVE_METHODDS.dll.AUTDAppendModulation(self.autd, mod.modulation_ptr)

    def append_modulation_sync(self, mod: Modulation):
        NATIVE_METHODDS.dll.AUTDAppendModulationSync(self.autd, mod.modulation_ptr)

    def append_gain(self, gain: Gain):
        NATIVE_METHODDS.dll.AUTDAppendGain(self.autd, gain.gain_ptr)

    def append_gain_sync(self, gain: Gain, wait_for_send: bool = False):
        NATIVE_METHODDS.dll.AUTDAppendGainSync(self.autd, gain.gain_ptr, wait_for_send)

    def append_stm_gain(self, gain: Gain):
        NATIVE_METHODDS.dll.AUTDAppendSTMGain(self.autd, gain.gain_ptr)

    def start_stm(self, freq):
        NATIVE_METHODDS.dll.AUTDStartSTModulation(self.autd, freq)

    def stop_stm(self):
        NATIVE_METHODDS.dll.AUTDStopSTModulation(self.autd)

    def finish_stm(self):
        NATIVE_METHODDS.dll.AUTDFinishSTModulation(self.autd)
