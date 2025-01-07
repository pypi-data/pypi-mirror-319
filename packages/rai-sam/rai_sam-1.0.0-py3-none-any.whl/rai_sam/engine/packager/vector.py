# -*- coding: utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.
import sys
from ctypes import *

class SamContext(Structure):
    _fields_ = [
        ("imp", c_void_p)
    ]

class SamVectorPackager():

    def __init__(
        self,
        beta = float(0.87),
        scale = float(293.50),
        so_name = "libsam_packager.so",
        module_name = "rai_sam",
        verbose = False,
    ):
        super().__init__()

        module = sys.modules.get(module_name)
        module_path = module.__path__
        so_path = module_path[0] + "/libs/" + so_name

        if verbose == True:
            print("Load Sam Packager Library: ", so_path)

        self.beta = c_float(beta)
        self.scale = c_float(scale)

        self.packager = cdll.LoadLibrary(so_path)
        self.context_ptr = pointer(SamContext())
        self.verbose = verbose

    def __del__(self):
        pass

    def SamPkgInit(self) -> int:
        ret = self.packager.InitLicenseContext(self.context_ptr)
        if ret != 0:
            print("Init Sam Context Fail - ", ret)
            return -1

        ret = self.packager.setVectorConfig(self.context_ptr, self.beta, self.scale)
        if ret != 0:
            print("Set Vector Config Fail\n")
            return None

        return 0
       
    def SamPkgEncrypt(self, pid: str, psw: str, vector: list) -> list:
        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())

        in_size = c_uint(len(vector))
        in_data = (c_float * in_size.value)()
        for i in range(len(vector)):
            in_data[i] = vector[i]

        if self.verbose == True:
            print("in_size: ", in_size.value)

        out_data = (c_float * in_size.value)()
        ret = self.packager.doVectorContentEncrypt(
                     self.context_ptr, pid_str, psw_str,
                     in_data, in_size, out_data)
        if ret != 0:
            print("Do Vector Content Encrypt Fail - ", ret)
            return None

        enc_vector = []
        for i in range(in_size.value):
            enc_vector.append(out_data[i])

        return enc_vector

    def SamPkgDecrypt(self, pid: str, psw: str, vector: list) -> list:
        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())

        in_size = c_uint(len(vector))
        in_data = (c_float * in_size.value)()
        for i in range(len(vector)):
            in_data[i] = vector[i]

        if self.verbose == True:
            print("in_size: ", in_size.value)

        out_data = (c_float * in_size.value)()
        ret = self.packager.doVectorContentDecrypt(
                     self.context_ptr, pid_str, psw_str,
                     in_data, in_size, out_data)
        if ret != 0:
            print("Do Vector Content Decrypt Fail - ", ret)
            return None

        dec_vector = []
        for i in range(in_size.value):
            dec_vector.append(out_data[i])

        return dec_vector

    def SamPkgFinalize(self):
        self.packager.FinalizeLicenseContext(self.context_ptr)

    def SamPkgEncryptVectors(
        self,
        pid: str,
        psw: str,
        vectors: list[list]) -> list[list]:

        enc_vectors = []

        ret = self.packager.InitLicenseContext(self.context_ptr)
        if ret != 0:
            print("Init Sam Context Fail - ", ret)
            return -1

        ret = self.packager.setVectorConfig(self.context_ptr, self.beta, self.scale)
        if ret != 0:
            print("Set Vector Config Fail\n")
            self.packager.FinalizeLicenseContext(self.context_ptr)
            return None

        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())

        for i in range(len(vectors)):
            vector = vectors[i]

            in_size = c_uint(len(vector))
            in_data = (c_float * in_size.value)()
            for i in range(len(vector)):
                in_data[i] = vector[i]

            if self.verbose == True:
                print("in_size: ", in_size.value)

            out_data = (c_float * in_size.value)()
            ret = self.packager.doVectorContentEncrypt(
                         self.context_ptr, pid_str, psw_str,
                         in_data, in_size, out_data)
            if ret != 0:
                print("Do Vector Content Encrypt Fail - ", ret)
                self.packager.FinalizeLicenseContext(self.context_ptr)
                return None

            enc_vector = []
            for i in range(in_size.value):
                enc_vector.append(out_data[i])

            enc_vectors.append(enc_vector)

        self.packager.FinalizeLicenseContext(self.context_ptr)

        return enc_vectors

    def SamPkgDecryptVectors(
        self,
        pid: str,
        psw: str,
        vectors: list[list]) -> list[list]:

        dec_vectors = []

        ret = self.packager.InitLicenseContext(self.context_ptr)
        if ret != 0:
            print("Init Sam Context Fail - ", ret)
            return -1

        ret = self.packager.setVectorConfig(self.context_ptr, self.beta, self.scale)
        if ret != 0:
            print("Set Vector Config Fail\n")
            self.packager.FinalizeLicenseContext(self.context_ptr)
            return None

        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())

        for i in range(len(vectors)):
            vector = vectors[i]

            in_size = c_uint(len(vector))
            in_data = (c_float * in_size.value)()
            for i in range(len(vector)):
                in_data[i] = vector[i]

            if self.verbose == True:
                print("in_size: ", in_size.value)

            out_data = (c_float * in_size.value)()
            ret = self.packager.doVectorContentDecrypt(
                         self.context_ptr, pid_str, psw_str,
                         in_data, in_size, out_data)
            if ret != 0:
                print("Do Vector Content Decrypt Fail - ", ret)
                self.packager.FinalizeLicenseContext(self.context_ptr)
                return None

            dec_vector = []
            for i in range(in_size.value):
                dec_vector.append(out_data[i])

            dec_vectors.append(dec_vector)

        self.packager.FinalizeLicenseContext(self.context_ptr)

        return dec_vectors


