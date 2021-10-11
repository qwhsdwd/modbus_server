#!/usr/bin/env python
# -- coding: utf_8 --
'''
 作者：weizy
 时间：2019/7/23
 简介：modbus协议从机测试脚本
 '''
import struct
from decimal import Decimal
import sys
import threading
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
import random
import time


def random_list_value(list_len):
    device_list = []
    for i in range(list_len):
        random_num = random.uniform(1000, 2000)
        device_list.append(round(random_num, 2))
    return device_list


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


def float_to_RTU(num_list):
    new_device_list = []
    for i in num_list:
        new_device_list.append(WriteFloat(i))
    return new_device_list


def final_list(float_double_list):
    new_list = []
    for i in range(len(float_double_list)):
        for j in range(2):
            new_list.append(float_double_list[i][j])
    return new_list


# try:
def main():
    # server里的address需要写的树莓派的IP和需要开放的端口，注意开放相应的端口
    SERVER = modbus_tcp.TcpServer(port=508)
    # 服务启动
    SERVER.start()
    # 建立另一个从机能耗
    SLAVE_NH = SERVER.add_slave(8)
    device_num_nh = 222
    SLAVE_NH.add_block('H', cst.HOLDING_REGISTERS, 0, device_num_nh * 2)  # 地址0，长度10

    # --------------------------------------能源--------------------------------------
    first_float_list = random_list_value(device_num_nh)
    second_float_list = float_to_RTU(first_float_list)
    third_float_list = final_list(second_float_list)
    SLAVE_NH.set_values('H', 0, third_float_list)  # 改变在地址0处的寄存器的值
    t = 0
    while 1:
        for i in range(len(first_float_list)):
            first_float_list[i] += round(random.uniform(0, 1))
        second_float_list = float_to_RTU(first_float_list)
        third_float_list = final_list(second_float_list)
        SLAVE_NH.set_values('H', 0, third_float_list)  # 改变在地址0处的寄存器的值
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t += 1
        print(time_now+"\t\t\t\t\t\t数据第{}次模拟".format(t))
        time.sleep(600)


if __name__ == '__main__':
    print("欢迎进入能源数据模拟程序")
    print("程序端口为508，刷新间隔为10分钟")
    main()
