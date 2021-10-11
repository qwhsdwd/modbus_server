import struct
import modbus_tk.defines
import modbus_tk.modbus
import modbus_tk.modbus_tcp
import time
import random

# ------------------------------------------------------------------------------
# 主程序
# ------------------------------------------------------------------------------

try:
    server = modbus_tk.modbus_tcp.TcpServer(port=501)
    # 注意，若是在linux里面运行，端口就不能不写了，否则就要用root才能跑，其它用户只能用1024以上的端口
    # 这里的端口和地址都是默认的，地址是本地：
    # 原来的程序：server = modbus_tk.modbus_tcp.TcpServer(port=502, address='0.0.0.0', timeout_in_sec=3)
    server.start()
    slave_1 = server.add_slave(1)
    slave_1.add_block('block1', modbus_tk.defines.HOLDING_REGISTERS, 250, 2)
    # 给slave_1添加一个模块（模块名，只读，地址，长度）
    print("-----------")
    while 1:
        bb = random.random()
        aa = struct.unpack('>HH', struct.pack('>f', bb))
        print
        'bb:', bb
        print
        "aa:", aa
        slave_1.set_values('block1', 0, aa)
        print
        '========='
        time.sleep(3)
    print("-----------")
except Exception as e:
    print
    '============error==========='
finally:
    print
    '=========stop========'
    server.stop()
