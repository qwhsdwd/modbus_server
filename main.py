from threading import Thread
from MyModbus import *
from sys rt

path
import sys

cf = ConfigParser()
cf.read("./config.ini")
secs = cf.sections()


def verify_config():
    global cf, secs
    # ------------------------------------检测配置文件正确性------------------------------------
    try:
        cf.read(sys.path.join(sys.path.dirname(sys.argv[0]), 'config.ini'))
    except DuplicateSectionError:
        exit()

    block_test_name_list = []
    # 所有section中block的列表
    slave_id_test_name_list = []
    # 所有section中slave_id的列表
    for i in range(len(secs[1:])):
        # 遍历section
        if cf.get(secs[1:][i], "type") != "signed" and cf.get(secs[1:][i], "type") != "float":
            # type是float或者signed之外的话报错且退出程序
            print(cf.get(secs[1:][i], "type"))
            print("{}中的type 请输入 signed 或者 float".format(secs[1:][i]))
            exit(1)
        if cf.get(secs[1:][i], "type") == "signed" and cf.options(secs[1:][i]) != ['type', 'slave_id', 'block_name',
                                                                                   'address', 'quantity',
                                                                                   'loop_interval_time']:
            # type是signed配置中key不对的话则退出程序
            print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            exit(1)
        if cf.get(secs[1:][i], "type") == "float" and cf.options(secs[1:][i]) != ['type', 'slave_id', 'block_name',
                                                                                  'address', 'quantity',
                                                                                  'loop_interval_time', "random_start",
                                                                                  "random_end", "random_add_start",
                                                                                  "random_add_end"]:
            # type是float配置中key不对的话则退出程序
            print("{}中section中配置有错误，请检查后运行".format(secs[1:][i]))
            exit(1)
        if int(cf.get(secs[1:][i], "slave_id")) < 1 or int(cf.get(secs[1:][i], "slave_id")) >= 256:
            print("{}中的slave_id取值必须在[1,255]之间".format(secs[1:][i]))
            exit(1)
        block_test_name_list.append(cf.get(secs[1:][i], "block_name"))
        # 添加block_name 到列表
        slave_id_test_name_list.append(cf.get(secs[1:][i], "slave_id"))
    if len(block_test_name_list) != len(set(block_test_name_list)):
        print("block_name中有重复，请检查后运行")
        exit(1)
    if len(slave_id_test_name_list) != len(set(slave_id_test_name_list)):
        print("slave_id中有重复,请检查后运行")
        exit(1)

    # ------------------------------------检测配置文件正确性------------------------------------


if __name__ == "__main__":

    verify_config()
    MyModbus = MyModbus()
    threads = []
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
