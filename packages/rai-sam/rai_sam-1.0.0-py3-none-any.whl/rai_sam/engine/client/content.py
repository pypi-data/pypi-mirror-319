# -*- coding: utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.
import sys
import base64
from ctypes import *

pro_name = "product_name_demo"
dev_name = "device_name_demo"

class SamContext(Structure):
    _fields_ = [
        ("imp", c_void_p)
    ]

class SamContentClient():
    def __init__(
        self,
        so_name = "libsam_client.so",
        module_name = "rai_sam",
        verbose = False,
    ):
        super().__init__()

        module = sys.modules.get(module_name)
        module_path = module.__path__
        so_path = module_path[0] + "/libs/" + so_name

        if verbose == True:
            print("Load Sam Client Library: ", so_path)

        self.client = cdll.LoadLibrary(so_path)
        self.context_ptr = pointer(SamContext())
        self.verbose = verbose

    def __del__(self):
        pass

    def SamClientInit(
        self,
        pid: str,
        psw: str) -> int:

        self.pid = pid
        self.psw = psw

        pro_name_str = create_string_buffer(pro_name.encode())
        dev_name_str = create_string_buffer(dev_name.encode())
        ret = self.client.sam_init_context(pro_name_str, dev_name_str, self.context_ptr)   
        if ret != 0:
            print("Sam Init Context Fail - ", ret)
            return -1
        else:
            return 0
       
    def SamClientDecrypt(self, content: str) -> str:
        password_str = create_string_buffer(self.psw.encode())

        content_decode = base64.b64decode(content)
        item_size = c_uint(len(content_decode))
        item_data = (c_ubyte * item_size.value)()
        memmove(item_data, content_decode, len(content_decode))

        out_size = item_size
        out_data = (c_ubyte * out_size.value)()

        ret = self.client.sam_on_item_decryption(
                   self.context_ptr, password_str,
                   item_data, item_size, out_data, pointer(out_size))
        if ret != 0:
            print("Sam Item Content Decryption Fail - ", ret)
            return None

        if self.verbose == True:
            print("out_size: ", out_size.value)

        out_data_str = create_string_buffer(out_size.value)
        memmove(out_data_str, out_data, out_size.value)

        if self.verbose == True:
            print("out_data: ", out_data_str.value)

        return out_data_str.value.decode()

    def SamClientFinalize(self):
        self.client.sam_final_context(self.context_ptr)

    def SamClientDecryptContents(
        self,
        pid: str,
        psw: str,
        contents: list[str]) -> list[str]:

        out_contents = []

        context_ptr = pointer(SamContext())
        pro_name_str = create_string_buffer(pro_name.encode())
        dev_name_str = create_string_buffer(dev_name.encode())
        ret = self.client.sam_init_context(pro_name_str, dev_name_str, context_ptr)   
        if ret != 0:
            print("Sam Init Context Fail - ", ret)
            return None

        password_str = create_string_buffer(psw.encode())

        for i in range(len(contents)):
            content = base64.b64decode(contents[i])

            item_size = c_uint(len(content))
            item_data = (c_ubyte * item_size.value)()
            memmove(item_data, content, len(content))

            out_size = item_size
            out_data = (c_ubyte * out_size.value)()

            ret = self.client.sam_on_item_decryption(
                      context_ptr, password_str,
                      item_data, item_size, out_data, pointer(out_size))
            if ret != 0:
                print("Sam Item Content Decryption Fail - ", ret)
                self.client.sam_final_context(context_ptr)
                return None

            if self.verbose == True:
                print("out_size: ", out_size.value)

            out_data_str = create_string_buffer(out_size.value)
            memmove(out_data_str, out_data, out_size.value)

            out_content = out_data_str.value.decode()
            out_contents.append(out_content)

            if self.verbose == True:
                print("out_content: ", out_content)

        self.client.sam_final_context(context_ptr)

        return out_contents

