import serial
import serial.tools.list_ports
import sys,time,datetime
# 打印输出当前可用串口
port_list = serial.tools.list_ports.comports()
for port in port_list:
    print(port)
print('请输入串口（例：COM28）')
name = input()
try:
    ser = serial.Serial()
    ser.port = name
    ser.open()
    send_number = 0
    while True:
        timeStamp = hex(int(time.time()))
        bytes_time = bytes().fromhex(timeStamp[2:10])
        wakeup_cam3510  = [0x10,0x00,0x00]
        unlock_okok_1_5 = [0x10, 0x00, 0x00, 0xC5, 0x14, 0x96, 0xCA, 0x11, 0x0F, 0x00, 0x01, 0x02, 0x39, 0x55, 0xDB, 0xBC, 0x5A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4C, 0x8C]
        locked_query_user_okok_1_5 = [0x10, 0x00,0x00,0xC5,0x15,0x96,0x21,0x59,0xA6,0x6D,0x3B,0x00,0x02,0x39,0x00,0x00,0x00,0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xD5]
        locked_got_user_okok_1_5 = [0x10,  0x00, 0x00, 0xC5, 0x15, 0x96, 0x01, 0x59, 0xA6, 0x6D, 0x3B, 0x00, 0x02, 0x39, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        sleep_csm3510 = [0x10, 0x00,0x00, 0xC5,0x01, 0x80, 0x44]
        # 初始化时间戳
        locked_got_user_okok_1_5[7] = bytes_time[0]
        locked_got_user_okok_1_5[8] = bytes_time[1]
        locked_got_user_okok_1_5[9] = bytes_time[2]
        locked_got_user_okok_1_5[10] = bytes_time[3]
        #求校验码
        checksum = 0x00
        for hexValue in locked_got_user_okok_1_5:
            checksum ^= hexValue
        checksum ^= 0x10
        locked_got_user_okok_1_5[26] = checksum
        #发送数据
        send_number = send_number+1
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')+'---->发送循环次数:', send_number)
        ser.write(wakeup_cam3510)
        time.sleep(0.2)
        print('send wakeup', wakeup_cam3510)
        ser.write(unlock_okok_1_5)
        time.sleep(0.2)
        print('send unlock',unlock_okok_1_5)
        ser.write(locked_query_user_okok_1_5)
        time.sleep(0.2)
        print('send query',locked_query_user_okok_1_5)
        ser.write(locked_got_user_okok_1_5)
        time.sleep(0.2)
        print('send fat data', locked_got_user_okok_1_5)
        ser.write(sleep_csm3510,)
        print('send sleep', sleep_csm3510)
        ser.flushInput()
        resp = ser.read(4)
        print('收到命令',resp)
        time.sleep(60)

except Exception as e:
    print(str(e))
finally:
    ser.close()
    pass




