'''
File: autd.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 29/12/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import ctypes
from ctypes import c_void_p, byref, Structure, c_float, c_int, c_bool
from enum import IntEnum
import math
import numpy as np

from .nativemethods import Nativemethods

NATIVE_METHODDS = Nativemethods()


class ModSamplingFreq(IntEnum):
    SMPL_125_HZ = 125
    SMPL_250_HZ = 250
    SMPL_500_HZ = 500
    SMPL_1_KHZ = 1000
    SMPL_2_KHZ = 2000
    SMPL_4_KHZ = 4000
    SMPL_8_KHZ = 8000


class ModBufSize(IntEnum):
    BUF_125 = 125
    BUF_250 = 250
    BUF_500 = 500
    BUF_1000 = 1000
    BUF_2000 = 2000
    BUF_4000 = 4000
    BUF_8000 = 8000
    BUF_16000 = 16000
    BUF_32000 = 32000


class Configuration:
    def __init__(self):
        self.mod_sample_freq = ModSamplingFreq.SMPL_4_KHZ
        self.mod_buf_size = ModBufSize.BUF_4000


class OptMethod(IntEnum):
    SDP = 0
    EVD = 1
    GS = 2
    GS_PAT = 3
    NAIVE = 4
    LM = 5


class SDPParams(Structure):
    _fields_ = [("regularization", c_float), ("repeat", c_int), ("plambda", c_float), ("normalize_amp", c_bool)]

    def __init__(self):
        super().__init__()
        self.regularization = -1
        self.repeat = -1
        self.plambda = -1
        self.normalize_amp = True


class EVDParams(Structure):
    _fields_ = [("regularization", c_float), ("normalize_amp", c_bool)]

    def __init__(self):
        super().__init__()
        self.regularization = -1
        self.normalize_amp = True


class NLSParams(Structure):
    _fields_ = [("eps1", c_float), ("eps2", c_float), ("k_max", c_float), ("tau", c_float)]

    def __init__(self):
        super().__init__()
        self.eps1 = -1
        self.eps2 = -1
        self.k_max = -1
        self.tau = -1


class Gain:
    def __init__(self):
        self.gain_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.dll.AUTDDeleteGain(self.gain_ptr)

    @staticmethod
    def adjust_amp(amp):
        d = math.asin(amp) / math.pi
        return int(511.0 * d)

    @staticmethod
    def grouped(group_ids, gains):
        size = len(group_ids)
        group_ids = np.array(group_ids).astype(np.int32)
        group_ids = np.ctypeslib.as_ctypes(group_ids)

        gains_array = np.zeros([size]).astype(np.object)
        for i, gain in enumerate(gains):
            gains_array[i] = gain.gain_ptr
        gains_array = np.ctypeslib.as_ctypes(gains_array)

        NATIVE_METHODDS.dll.AUTDGroupedGain(byref(gain.gain_ptr), group_ids, gains_array, size)

    @staticmethod
    def focal_point(pos, amp: float = 1.0):
        duty = Gain.adjust_amp(amp)
        return Gain.focal_point_with_duty(pos, duty)

    @staticmethod
    def focal_point_with_duty(pos, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.dll.AUTDFocalPointGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], duty)
        return gain

    @staticmethod
    def bessel_beam(pos, dir, theta_z, amp: float = 1.0):
        duty = Gain.adjust_amp(amp)
        return Gain.bessel_beam_with_duty(pos, dir, theta_z, duty)

    @staticmethod
    def bessel_beam_with_duty(pos, dir, theta_z, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.dll.AUTDBesselBeamGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], theta_z, duty)
        return gain

    @staticmethod
    def plane_wave(pos, dir, amp: float = 1.0):
        duty = Gain.adjust_amp(amp)
        return Gain.plane_wave_with_duty(pos, dir, duty)

    @staticmethod
    def plane_wave_with_duty(pos, dir, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.dll.AUTDPlaneWaveGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], duty)
        return gain

    @staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint16)
        data = np.ctypeslib.as_ctypes(data)

        gain = Gain()
        NATIVE_METHODDS.dll.AUTDCustomGain(byref(gain.gain_ptr), data, size)
        return gain

    @staticmethod
    def holo(foci, amps, method: OptMethod = OptMethod.SDP, params=None):
        size = len(foci)
        amps = np.array(amps).astype(np.float32)
        amps = np.ctypeslib.as_ctypes(amps)
        foci_array = np.zeros([size * 3]).astype(np.float32)
        for i, focus in enumerate(foci):
            foci_array[3 * i] = focus[0]
            foci_array[3 * i + 1] = focus[1]
            foci_array[3 * i + 2] = focus[2]
        foci_array = np.ctypeslib.as_ctypes(foci_array)

        params = None if params is None else byref(params)

        gain = Gain()
        NATIVE_METHODDS.dll.AUTDHoloGain(byref(gain.gain_ptr), foci_array, amps, size, int(method), params)
        return gain

    @staticmethod
    def transducer_test(idx: int, duty: int, phase: int):
        gain = Gain()
        NATIVE_METHODDS.dll.AUTDTransducerTestGain(byref(gain.gain_ptr), idx, duty, phase)
        return gain


class Modulation:
    def __init__(self):
        self.modulation_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.dll.AUTDDeleteModulation(self.modulation_ptr)

    @staticmethod
    def static(amp=255):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDModulation(byref(mod.modulation_ptr), amp)
        return mod

    @staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint16)
        data = np.ctypeslib.as_ctypes(data)

        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDSineModulation(byref(mod.modulation_ptr), data, size)
        return mod

    @staticmethod
    def from_raw_pcm(filename, sampling_freq: float):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDRawPCMModulation(byref(mod.modulation_ptr), filename.encode('utf-8'), sampling_freq)
        return mod

    @staticmethod
    def from_wav(filename):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDWavModulation(byref(mod.modulation_ptr), filename.encode('utf-8'))
        return mod

    @staticmethod
    def sine_wave(freq: int, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDSineModulation(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    @staticmethod
    def saw_wave(freq: int):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDSawModulation(byref(mod.modulation_ptr), freq)
        return mod

    @staticmethod
    def square_wave(freq: int, low: int = 0, high: int = 255):
        mod = Modulation()
        NATIVE_METHODDS.dll.AUTDSquareModulation(byref(mod.modulation_ptr), freq, low, high)
        return mod


class Sequence:
    def __init__(self):
        self.seq_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.dll.AUTDDeleteSequence(self.seq_ptr)

    @staticmethod
    def sequence():
        seq = Sequence()
        NATIVE_METHODDS.dll.AUTDSequence(byref(seq.seq_ptr))
        return seq

    @staticmethod
    def circum(center, normal, radius, num_points):
        seq = Sequence()
        NATIVE_METHODDS.dll.AUTDCircumSequence(
            byref(
                seq.seq_ptr),
            center[0],
            center[1],
            center[2],
            normal[0],
            normal[1],
            normal[2],
            radius,
            num_points)
        return seq

    def add_point(self, point):
        NATIVE_METHODDS.dll.AUTDSequenceAppnedPoint(self.seq_ptr, point[0], point[1], point[2])

    def add_points(self, points):
        size = len(points)
        points_array = np.zeros([size * 3]).astype(np.float32)
        for i, p in enumerate(points):
            points_array[3 * i] = p[0]
            points_array[3 * i + 1] = p[1]
            points_array[3 * i + 2] = p[2]
        points_array = np.ctypeslib.as_ctypes(points_array)

        NATIVE_METHODDS.dll.AUTDSequenceAppnedPoint(self.seq_ptr, points_array, size)

    def set_frequency(self, freq: float):
        return NATIVE_METHODDS.dll.AUTDSequenceSetFreq(self.seq_ptr, freq)

    def frequency(self):
        return NATIVE_METHODDS.dll.AUTDSequenceFreq(self.seq_ptr)

    def sampling_frequency(self):
        return NATIVE_METHODDS.dll.AUTDSequenceSamplingFreq(self.seq_ptr)

    def sampling_frequency_div(self):
        return NATIVE_METHODDS.dll.AUTDSequenceSamplingFreqDiv(self.seq_ptr)


class Link:
    def __init__(self):
        self.link_ptr = c_void_p()

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
        self.p_cnt = c_void_p()
        NATIVE_METHODDS.dll.AUTDCreateController(byref(self.p_cnt))
        self.__disposed = False

    def __del__(self):
        self.dispose()

    def open_with(self, link: Link):
        NATIVE_METHODDS.dll.AUTDOpenControllerWith(self.p_cnt, link.link_ptr)

    def firmware_info_list(self):
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.dll.AUTDGetFirmwareInfoListPointer(self.p_cnt, byref(handle))

        for i in range(size):
            sb_cpu = ctypes.create_string_buffer(128)
            sb_fpga = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.dll.AUTDGetFirmwareInfo(handle, i, sb_cpu, sb_fpga)
            res.append([sb_cpu.value.decode('utf-8'), sb_fpga.value.decode('utf-8')])

        NATIVE_METHODDS.dll.AUTDFreeFirmwareInfoListPointer(handle)

        return res

    def dispose(self):
        if not self.__disposed:
            self.close()
            self._free()
            self.__disposed = True

    def add_device(self, pos, rot, group_id=0):
        return NATIVE_METHODDS.dll.AUTDAddDevice(self.p_cnt, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2], group_id)

    def add_device_quaternion(self, pos, q, group_id=0):
        return NATIVE_METHODDS.dll.AUTDAddDeviceQuaternion(self.p_cnt, pos[0], pos[1], pos[2], q[0], q[1], q[2], q[3], group_id)

    def calibrate(self, config: Configuration = Configuration()):
        return NATIVE_METHODDS.dll.AUTDCalibrate(self.p_cnt, int(config.mod_sample_freq), int(config.mod_buf_size))

    def set_delay(self, delays):
        size = len(delays)
        data = np.array(delays).astype(np.uint16)
        data = np.ctypeslib.as_ctypes(data)

        NATIVE_METHODDS.dll.AUTDSetDelay(self.p_cnt, data, size)

    def stop(self):
        NATIVE_METHODDS.dll.AUTDStop(self.p_cnt)

    def close(self):
        NATIVE_METHODDS.dll.AUTDCloseController(self.p_cnt)

    def clear(self):
        NATIVE_METHODDS.dll.AUTDClear(self.p_cnt)

    def _free(self):
        NATIVE_METHODDS.dll.AUTDFreeController(self.p_cnt)

    def set_silent(self, silent: bool):
        NATIVE_METHODDS.dll.AUTDSetSilentMode(self.p_cnt, silent)

    def set_wavelength(self, wavelength: float):
        NATIVE_METHODDS.dll.AUTDSetWavelength(self.p_cnt, wavelength)

    def is_open(self):
        return NATIVE_METHODDS.dll.AUTDIsOpen(self.p_cnt)

    def is_silent(self):
        return NATIVE_METHODDS.dll.AUTDIsSilentMode(self.p_cnt)

    def wavelength(self):
        return NATIVE_METHODDS.dll.AUTDWavelength(self.p_cnt)

    def num_devices(self):
        return NATIVE_METHODDS.dll.AUTDNumDevices(self.p_cnt)

    def num_transducers(self):
        return NATIVE_METHODDS.dll.AUTDNumTransducers(self.p_cnt)

    def remaining_in_buffer(self):
        return NATIVE_METHODDS.dll.AUTDRemainingInBuffer(self.p_cnt)

    def append_gain(self, gain: Gain):
        NATIVE_METHODDS.dll.AUTDAppendGain(self.p_cnt, gain.gain_ptr)

    def append_gain_sync(self, gain: Gain, wait_for_send: bool = False):
        NATIVE_METHODDS.dll.AUTDAppendGainSync(self.p_cnt, gain.gain_ptr, wait_for_send)

    def append_modulation(self, mod: Modulation):
        NATIVE_METHODDS.dll.AUTDAppendModulation(self.p_cnt, mod.modulation_ptr)

    def append_modulation_sync(self, mod: Modulation):
        NATIVE_METHODDS.dll.AUTDAppendModulationSync(self.p_cnt, mod.modulation_ptr)

    def append_stm_gain(self, gain: Gain):
        NATIVE_METHODDS.dll.AUTDAppendSTMGain(self.p_cnt, gain.gain_ptr)

    def start_stm(self, freq):
        NATIVE_METHODDS.dll.AUTDStartSTModulation(self.p_cnt, freq)

    def stop_stm(self):
        NATIVE_METHODDS.dll.AUTDStopSTModulation(self.p_cnt)

    def finish_stm(self):
        NATIVE_METHODDS.dll.AUTDFinishSTModulation(self.p_cnt)

    def append_sequence(self, seq: Sequence):
        NATIVE_METHODDS.dll.AUTDAppendSequence(self.p_cnt, seq.seq_ptr)
