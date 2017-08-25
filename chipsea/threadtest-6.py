#encode=utf-8


import sys; import time;import  traceback
from serial.threaded import *;


class PrintLines(LineReader):
    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        sys.stdout.write('port opened\n')
        self.write_line('hello world')

    def handle_line(self, data):
        sys.stdout.write('line received: {}\n'.format(repr(data)))

    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')

ser = serial.Serial('COM6', baudrate=9600)
with ReaderThread(ser, PrintLines) as protocol:

    while True:
        protocol.write_line('yes,come on')
        time.sleep(2)
        pass
