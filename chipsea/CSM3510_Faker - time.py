
#encode=utf-8

import  queue
import  _thread
import sys; import time; import traceback; import  datetime
import serial
import serial.tools.list_ports
from  serial.threaded import *


class BleMonitorProtocol(Protocol):

    def __init__(self):
        super(BleMonitorProtocol,self).__init__()
        self.queue_recieved = queue.Queue()
        self.work_thread = _thread.start_new_thread(self.decode_mcu_protocol, ('thread_cc2640',))

    def connection_made(self, transport):
        super(BleMonitorProtocol, self).connection_made(transport)
        self.transport = transport
        print('port opened\n')

    def data_received(self, data):
        # print(type(data))
        for byte in data:
            self.queue_recieved.put(byte)

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        # _thread.exit_thread(self.work_thread)
        print('port closed\n')

    def decode_mcu_protocol(self, ThreadName):
        print('decoding...')
        while True:
            # time.sleep(0.1)
            while self.queue_recieved.qsize() >= 1:
                # print(type(self.queue_recieved.get()))
                i_head = self.queue_recieved.get()
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + '-' + hex(i_head))
                # if i_head == 0xC5:
                #     i_length= self.queue_recieved.get()
                #     time.sleep(0.1)
                #     if i_length == 1:
                #         i_command = self.queue_recieved.get()
                #         if i_command == 0x80 or i_command == 0x90:
                #             self.write_ack_to_mcu()
                #             self.queue_recieved.get()
                #         if i_command == 0x81:
                #             self.write_adv_to_mcu()
                #             self.queue_recieved.get()
                #     else:
                #         i_command = self.queue_recieved.get()
                #         while i_length > 0:
                #             i_length = i_length - 1
                #             self.queue_recieved.get()
                #         pass
                #         print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), ':', '收到命令...' + hex(i_command))
                # else:
                #     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + '-' + hex(i_head))
        pass

    def write_ack_to_mcu(self):
        # byte_array = b'\xc5\xff\x80\x44'
        byte_array_ack = b'\xc5\x01\x80\x44'
        # self.transport.write(byte_array)
        time.sleep(0.1)
        self.transport.write(byte_array_ack)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), ':','收到睡眠命令-------------------------------------------SLEEP')
        # print('reply: ' + str(byte_array))
        # print('reply:', end='')
        # for b in byte_array:
        #     print(hex(b)+",", end='')
        # print('')
        print('reply:', end='')
        for b in byte_array_ack:
            print(hex(b) + ",", end='')
        print('')

    def write_adv_to_mcu(self):
        byte_array = b'\xc5\x01\x01\xc5'
        self.transport.write(byte_array)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), ':','收到查询BLE状态命令-----state')
        # print('reply: ' + str(byte_array))
        print('reply:', end='')
        for b in byte_array:
            print(hex(b)+",", end='')
        print('')
if __name__ == '__main__':
    pass
    print('搜索到可用串口:')
    com_name_list = serial.tools.list_ports.comports()
    for port in com_name_list:
        print(port)
    print("请输入串口：")
    com_name = input()
    while True:
        try:
            ser = serial.Serial(com_name, baudrate=9600)
            with ReaderThread(ser, BleMonitorProtocol) as protocol:
                pass
                while True:
                        # time.sleep(1)
                        pass
        except Exception as e:
            print('异常'+ str(e))
            print('请重新输入')
        finally:
            com_name = input()


