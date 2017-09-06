import  serial
import  serial.tools.list_ports
import  time

class CSM3510(object):
    """docstring for ClassName"""
    port = "com1"
    cmd_wakeup = [0x10,0x00,0x00,0x00]
    cmd_query_state = [0x10,0x00,0x00,0xC5,0x01,0x81,0x45]
    def find_port(self):
        pass
        ports = serial.tools.list_ports.comports()
        print("找到可用串口")
        ser = serial.Serial()
        ser.timeout = 1
        for sp_name in ports:
            try:
                ser.port = sp_name[0]
                print("正在测试...",sp_name[0])
                ser.open()
                ser.flushInput()
                ser.flushOutput()
                ser.write(self.cmd_wakeup)
                time.sleep(0.2)
                ser.write(self.cmd_query_state)
                rec = ser.read(4)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0xc5 and rec[1] ==0x01 and rec[2] == 0x01 and rec[3] == 0xC5):
                         print("找到3510关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
            except Exception as e:
                print(str(e))
        return False, 'None'


class CC2640(object):
    """docstring for ClassName"""
    port = "com1"
    cmd_wakeup = [0x10,0x00,0x00,0x00]
    cmd_query_state = [0x10,0x00,0x00,0xC5,0x01,0x81,0x45]
    def find_port(self):
        pass
        ports = serial.tools.list_ports.comports()
        print("找到可用串口")
        ser = serial.Serial()
        ser.timeout = 1
        for sp_name in ports:
            try:
                ser.port = sp_name[0]
                print("正在测试...",sp_name[0])
                ser.open()
                ser.flushInput()
                ser.flushOutput()
                ser.write(self.cmd_wakeup)
                time.sleep(0.2)
                ser.write(self.cmd_query_state)
                rec = ser.read(4)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0xc5 and rec[1] ==0x01 and rec[2] == 0x01 and rec[3] == 0xC5):
                         print("找到测试架关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
            except Exception as e:
                print(str(e))
        return False, 'None'

class QrPrinter(object):
    """docstring for ClassName"""
    port = "com1"
    cmd_wakeup = [0x10,0x00,0x00,0x00]
    cmd_query_state = [0x10,0x00,0x00,0xC5,0x01,0x81,0x45]
    def find_port(self):
        pass
        ports = serial.tools.list_ports.comports()
        print("找到可用串口")
        ser = serial.Serial()
        ser.timeout = 1
        for sp_name in ports:
            try:
                ser.port = sp_name[0]
                print("正在测试...",sp_name[0])
                ser.open()
                ser.flushInput()
                ser.flushOutput()
                ser.write(self.cmd_wakeup)
                time.sleep(0.2)
                ser.write(self.cmd_query_state)
                rec = ser.read(4)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0xc5 and rec[1] ==0x01 and rec[2] == 0x01 and rec[3] == 0xC5):
                         print("找到打印机关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
            except Exception as e:
                print(str(e))
        return False, 'None'

class CurrentMeasure(object):
    """docstring for ClassName"""
    port = "com1"
    cmd_wakeup = [0x10,0x00,0x00,0x00]
    cmd_query_state = [0x10,0x00,0x00,0xC5,0x01,0x81,0x45]
    def find_port(self):
        pass
        ports = serial.tools.list_ports.comports()
        print("找到可用串口")
        ser = serial.Serial()
        ser.timeout = 1
        for sp_name in ports:
            try:
                ser.port = sp_name[0]
                print("正在测试...",sp_name[0])
                ser.open()
                ser.flushInput()
                ser.flushOutput()
                ser.write(self.cmd_wakeup)
                time.sleep(0.2)
                ser.write(self.cmd_query_state)
                rec = ser.read(4)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0xc5 and rec[1] ==0x01 and rec[2] == 0x01 and rec[3] == 0xC5):
                         print("找到电流表关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
            except Exception as e:
                print(str(e))
        return False, 'None'