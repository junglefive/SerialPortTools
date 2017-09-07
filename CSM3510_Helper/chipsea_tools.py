import  serial
import  serial.tools.list_ports
import  time

class CSM3510(object):
    """docstring for ClassName"""
    is_available = False
    port = "com1"
    baudrate = 9600
    databits = 8
    cmd_wakeup = [0x10,0x00,0x00,0x00]
    cmd_query_state = [0x10,0x00,0x00,0xC5,0x01,0x81,0x45]
    cmd_get_mac_address =[0x10,0x00,0x00,0xC5,0x01,0x79,0xBD]
    cmd_get_soft_version = [0x10,0x00,0x00,0xC5,0x01,0x78,0xBC]
    cmd_set_adv_37 =[0x10,0x00,0x00,0xC5,0x01,0xf7,0x33]
    cmd_set_adv_38 =[0x10,0x00,0x00,0xC5,0x01,0xf8,0x3c]
    cmd_set_adv_39 =[0x10,0x00,0x00,0xC5,0x01,0xf9,0x3D]
    cmd_set_adv_default = [0x10,0x00,0x00,0xC5,0x01,0xf6,0x32]
    cmd_send_notify_data = [0x10,0x00,0x00,0xC5,0x15,0x94,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x00,0x44]
    cmd_set_force_sleep = [0x10,0x00,0x00,0xC5,0x01,0x74,0xB0]

    def setting_command(self, cmd):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            ser.write(cmd)
            rec = ser.read(4)
            ser.close()
            if rec:
                print("成功接收到数...", ' '.join('{:02x}'.format(x) for x in rec))
                print("命令执行成功")
                if rec[0]==0xc5 and rec[1]==0x01 and rec[2]==0x80 and rec[3]==0x44:
                    return True
            else:
                return False
        except Exception as e:
            pass
            return False

    def get_soft_version(self):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            print("发送数据", ' '.join('{:02x}'.format(x) for x in self.cmd_get_soft_version))
            ser.write(self.cmd_get_soft_version)
            rec = ser.read(4)
            ser.close()
            if rec:
                print("成功接收到数...", ' '.join('{:02x}'.format(x) for x in rec))
                if rec[0] == 0xc5 and rec[1]==0x01 and rec[2] == 0x23 :
                    return True, "CS2.3"
                else:
                    return False, "Erro"
            else:
                return False, "None"
        except Exception as e:
            pass
            return False, "None"

    def get_mac_address(self):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            print("发送数据", ' '.join('{:02x}'.format(x) for x in self.cmd_get_mac_address))
            ser.write(self.cmd_get_mac_address)
            rec = ser.read(9)
            ser.close()
            if rec:
                print("成功接收到数...", ' '.join('{:02x}'.format(x) for x in rec))
                mac = rec[2:8]
                if mac[0] == 0xc8 and mac[1] == 0xb2:
                    address = ' '.join('{:02x}'.format(x) for x in mac)
                    return True, address.upper()

                else:
                    address = ' '.join('{:02x}'.format(x) for x in mac)
                    return  False, address.upper()
            else:
                return False, "None"
        except Exception as e:
            pass
            return False, "None"

    def read_app_data(self):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            rec = ser.read(20)
            ser.close()
            if rec:
                print("成功接收到数...",' '.join('{:02x}'.format(x) for x in rec))
                if rec[0] == 0x01 and rec[19] == 0x00:
                    return True
        except Exception as e:
            pass
            return False

    def query_work_state(self):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 0.1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            print("发送数据", ' '.join('{:02x}'.format(x) for x in self.cmd_query_state))
            ser.write(self.cmd_query_state)
            rec = ser.read(4)
            ser.close()
            if rec:
                print("成功接收到数...", ' '.join('{:02x}'.format(x) for x in rec))
                if(rec[0]==0xc5 and rec[1]==0x01 and rec[2]==0x01 and rec[3]==0xc5):
                    return True
        except Exception as e:
            print("串口丢失")
            return False

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
    baudrate = 9600
    databits = 8
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
    baudrate = 9600
    databits = 8
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
    baudrate = 9600
    databits = 8
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