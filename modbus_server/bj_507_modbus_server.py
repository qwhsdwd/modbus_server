#!/usr/bin/env python
# -- coding: utf_8 --
'''
 作者：曲伟豪
 时间：2021/9/28
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


def random_list_Boolean(list_len):
    device_list = []
    for i in range(list_len):
        device_list.append(random.randint(0, 1))
    return device_list


def main():
    # server里的address需要写的树莓派的IP和需要开放的端口，注意开放相应的端口
    SERVER = modbus_tcp.TcpServer(port=507)
    # 服务启动
    SERVER.start()
    # 建立另一个从机报警
    SLAVE_BJ = SERVER.add_slave(7)
    device_num_bj = 20
    SLAVE_BJ.add_block('G', cst.HOLDING_REGISTERS, 0, device_num_bj)  # 地址0，长度10

    # --------------------------------------报警--------------------------------------
    t = 0
    while 1:
        device_list = random_list_Boolean(device_num_bj)
        SLAVE_BJ.set_values('G', 0, device_list)  # 改变在地址0处的寄存器的值
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        t += 1
        print(time_now + "\t\t\t\t\t\t数据第{}次模拟".format(t))

        time.sleep(5)


if __name__ == '__main__':
    print("欢迎进入报警数据模拟程序")
    print("程序端口为505，刷新间隔为5秒")
    main()
