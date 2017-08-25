
#encode=utf-8

import  queue
import  _thread
import sys; import time;import  traceback
from serial.threaded import *;


class BleMonitorProtocol(Protocol):

    def __init__(self):
        super(BleMonitorProtocol,self).__init__()
        self.queue_recieved = queue.Queue()
        self.work_thread = _thread.start_new_thread(self.decode_cc2640_protocol, ('thread_cc2640',))

    def connection_made(self, transport):
        super(BleMonitorProtocol, self).connection_made(transport)
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

    def decode_cc2640_protocol(self, ThreadName):
        print('decoding...')
        while True:
            time.sleep(0.1)
            # while self.queue_recieved.qsize() > 0:
                # print(hex(protocol.queue_recieved.get()))
            print(self.queue_recieved)
        pass

ser = serial.Serial('COM6', baudrate=9600)
with ReaderThread(ser, BleMonitorProtocol) as protocol:
    while True:
        # if protocol.queue_recieved.qsize() > 0:
            pass
            pass

