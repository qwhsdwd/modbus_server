import multiprocessing
from time import strftime, sleep
from tkinter import *
import tkinter.messagebox
from tkinter import messagebox
from configparser import ConfigParser
from configparser import DuplicateSectionError
from threading import Thread
from modbus_tk import modbus_tcp
import modbus_tk
import random
from struct import pack
from sys import exit
from os import path,remove

threads = []
m1 = multiprocessing.Process()
port = 502
log_file_name = "modbus.log"
config_file_name = "modbus_config.ini"


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


def multiprocessing_(func):
    global m1
    m1 = multiprocessing.Process(target=func)
    m1.start()
    # m1.join()


def my_mes1(text):
    messagebox.showerror("出现错误", text)


def my_mes2():
    ret = messagebox.askyesno("读取成功", "读取成功，是否开始运行？")
    if ret:
        multiprocessing_(run)


def write_to_logFile(text):
    realtime = strftime("%Y-%m-%d %H:%M:%S ")
    with open(path.join(path.dirname(sys.argv[0]), 'modbus.log'), "a") as f:
        f.write("{}\t\t\t{}\n".format(realtime, text))


def verify_config(configtext):
    global config
    config = ConfigParser()
    try:
        config.read_string(configtext)
    except DuplicateSectionError:
        return "section重复，请检查"
        # my_mes1("section重复，请检查")
    # try
    # config = config
    config.read_string(configtext)
    secs = config.sections()
    block_test_name_list = []
    # 所有section中block的列表
    slave_id_test_name_list = []
    # 所有section中slave_id的列表
    for i in range(len(secs[1:])):
        # 遍历section
        if config.get(secs[1:][i], "type") != "signed" and config.get(secs[1:][i], "type") != "float":
            # type是float或者signed之外的话报错且退出程序
            # print(config.get(secs[1:][i], "type"))
            return "{}中的type 请输入 signed 或者 float".format(secs[1:][i])
            # my_mes1("{}中的type 请输入 signed 或者 float".format(secs[1:][i]))
            # print("{}中的type 请输入 signed 或者 float".format(secs[1:][i]))
            # exit(1)
        if config.get(secs[1:][i], "type") == "signed" and config.options(secs[1:][i]) != ['type', 'slave_id',
                                                                                           'block_name',
                                                                                           'address',
                                                                                           'quantity',
                                                                                           'loop_interval_time']:
            # type是signed配置中key不对的话则退出程序
            return "{}中section中配置有错误，请检查后运行".format(secs[1:][i])
            # my_mes1("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            # print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            # exit(1)
        if config.get(secs[1:][i], "type") == "float" and config.options(secs[1:][i]) != ['type', 'slave_id',
                                                                                          'block_name',
                                                                                          'address',
                                                                                          'quantity',
                                                                                          'loop_interval_time',
                                                                                          "random_start",
                                                                                          "random_end",
                                                                                          "random_add_start",
                                                                                          "random_add_end"]:
            # type是float配置中key不对的话则退出程序
            # my_mes1("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            return "{}中section中配置有错误，请检查后运行".format(secs[1:][i])
            # print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            # exit(1)
        if int(config.get(secs[1:][i], "slave_id")) < 1 or int(config.get(secs[1:][i], "slave_id")) >= 256:
            # my_mes1("{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i]))
            return "{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i])
            # print("{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i]))
            # exit(1)
        block_test_name_list.append(config.get(secs[1:][i], "block_name"))
        # 添加block_name 到列表
        slave_id_test_name_list.append(config.get(secs[1:][i], "slave_id"))
    if len(block_test_name_list) != len(set(block_test_name_list)):
        # my_mes1("block_name中有重复，请检查后运行")
        # print("block_name中有重复，请检查后运行")
        return 'block_name中有重复，请检查后运行"'
        # exit(1)
    if len(slave_id_test_name_list) != len(set(slave_id_test_name_list)):
        # my_mes1("slave_id中有重复,请检查后运行")
        # print("slave_id中有重复,请检查后运行")
        return 'save_d中有重复，请检查后运行"'
        # exit(1)
    # finally:
    #     return 1
    # ------------------------------------检测配置文件正确性------------------------------------


def write_config():
    global port, config
    log_signal = 1
    # config = ConfigParser()
    configread = text1.get(0.0, END)
    if len(configread) <= 1:
        my_mes1("请先在文本框写入配置")
    # verify_config(configread)
    # print(verify_config(configread))
    else:
        if verify_config(configread) is None:
            # config.read_string(configtext)
            with open("modbus_config.ini","w") as f:
                f.write(configread)
            # config_list.append(config)
            # print(config_list)
            # secs1 = config.sections()
            port = config.get("modbus_tk", "port")
            my_mes2()
        else:
            my_mes1(verify_config(configread))


def write_template():
    # pass
    text1.delete(0.0, END)
    text1.insert(END, configtext)


def great_block_and_run(SERVER, slave_id, block_name, address, size, slave_type, loop_interval_time,
                        *random_num):
    write_to_logFile("slave{}启动".format(slave_id))
    # showinfo("slave{}启动".format(slave_id))
    # print("slave{}启动".format(slave_id))
    # 创建block
    # print(slave_id, block_name, address, size, slave_type, loop_interval_time)
    SLAVE = SERVER.add_slave(slave_id)
    if slave_type == "signed":
        SLAVE.add_block(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size)  # 地址0，长度4
        # print(block_name, modbus_tk.defines.HOLDING_REGISTERS, address, size)
        t = 0
        while 1:
            t += 1
            device_list = random_list_Boolean(size)
            SLAVE.set_values(block_name, address, device_list)  # 改变在地址0处的寄存器的值
            # print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
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
            # print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            sleep(loop_interval_time)


def run():
    global MyModbus,config_list
    config=ConfigParser()
    config.read('modbus_config.ini')
    secs = config.sections()
    SERVER = modbus_tcp.TcpServer(port=502)
    for i in range(len(secs[1:])):
        slave_id = int(config.get(secs[1:][i], "slave_id"))
        block_name = config.get(secs[1:][i], "block_name")
        address = int(config.get(secs[1:][i], "address"))
        size = int(config.get(secs[1:][i], "quantity"))
        slave_type = config.get(secs[1:][i], "type")
        loop_interval_time = int(config.get(secs[1:][i], "loop_interval_time"))
        if slave_type == "signed":
            t1 = (Thread(target=great_block_and_run,
                         args=(SERVER, slave_id, block_name, address, size, slave_type, loop_interval_time, (),)))
            threads.append(t1)
        elif slave_type == "float":
            random_start = config.get(secs[1:][i], "random_start")
            random_end = config.get(secs[1:][i], "random_end")
            random_add_start = config.get(secs[1:][i], "random_add_start")
            random_add_end = config.get(secs[1:][i], "random_add_end")
            t1 = (Thread(target=great_block_and_run,
                         args=(SERVER, slave_id, block_name, address, size, slave_type, loop_interval_time,
                               (random_start, random_end, random_add_start, random_add_end),)))
            threads.append(t1)
    for j in threads:
        j.start()
    # for j in threads:
    #     j.join()


def write_to_logFile(text):
    realtime = strftime("%Y-%m-%d %H:%M:%S ")
    with open('modbus.log', "a") as f:
        f.write("{}\t\t\t\t\t{}\n".format(realtime, text))


def stop():
    # print(m1)
    if not m1.is_alive():
        my_mes1("已经终止")
    else:
        m1.terminate()
        write_to_logFile("运行终止")


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()


def showinfo(result):
    # print(result)
    realtime = strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + result  # 系统时间和传入结果
    text2.insert(END, textvar)  # 显示在text框里面


def read_log_file():
    fpath = "modbus.log"
    # with open(fpath, "r") as f:
    #     f.write("")
    fp_r = open(fpath, 'r')
    while True:
        # print(log_signal)
        sleep(0.1)
        line_r = fp_r.readline()
        # print(line_r)
        text2.insert(END, line_r)
        text2.see(END)
        # text2.update()


def log_clear():
    text2.delete(0.0, END)


def exit_():
    if m1.is_alive():
        my_mes1("请先停止运行再退出程序")
    else:
        exit()


if __name__ == '__main__':
    # with open("modbus.log", "w") as f:
    #     f.write("")
    root = Tk()
    root.title("modbus数据模拟")
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    w = 500
    h = 800
    x = (screenWidth - w) / 2
    y = (screenHeight - h) / 2
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)  ## 规定窗口不可缩放
    first_lab = Label(root, text="欢迎使用modbus数据模拟器", font="Helvetic 20 bold")
    first_lab.pack(pady=15)
    button_write = Button(root, text="写入配置", command=write_config, width=8)
    button_config = Button(root, text="获取模板", command=write_template, width=8)
    button_run = Button(root, text="开始运行", command=lambda: multiprocessing_(run), width=8)
    button_stop = Button(root, text="停止运行", command=stop, width=8)
    button_clear = Button(root, text="清空日志", command=log_clear, width=10)
    button_exit = Button(root, text="退出程序", command=exit_, width=10)
    labFrame1 = LabelFrame(root, text="配置数据", height=100, width=470)
    labFrame2 = LabelFrame(root, text="日志", height=100, width=470)
    text1 = Text(labFrame1, height=20)
    text2 = Text(labFrame2, height=27)
    # text2.insert(END,"hello world")
    configtext = """[modbus_tk]
port = 502

[block1]
type = signed
slave_id = 1
block_name = A
address = 0
quantity = 5
loop_interval_time = 10

[block2]
type = signed
slave_id = 5
block_name = B
address = 0
quantity = 3
loop_interval_time = 5

[block3]
type = float
slave_id = 6
block_name = C
address = 0
quantity = 3
loop_interval_time = 3
random_start = 1000
random_end = 1200
random_add_start = 1
random_add_end = 2"""
    # text.insert(END, configtext)
    text1.pack()
    labFrame1.pack(padx=10)
    button_config.place(x=30, y=360)
    button_write.place(x=150, y=360)
    button_run.place(x=270, y=360)
    button_stop.place(x=390, y=360)
    labFrame2.pack(padx=10, pady=50)
    text2.pack()
    button_clear.place(x=80, y=760)
    button_exit.place(x=300, y=760)
    thread_it(read_log_file)

    with open(log_file_name, "w") as f:
        f.write("")

    if path.exists(config_file_name):
        remove(config_file_name)


    # path.join(path.dirname(sys.argv[0]), 'GUI.py')
    root.mainloop()
