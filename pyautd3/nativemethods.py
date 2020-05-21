'''
File: nativemethods.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 21/05/2020
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import threading
import ctypes
from ctypes import c_void_p, c_bool, c_int, POINTER, c_double, c_long, c_char_p, c_ubyte


class Singleton(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Nativemethods(metaclass=Singleton):
    dll = None

    def init_dll(self, dlllocation):
        self.dll = ctypes.CDLL(dlllocation)

        self.__init_controller()
        self.__init_property()
        self.__init_gain()
        self.__init_modulation()
        self.__init_low_level_interface()
        self.__init_link()

    def __init_controller(self):
        self.dll.AUTDCreateController.argtypes = [POINTER(c_void_p)]
        self.dll.AUTDCreateController.restypes = [None]

        self.dll.AUTDOpenController.argtypes = [c_void_p, c_int, c_char_p]
        self.dll.AUTDOpenController.restypes = [c_int]

        self.dll.AUTDOpenControllerWith.argtypes = [c_void_p, c_void_p]
        self.dll.AUTDOpenControllerWith.restypes = [c_int]

        self.dll.AUTDAddDevice.argtypes = [c_void_p, c_double, c_double, c_double, c_double, c_double, c_double, c_int]
        self.dll.AUTDAddDevice.restypes = [c_int]

        self.dll.AUTDAddDeviceQuaternion.argtypes = [c_void_p, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_int]
        self.dll.AUTDAddDeviceQuaternion.restypes = [c_int]

        self.dll.AUTDDelDevice.argtypes = [c_void_p, c_int]
        self.dll.AUTDDelDevice.restypes = [None]

        self.dll.AUTDCloseController.argtypes = [c_void_p]
        self.dll.AUTDCloseController.restypes = [None]

        self.dll.AUTDFreeController.argtypes = [c_void_p]
        self.dll.AUTDFreeController.restypes = [None]

        self.dll.AUTDSetSilentMode.argtypes = [c_void_p, c_bool]
        self.dll.AUTDSetSilentMode.restypes = [None]

        self.dll.AUTDCalibrateModulation.argtypes = [c_void_p]
        self.dll.AUTDCalibrateModulation.restypes = [c_bool]

        self.dll.AUTDGetAdapterPointer.argtypes = [POINTER(c_void_p)]
        self.dll.AUTDGetAdapterPointer.restypes = [c_int]

        self.dll.AUTDGetAdapter.argtypes = [c_void_p, c_int, c_char_p, c_char_p]
        self.dll.AUTDGetAdapter.restypes = [None]

        self.dll.AUTDFreeAdapterPointer.argtypes = [c_void_p]
        self.dll.AUTDFreeAdapterPointer.restypes = [None]

        self.dll.AUTDGetFirmwareInfoListPointer.argtypes = [c_void_p, POINTER(c_void_p)]
        self.dll.AUTDGetFirmwareInfoListPointer.restypes = [c_int]

        self.dll.AUTDGetFirmwareInfo.argtypes = [c_void_p, c_int, c_char_p, c_char_p]
        self.dll.AUTDGetFirmwareInfo.restypes = [None]

        self.dll.AUTDFreeFirmwareInfoListPointer.argtypes = [c_void_p]
        self.dll.AUTDFreeFirmwareInfoListPointer.restypes = [None]

    def __init_property(self):
        self.dll.AUTDIsOpen.argtypes = [c_void_p]
        self.dll.AUTDIsOpen.restypes = [c_bool]

        self.dll.AUTDIsSilentMode.argtypes = [c_void_p]
        self.dll.AUTDIsSilentMode.restypes = [c_bool]

        self.dll.AUTDNumDevices.argtypes = [c_void_p]
        self.dll.AUTDNumDevices.restypes = [c_int]

        self.dll.AUTDNumTransducers.argtypes = [c_void_p]
        self.dll.AUTDNumTransducers.restypes = [c_int]

        self.dll.AUTDRemainingInBuffer.argtypes = [c_void_p]
        self.dll.AUTDRemainingInBuffer.restypes = [c_long]

    def __init_gain(self):
        self.dll.AUTDFocalPointGain.argtypes = [POINTER(c_void_p), c_double, c_double, c_double, c_ubyte]
        self.dll.AUTDFocalPointGain.restypes = [None]

        self.dll.AUTDGroupedGain.argtypes = [POINTER(c_void_p), POINTER(c_int), POINTER(c_void_p), c_int]
        self.dll.AUTDGroupedGain.restypes = [None]

        self.dll.AUTDBesselBeamGain.argtypes = [POINTER(c_void_p), c_double, c_double, c_double, c_double, c_double, c_double, c_double]
        self.dll.AUTDBesselBeamGain.restypes = [None]

        self.dll.AUTDPlaneWaveGain.argtypes = [POINTER(c_void_p), c_double, c_double, c_double]
        self.dll.AUTDPlaneWaveGain.restypes = [None]

        self.dll.AUTDCustomGain.argtypes = [POINTER(c_void_p), POINTER(c_ubyte), c_int]
        self.dll.AUTDCustomGain.restypes = [None]

        self.dll.AUTDHoloGain.argtypes = [POINTER(c_void_p), POINTER(c_double), POINTER(c_double), c_int]
        self.dll.AUTDHoloGain.restypes = [None]

        self.dll.AUTDTransducerTestGain.argtypes = [POINTER(c_void_p), c_int, c_int, c_int]
        self.dll.AUTDTransducerTestGain.restypes = [None]

        self.dll.AUTDNullGain.argtypes = [POINTER(c_void_p)]
        self.dll.AUTDNullGain.restypes = [None]

        self.dll.AUTDDeleteGain.argtypes = [c_void_p]
        self.dll.AUTDDeleteGain.restypes = [None]

    def __init_modulation(self):
        self.dll.AUTDModulation.argtypes = [POINTER(c_void_p), c_ubyte]
        self.dll.AUTDModulation.restypes = [None]

        self.dll.AUTDRawPCMModulation.argtypes = [POINTER(c_void_p), c_char_p, c_double]
        self.dll.AUTDRawPCMModulation.restypes = [None]

        self.dll.AUTDRawPCMModulation.argtypes = [POINTER(c_void_p), c_int]
        self.dll.AUTDRawPCMModulation.restypes = [None]

        self.dll.AUTDSineModulation.argtypes = [POINTER(c_void_p), c_int, c_double, c_double]
        self.dll.AUTDSineModulation.restypes = [None]

        self.dll.AUTDWavModulation.argtypes = [POINTER(c_void_p), c_char_p]
        self.dll.AUTDWavModulation.restypes = [None]

        self.dll.AUTDDeleteModulation.argtypes = [c_void_p]
        self.dll.AUTDDeleteModulation.restypes = [None]

    def __init_link(self):
        self.dll.AUTDSOEMLink.argtypes = [POINTER(c_void_p), c_char_p, c_int]
        self.dll.AUTDSOEMLink.restypes = [None]

        self.dll.AUTDEtherCATLink.argtypes = [POINTER(c_void_p), c_char_p, c_char_p]
        self.dll.AUTDEtherCATLink.restypes = [None]

        self.dll.AUTDLocalEtherCATLink.argtypes = [POINTER(c_void_p)]
        self.dll.AUTDLocalEtherCATLink.restypes = [None]

        self.dll.AUTDEmulatorLink.argtypes = [POINTER(c_void_p), c_char_p, c_int, c_void_p]
        self.dll.AUTDEmulatorLink.restypes = [None]

    def __init_low_level_interface(self):
        self.dll.AUTDAppendGain.argtypes = [c_void_p, c_void_p]
        self.dll.AUTDAppendGain.restypes = [None]

        self.dll.AUTDAppendGainSync.argtypes = [c_void_p, c_void_p, c_bool]
        self.dll.AUTDAppendGainSync.restypes = [None]

        self.dll.AUTDAppendModulation.argtypes = [c_void_p, c_void_p]
        self.dll.AUTDAppendModulation.restypes = [None]

        self.dll.AUTDAppendModulationSync.argtypes = [c_void_p, c_void_p]
        self.dll.AUTDAppendModulationSync.restypes = [None]

        self.dll.AUTDAppendSTMGain.argtypes = [c_void_p, c_void_p]
        self.dll.AUTDAppendSTMGain.restypes = [None]

        self.dll.AUTDStartSTModulation.argtypes = [c_void_p, c_double]
        self.dll.AUTDStartSTModulation.restypes = [None]

        self.dll.AUTDStopSTModulation.argtypes = [c_void_p]
        self.dll.AUTDStopSTModulation.restypes = [None]

        self.dll.AUTDFinishSTModulation.argtypes = [c_void_p]
        self.dll.AUTDFinishSTModulation.restypes = [None]
