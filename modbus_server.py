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


def random_list_Boolean(list_len):
    device_list = []
    for i in range(list_len):
        device_list.append(random.randint(0, 1))
    return device_list


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


# LOGGER = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
# try:
def run(server, id, name, size):
    SLAVE = server.add_slave(id)
    SLAVE.add_block(name, cst.HOLDING_REGISTERS, 0, size)  # 地址0，长度4

    print("{}已启动".format(id))
    while 1:
        device_list = random_list_Boolean(size)
        print(name, device_list)
        SLAVE.set_values(name, 0, device_list)  # 改变在地址0处的寄存器的值
        # print(name,device_list)
        time.sleep(5)


def main():
    # server里的address需要写的树莓派的IP和需要开放的端口，注意开放相应的端口
    SERVER = modbus_tcp.TcpServer(port=502)
    # 服务启动
    SERVER.start()
    device_num = []
    # 建立第一个从机车位
    SLAVE_CW = SERVER.add_slave(1)
    device_num_cw = 1095
    SLAVE_CW.add_block('A', cst.HOLDING_REGISTERS, 0, device_num_cw)  # 地址0，长度4
    # 建立另一个从机照明
    SLAVE_ZM = SERVER.add_slave(2)
    device_num_zm = 55
    SLAVE_ZM.add_block('B', cst.HOLDING_REGISTERS, 0, device_num_zm)  # 地址0，长度10
    # 建立另一个从机门禁
    SLAVE_MJ = SERVER.add_slave(3)
    device_num_mj = 14
    SLAVE_MJ.add_block('C', cst.HOLDING_REGISTERS, 0, device_num_mj)  # 地址0，长度10
    # 建立另一个从机排风
    SLAVE_PF = SERVER.add_slave(4)
    device_num_pf = 81
    SLAVE_PF.add_block('D', cst.HOLDING_REGISTERS, 0, device_num_pf)  # 地址0，长度10
    # 建立另一个从机排水
    SLAVE_PS = SERVER.add_slave(5)
    device_num_ps = 34
    SLAVE_PS.add_block('E', cst.HOLDING_REGISTERS, 0, device_num_ps)  # 地址0，长度10
    # 建立另一个从机空调
    SLAVE_KT = SERVER.add_slave(6)
    device_num_kt = 16
    SLAVE_KT.add_block('F', cst.HOLDING_REGISTERS, 0, device_num_kt)  # 地址0，长度10
    # 建立另一个从机报警
    SLAVE_BJ = SERVER.add_slave(7)
    device_num_bj = 20
    SLAVE_BJ.add_block('G', cst.HOLDING_REGISTERS, 0, device_num_bj)  # 地址0，长度10
    device_num.append(device_num_cw)
    device_num.append(device_num_zm)
    device_num.append(device_num_mj)
    device_num.append(device_num_pf)
    device_num.append(device_num_ps)
    device_num.append(device_num_kt)
    device_num.append(device_num_bj)
    random_device_id_list = [x for x in range(1, 256)]
    device_id_list = random.sample(random_device_id_list, 7)
    device_id_list = [x for x in range(8, 15)]
    # print(device_id_list)
    name_list = [chr(i) for i in range(65, 72)]
    threads = []
    for i in range(len(device_id_list)):
        threads.append(threading.Thread(target=run, args=(SERVER, device_id_list[i], name_list[i], device_num[i],)))

    for i in threads:
        i.start()
    for i in threads:
        i.join()

    # 建立另一个从机能耗
    SLAVE_NH = SERVER.add_slave(8)
    device_num_nh = 222
    SLAVE_NH.add_block('H', cst.HOLDING_REGISTERS, 0, device_num_nh * 2)  # 地址0，长度10

    # print("------")
    # --------------------------------------车位--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_cw)
    #     SLAVE_CW.set_values('A', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------照明--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_zm)
    #     SLAVE_ZM.set_values('B', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------门禁--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_mj)
    #     SLAVE_MJ.set_values('C', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------排风--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_pf)
    #     SLAVE_PF.set_values('D', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------排水--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_ps)
    #     SLAVE_PS.set_values('E', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------空调--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_kt)
    #     SLAVE_KT.set_values('F', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------报警--------------------------------------
    # while 1:
    #     device_list = random_list_Boolean(device_num_bj)
    #     SLAVE_BJ.set_values('G', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    # --------------------------------------能源--------------------------------------
    # first_float_list = random_list_value(device_num_nh)
    # second_float_list = float_to_RTU(first_float_list)
    # third_float_list = final_list(second_float_list)
    # SLAVE_NH.set_values('H', 0, third_float_list)  # 改变在地址0处的寄存器的值
    # print(first_float_list)
    # print(third_float_list)
    # while 1:
    #     for i in range(len(first_float_list)):
    #         first_float_list[i] += round(random.uniform(0, 1))
    #     second_float_list = float_to_RTU(first_float_list)
    #     third_float_list = final_list(second_float_list)
    #     SLAVE_NH.set_values('H', 0, third_float_list)  # 改变在地址0处的寄存器的值
    #     print(first_float_list)
    #     print(third_float_list)
    #     time.sleep(5)

    # while 1:
    #     device_list = random_list_Boolean(device_num_cw)
    #     SLAVE_CW.set_values('A', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_zm)
    #     SLAVE_ZM.set_values('B', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_mj)
    #     SLAVE_MJ.set_values('C', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_pf)
    #     SLAVE_PF.set_values('D', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_ps)
    #     SLAVE_PS.set_values('E', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_kt)
    #     SLAVE_KT.set_values('F', 0, device_list)  # 改变在地址0处的寄存器的值
    #     device_list = random_list_Boolean(device_num_bj)
    #     SLAVE_BJ.set_values('G', 0, device_list)  # 改变在地址0处的寄存器的值
    #     time.sleep(5)
    #
    # SERVER.stop()


if __name__ == '__main__':
    main()
