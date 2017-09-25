
#encode=utf-8

import  queue
import  _thread
import sys; import time; import traceback; import  datetime
import serial
import serial.tools.list_ports
from  serial.threaded import *
import sqlite3 as lite



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
        print('串口丢失，请检查连线，重启本软件\n')
        print('串口丢失，请检查连线，重启本软件\n')
        print('串口丢失，请检查连线，重启本软件\n')
        print('串口丢失，请检查连线，重启本软件\n')
        print('串口丢失，请检查连线，重启本软件\n')

    def decode_mcu_protocol(self, ThreadName):
        print('decoding...')
        while True:
            # time.sleep(0.1)
            while self.queue_recieved.qsize() >= 32:

                i_head1 = self.queue_recieved.get()
                time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if i_head1 == 0x53:
                    i_head2 = self.queue_recieved.get();
                    if i_head2 == 0x4D:
                        # 丢掉3bytes的ID标识
                        self.queue_recieved.get();self.queue_recieved.get();self.queue_recieved.get();self.queue_recieved.get();
                        # 丢掉4bytes的命令字节
                        self.queue_recieved.get();self.queue_recieved.get();self.queue_recieved.get();
                        command = self.queue_recieved.get();
                        cmd_length = self.queue_recieved.get();
                        if command == 0x10 and cmd_length == 0x06:
                            try:
                                con = lite.connect('./data/chipsea.db')
                                cur = con.cursor();cur.execute('select sqlite_version()');data = cur.fetchone();print("version: %s"  %data)
                                cur.execute("CREATE TABLE IF NOT EXISTS mac_address_table(cur_time TEXT, mac_address TEXT)")
                                mac_address = [0x00,0x00,0x00,0x00,0x00,0x00]
                                mac_address[0] = self.queue_recieved.get();
                                mac_address[1] = self.queue_recieved.get();
                                mac_address[2] = self.queue_recieved.get();
                                mac_address[3] = self.queue_recieved.get();
                                mac_address[4] = self.queue_recieved.get();
                                mac_address[5] = self.queue_recieved.get();
                                address = ' '.join('{:02x}'.format(x) for x in mac_address)
                                address.upper()
                                data = "INSERT INTO mac_address_table(cur_time, mac_address)VALUES('%s', '%s');" %(time_stamp,address)
                                cur.execute(data)
                                # print(data)
                                print(time_stamp,":", address)

                                con.commit()
                                con.close()
                            except Exception as e:
                                raise e
                else:
                   pass


        pass

if __name__ == '__main__':

    while True:
        try:
            pass
            print('正在识别串口....:')
            com_name = None
            found_port = False
            print("搜索到以下串口")
            com_name_list = serial.tools.list_ports.comports()
            for port in com_name_list:
                print(port)
            slave_state = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1E]
            # slave_state = [0x00,0x11]
            for port in com_name_list:
                print("正在测试串口:", port[0])
                try:
                    ser = serial.Serial(port[0], baudrate=115200, timeout=1)
                    ser.flushOutput()
                    ser.flushInput()
                    ser.write(slave_state)
                    recieve = ser.read(32)
                    if recieve:
                        if recieve[0] == 0x53 and recieve[1] == 0x4D and recieve[2] == 0x00 and recieve[3] == 0x00 and recieve[4] == 0x00 and recieve[5] == 0x00:
                            com_name = port[0]
                            found_port = True
                            # 成功获取串口名
                            print("成功检测到串口-CC2640")
                    ser.close()
                except Exception as e:
                    print(str(e))
                finally:
                    if ser:
                        ser.close()
            ser = None
            while True and found_port==True:
                try:
                    ser = serial.Serial(com_name, baudrate=115200)
                    print("已打开串口",com_name)
                    with ReaderThread(ser, BleMonitorProtocol) as protocol:
                        pass
                        while True:
                                # time.sleep(1)
                                pass
                                pass
                except Exception as e:
                    if ser:
                        ser.close()
                    print('异常'+ str(e))
                    print('请重启')
                    print('请重启')
                    print('请重启')
                    print('请重启')
                    print('请重启')

                finally:
                    pass
        except Exception as e:
             print(str(e))
        finally:
            pass


