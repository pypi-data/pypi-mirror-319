# -*- coding: utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.
import sys
import base64
from ctypes import *

class SamContext(Structure):
    _fields_ = [
        ("imp", c_void_p)
    ]

class SamContentPackager():
    def __init__(
        self,
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

        self.packager = cdll.LoadLibrary(so_path)
        self.context_ptr = pointer(SamContext())
        self.verbose = verbose

    def __del__(self):
        pass

    def SamPkgInit(
        self,
        pid: str,
        psw: str) -> int:
        ret = self.packager.InitLicenseContext(self.context_ptr)
        if ret != 0:
            print("Init Sam Context Fail - ", ret)
            return -1

        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())
        ret = self.packager.GenerateLicenseInfo(self.context_ptr, pid_str, psw_str)
        if ret != 0:
            print("Generate License Info Fail - ", ret)
            return -1
 
        lic_id = create_string_buffer(64)
        ret = self.packager.GetLicenseId(self.context_ptr, lic_id)
        if ret != 0:
            print("Get License ID Fail - ", ret)
            return -1

        if self.verbose == True:
            print("lic_id: ", lic_id.value.decode())

        return 0
       
    def SamPkgEncrypt(self, content: str) -> str:
        enc_mode = c_uint(2)
        content = content.encode()

        item_data = create_string_buffer(content)
        item_size = c_uint(len(content))

        if self.verbose == True:
            print("item_size: ", item_size.value)

        out_size = c_uint()
        ret = self.packager.doItemContentEncrypt(
                       self.context_ptr, enc_mode,
                       item_data, item_size, POINTER(c_ubyte)(), pointer(out_size))
        if ret != 0:
            print("Do Item Content Encrypt Fail - ", ret)
            return None

        if self.verbose == True:
            print("out_size: ", out_size.value)

        out_data = (c_ubyte * out_size.value)()
        ret = self.packager.doItemContentEncrypt(
                     self.context_ptr, enc_mode,
                     item_data, item_size, out_data, pointer(out_size))
        if ret != 0:
            print("Do Item Content Encrypt Fail - ", ret)
            return None

        return base64.b64encode(out_data)

    def SamPkgFinalize(self):
        self.packager.FinalizeLicenseContext(self.context_ptr)

    def SamPkgEncryptContents(
        self,
        pid: str,
        psw: str,
        contents: list[str]) -> list[str]:

        out_contents = []

        enc_mode = c_uint(2)
        context_ptr = pointer(SamContext())

        ret = self.packager.InitLicenseContext(context_ptr)
        if ret != 0:
            print("Init Sam Context Fail - ", ret)
            return -1

        pid_str = create_string_buffer(pid.encode())
        psw_str = create_string_buffer(psw.encode())
        ret = self.packager.GenerateLicenseInfo(context_ptr, pid_str, psw_str)
        if ret != 0:
            print("Generate License Info Fail - ", ret)
            self.packager.FinalizeLicenseContext(context_ptr)
            return -1
 
        for i in range(len(contents)):
            content = contents[i].encode()

            item_size = c_uint(len(content))
            item_data = create_string_buffer(content)

            out_size = c_uint()
            ret = self.packager.doItemContentEncrypt(
                           context_ptr, enc_mode,
                           item_data, item_size, POINTER(c_ubyte)(), pointer(out_size))
            if ret != 0:
                print("Do Item Content Encrypt Fail - ", ret)
                self.packager.FinalizeLicenseContext(context_ptr)
                return None

            if self.verbose == True:
                print("out_size: ", out_size.value)

            out_data = (c_ubyte * out_size.value)()
            ret = self.packager.doItemContentEncrypt(
                         context_ptr, enc_mode,
                         item_data, item_size, out_data, pointer(out_size))
            if ret != 0:
                print("Do Item Content Encrypt Fail - ", ret)
                self.packager.FinalizeLicenseContext(context_ptr)
                return None

            out_content = base64.b64encode(out_data)
            out_contents.append(out_content.decode())

        self.packager.FinalizeLicenseContext(context_ptr)

        return out_contents

