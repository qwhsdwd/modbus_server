import struct
import random
import time
from decimal import Decimal


def WriteFloat(value, reverse=False):
    y_bytes = struct.pack('!f', value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    n, m = y_hex[:-4], y_hex[-4:]
    n, m = int(n, 16), int(m, 16)
    if reverse:
        v = [n, m]
    else:
        v = [m, n]
    return v


def random_list_value(list_len):
    device_list = []
    for i in range(list_len):
        random_num = random.uniform(10.4, 20.2)
        device_list.append(random_num)
    return device_list

def float_to_RTU(num_list):
    new_device_list = []
    for i in num_list:
        new_device_list.append(WriteFloat(i))
    return new_device_list

def final_list(float_double_list):
    new_list=[]
    for i in range(len(float_double_list)):
        for j in range(2):
            new_list.append(float_double_list[i][j])
    return new_list


if __name__ == '__main__':
    # print(WriteFloat(12.32))
    # while 1:
    first_float_list = random_list_value(20)
    second_float_list=float_to_RTU(first_float_list)
    third_float_list=final_list(second_float_list)
    while 1:
        for i in range(len(first_float_list)):
            first_float_list[i]+=random.uniform(1,5)
        second_float_list=float_to_RTU(first_float_list)
        third_float_list=final_list(second_float_list)
        time.sleep(5)


    print(first_float_list)
    print(second_float_list)
    print(third_float_list)

