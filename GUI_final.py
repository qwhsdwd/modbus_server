import multiprocessing
import threading
import time
from tkinter import *
import tkinter.messagebox
from tkinter import messagebox
import configparser
# from main import verify_config
from threading import Thread
from MyModbus import *
from time import strftime
from modbus_tk import modbus_tcp


def multiprocessing_(func):
    global m1
    m1 = multiprocessing.Process(target=func)
    m1.start()
    # m1.join()


def my_mes1(text):
    messagebox.showerror("配置文件有误", text)


def my_mes2():
    ret = messagebox.askretrycancel("读取成功", "读取成功，是否开始运行？")
    if ret:
        multiprocessing_(run)


def verify_config(config_, config_text):
    global secs, cf
    try:
        config_.read_string(config_text)
    except configparser.DuplicateSectionError:
        my_mes1("section重复，请检查")
    cf = config_
    config_.read_string(config_text)
    secs = config_.sections()
    block_test_name_list = []
    # 所有section中block的列表
    slave_id_test_name_list = []
    # 所有section中slave_id的列表
    for i in range(len(secs[1:])):
        # 遍历section
        if config_.get(secs[1:][i], "type") != "signed" and config_.get(secs[1:][i], "type") != "float":
            # type是float或者signed之外的话报错且退出程序
            print(config_.get(secs[1:][i], "type"))
            my_mes1("{}中的type 请输入 signed 或者 float".format(secs[1:][i]))
            print("{}中的type 请输入 signed 或者 float".format(secs[1:][i]))
            # exit(1)
        if config_.get(secs[1:][i], "type") == "signed" and config_.options(secs[1:][i]) != ['type', 'slave_id',
                                                                                             'block_name',
                                                                                             'address',
                                                                                             'quantity',
                                                                                             'loop_interval_time']:
            # type是signed配置中key不对的话则退出程序
            my_mes1("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            # exit(1)
        if config_.get(secs[1:][i], "type") == "float" and config_.options(secs[1:][i]) != ['type', 'slave_id',
                                                                                            'block_name',
                                                                                            'address',
                                                                                            'quantity',
                                                                                            'loop_interval_time',
                                                                                            "random_start",
                                                                                            "random_end",
                                                                                            "random_add_start",
                                                                                            "random_add_end"]:
            # type是float配置中key不对的话则退出程序
            my_mes1("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            # exit(1)
        if int(config_.get(secs[1:][i], "slave_id")) < 1 or int(config_.get(secs[1:][i], "slave_id")) >= 256:
            my_mes1("{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i]))
            print("{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i]))
            # exit(1)
        block_test_name_list.append(config_.get(secs[1:][i], "block_name"))
        # 添加block_name 到列表
        slave_id_test_name_list.append(config_.get(secs[1:][i], "slave_id"))
    if len(block_test_name_list) != len(set(block_test_name_list)):
        my_mes1("block_name中有重复，请检查后运行")
        print("block_name中有重复，请检查后运行")
        # exit(1)
    if len(slave_id_test_name_list) != len(set(slave_id_test_name_list)):
        my_mes1("slave_id中有重复,请检查后运行")
        print("slave_id中有重复,请检查后运行")
        # exit(1)

    # ------------------------------------检测配置文件正确性------------------------------------


def write_config():
    global SERVER
    config_read = text1.get(0.0, END)
    verify_config(config, config_read)
    config.read_string(config_text)
    secs = config.sections()
    SERVER = modbus_tk.modbus_tcp.TcpServer(config.get("modbus_tk", "port"))
    print(config.get("modbus_tk", "port"))
    my_mes2()


def write_template():
    # pass
    # text.delete(0.0, END)
    text1.insert(END, config_text)


def run():
    # SERVER = modbus_tk.modbus_tcp.TcpServer(int(self.port))
    for i in range(len(secs[1:])):
        slave_id = int(cf.get(secs[1:][i], "slave_id"))
        block_name = cf.get(secs[1:][i], "block_name")
        address = int(cf.get(secs[1:][i], "address"))
        size = int(cf.get(secs[1:][i], "quantity"))
        slave_type = cf.get(secs[1:][i], "type")
        loop_interval_time = int(cf.get(secs[1:][i], "loop_interval_time"))
        if slave_type == "signed":
            t1 = (Thread(target=MyModbus.great_block_and_run,
                         args=(slave_id, block_name, address, size, slave_type, loop_interval_time, (),)))
            threads.append(t1)
        elif slave_type == "float":
            random_start = cf.get(secs[1:][i], "random_start")
            random_end = cf.get(secs[1:][i], "random_end")
            random_add_start = cf.get(secs[1:][i], "random_add_start")
            random_add_end = cf.get(secs[1:][i], "random_add_end")
            t1 = (Thread(target=MyModbus.great_block_and_run,
                         args=(slave_id, block_name, address, size, slave_type, loop_interval_time,
                               (random_start, random_end, random_add_start, random_add_end),)))
            threads.append(t1)
    for j in threads:
        j.start()
    for j in threads:
        j.join()


def stop():
    m1.terminate()
    print(threads)


def showinfo(result):
    realtime = strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + result  # 系统时间和传入结果
    text2.insert('end', textvar)  # 显示在text框里面
    text2.insert('insert', '\n')  # 换行


# def read_log_file():
#     fpath = "modbus.log"
#     # with open(fpath, "r") as f:
#     #     f.write("")
#     fp_r = open(fpath, 'r')
#
#     while True:
#         time.sleep(0.1)
#         line_r = fp_r.readline()
#         text2.insert(END, line_r)


def great_block_and_run(SERVER, slave_id, block_name, address, size, slave_type, loop_interval_time,
                        *random_num):
    # write_to_logFile("slave{}启动".format(slave_id))
    showinfo("slave{}启动".format(slave_id))
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
            showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
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
            showinfo("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            print("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            # write_to_logFile("slave{}运行第{}次，间隔时间为{}秒".format(slave_id, t, loop_interval_time))
            sleep(loop_interval_time)


threads = []
m1 = multiprocessing.Process()
cf = configparser.ConfigParser()
config = configparser.ConfigParser()
SERVER = modbus_tk.modbus_tcp.TcpServer()

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
    labFrame1 = LabelFrame(root, text="配置数据", height=100, width=470)
    labFrame2 = LabelFrame(root, text="日志", height=100, width=470)
    text1 = Text(labFrame1, height=20)
    text2 = Text(labFrame2, height=20)
    config_text = """[modbus_tk]
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
    # text.insert(END, config_text)
    text1.pack()
    labFrame1.pack(padx=10)
    button_config.place(x=30, y=360)
    button_write.place(x=150, y=360)
    button_run.place(x=270, y=360)
    button_stop.place(x=390, y=360)
    labFrame2.pack(padx=10, pady=50)
    text2.pack()
    # read_thread = threading.Thread(target=read_log_file)
    # read_thread.daemon = True
    # read_thread.start()
    # # read_thread.join()

    root.mainloop()
