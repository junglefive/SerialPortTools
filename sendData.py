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


