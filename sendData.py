import serial
import serial.tools.list_ports
import sys,time
# 打印输出当前可用串口
port_list = serial.tools.list_ports.comports()
for port in port_list:
    print(port)
ser = serial.Serial()
name = port_list[1]
name = input()
ser.port = name
ser.open()
while True:
    try:
        time.sleep(0.1)
        resp = ser.write(b'CSM3510\n')
        # if(resp == b'CSM3510\n'):
        #     print('haha')
        print(resp)
    except:
        print('exception')
        ser.close()
ser.close()
input()
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

ser = serial.serial_for_url('loop://', baudrate=115200, timeout=1)
with ReaderThread(ser, PrintLines) as protocol:
    protocol.write_line('hello')
    time.sleep(2)


