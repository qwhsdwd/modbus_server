import ctypes
import threading
from struct import pack
import random
from time import sleep

import modbus_tk
import modbus_tk.defines
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
from configparser import ConfigParser
from configparser import DuplicateSectionError
from time import strftime


# from GUI import showinfo


def float_to_RTU(num_list):
    new_device_list = []
    for i in num_list:
        new_device_list.append(WriteFloat(i))
    return new_device_list


def WriteFloat(float_value, reverse=False):
    y_bytes = pack('!f', float_value)
    # y_hex = bytes.hex(y_bytes)
    y_hex = ''.join(['%02x' % i for i in y_bytes])
    n, m = y_hex[:-4], y_hex[-4:]
    n, m = int(n, 16), int(m, 16)
    if reverse:
        v = [n, m]
    else:
        v = [m, n]
    return v


def float_final_list(float_double_list):
    new_list = []
    for i in range(len(float_double_list)):
        for j in range(2):
            new_list.append(float_double_list[i][j])
    return new_list


def random_list_Boolean(size):
    device_list = []
    for i in range(size):
        device_list.append(random.randint(0, 1))
    return device_list


def random_list_int(size, random_start, random_end):
    device_list = []
    for i in range(size):
        random_num = random.randint(random_start, random_end)
        device_list.append(random_num)
    return device_list


def random_list_value(size, random_start, random_end, precision=0):
    device_list = []
    for i in range(size):
        random_num = random.uniform(random_start, random_end)
        if precision == 0:
            device_list.append(random_num)
        else:
            device_list.append(round(random_num, precision))
    return device_list


def random_list_float(size, random_start, random_end, precision=0):
    return 0
    pass


def write_to_logFile(text):
    realtime = strftime("%Y-%m-%d %H:%M:%S ")
    with open("modbus.log", "a") as f:
        f.write("{}\t\t\t\t\t{}\n".format(realtime, text))


cf = ConfigParser()
cf.read("./config.ini")


def great_block_and_run(SERVER, slave_id, block_name, address, size, slave_type, loop_interval_time,
                        *random_num):
    # write_to_logFile("slave{}启动".format(slave_id))
    # showinfo("slave{}启动".format(slave_id))
    print("slave{}启动".format(slave_id))
    # 创建block
    # print(slave_id, block_name, address, size, slave_type, loop_interval_time)
    SLAVE = SERVER.add_slave(slave_id)
    if slave_type == "signed":
        SLAVE.add_block(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size)  # 地址0，长度4
        t = 0
        while 1:
            t += 1
            device_list = random_list_Boolean(size)
            SLAVE.set_values(block_name, address, device_list)  # 改变在地址0处的寄存器的值
            print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            sleep(loop_interval_time)

    elif slave_type == "float":
        SLAVE.add_block(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size * 2)  # 地址0，长度4
        t = 0
        first_float_list = random_list_value(size, int(random_num[0][0]), int(random_num[0][1]))
        second_float_list = float_to_RTU(first_float_list)
        third_float_list = float_final_list(second_float_list)
        SLAVE.set_values(block_name, address, third_float_list)  # 改变在地址0处的寄存器的值
        while 1:
            for i in range(len(first_float_list)):
                first_float_list[i] += round(random.uniform(int(random_num[0][2]), int(random_num[0][3])))
            second_float_list = float_to_RTU(first_float_list)
            third_float_list = float_final_list(second_float_list)
            SLAVE.set_values(block_name, address, third_float_list)  # 改变在地址0处的寄存器的值
            t += 1
            print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            sleep(loop_interval_time)


class MyModbus():
    def __init__(self):
        self.port = cf.get("modbus_tk", "port")
        self.SERVER = modbus_tk.modbus_tcp.TcpServer(int(self.port))
        # 服务启动
        self.SERVER.start()

    def great_block_and_run(self, slave_id, block_name, address, size, slave_type, loop_interval_time,
                            *random_num):
        # write_to_logFile("slave{}启动".format(slave_id))
        # showinfo("slave{}启动".format(slave_id))
        print("slave{}启动".format(slave_id))
        # 创建block
        # print(slave_id, block_name, address, size, slave_type, loop_interval_time)
        SLAVE = self.SERVER.add_slave(slave_id)
        if slave_type == "signed":
            SLAVE.add_block(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size)  # 地址0，长度4
            t = 0
            while 1:
                t += 1
                device_list = random_list_Boolean(size)
                SLAVE.set_values(block_name, address, device_list)  # 改变在地址0处的寄存器的值
                print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                # showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                # write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                sleep(loop_interval_time)

        elif slave_type == "float":
            SLAVE.add_block(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size * 2)  # 地址0，长度4
            t = 0
            first_float_list = random_list_value(size, int(random_num[0][0]), int(random_num[0][1]))
            second_float_list = float_to_RTU(first_float_list)
            third_float_list = float_final_list(second_float_list)
            SLAVE.set_values(block_name, address, third_float_list)  # 改变在地址0处的寄存器的值
            while 1:
                for i in range(len(first_float_list)):
                    first_float_list[i] += round(random.uniform(int(random_num[0][2]), int(random_num[0][3])))
                second_float_list = float_to_RTU(first_float_list)
                third_float_list = float_final_list(second_float_list)
                SLAVE.set_values(block_name, address, third_float_list)  # 改变在地址0处的寄存器的值
                t += 1
                print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                # showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                # write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
                sleep(loop_interval_time)
