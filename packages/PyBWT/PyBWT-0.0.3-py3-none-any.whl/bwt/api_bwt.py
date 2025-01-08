import os
import ctypes


def create():
    pass

def parse():
    pass

def verify():
    pass

def test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)

    c_lib = ctypes.CDLL(os.path.join(dir_path, "libbwt.so"))

    c_lib.verify_bwt.argtypes = [ctypes.c_ubyte, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t]
    c_lib.verify_bwt.restype = ctypes.c_bool

    print(c_lib.verify_bwt(1,
                     b'AUJXVBM3_v8Aa2V5MQN2YWx1ZTEDa2V5MgN2YWx1ZTIDALh3LhUs8-utw-5HzUegn6HaGGSL61GbzGNJdLIcS0NNOQbVC2Rz0EV2hM6lOGzAjQ',
                     b'demo\x00key',
                     8))



