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
    cmd_set_adv_37 = [0x10,0x00,0x00,0xC5,0x01,0xf7,0x33]
    cmd_set_adv_38 = [0x10,0x00,0x00,0xC5,0x01,0xf8,0x3c]
    cmd_set_adv_39 = [0x10,0x00,0x00,0xC5,0x01,0xf9,0x3D]
    cmd_set_adv_default = [0x10,0x00,0x00,0xC5,0x01,0xf6,0x32]
    cmd_send_notify_data = [0x10,0x00,0x00,0xC5,0x15,0x94,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x00,0x44]
    cmd_set_force_sleep = [0x10,0x00,0x00,0xC5,0x01,0x74,0xB0]
    # csm3510属性信息
    mac_address = []


    def send_command(self, cmd):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            print(cmd)
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
            print(str(e))
            self.is_available = False
            return False

    def send_data(self, cmd):
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            print(cmd)
            ser.write(cmd)
            ser.close()
            return True
        except Exception as e:
            pass
            print(str(e))
            self.is_available = False
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
            self.is_available = False
            print(str(e))
            self.is_available = False
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
                self.mac_address = rec
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
            self.is_available = False
            print(str(e))
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
            print(str(rec))
            if rec:
                print("成功接收到数...",' '.join('{:02x}'.format(x) for x in rec))
                if rec[0] == 0x01 and rec[19] == 0x00:
                    return True, rec
            else:
                return False, rec
        except Exception as e:
            pass
            print(str(e))
            self.is_available = False
            return False,rec

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
            self.is_available = False
            print("串口丢失")
            return False

    def find_port(self):
        pass
        ports = serial.tools.list_ports.comports()
        print("找到可用串口")
        ser = serial.Serial()
        ser.timeout = 0.2
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
                    else:
                        pass
                else:
                    pass

            except Exception as e:
                print(str(e))
                self.is_available = False
        return False, 'None'

"""测试架类"""

class CC2640(object):
    """docstring for ClassName"""
    port = "com1"
    baudrate = 115200
    databits = 8
    cmd_sample      = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x20,0x00]
    cmd_reset       = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_query_state = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_send_mac    = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_get_adv_rssi= [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x11,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_get_adv_data= [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x12,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_connect     = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x13,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_get_version = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_get_device  = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x15,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_get_notify  = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x16,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    cmd_send_data   = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x17,0x14,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x20,0x00]
    cmd_disconnect  = [0x4D,0x53,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x18,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]



    def send_command(self, cmd, timeout = 1):
        return True, "软件调试"
        """发送命令"""
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = timeout
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            ser.write(cmd)
            rec = ser.read(32)
            ser.close()
            if rec:
                print("成功接收到数...",' '.join('{:02x}'.format(x) for x in rec))
                return True, rec
            else:
                return False, "校验失败"
        except Exception as e:
            pass
            print(str(e))
            self.is_available = False
            return False,"出现异常"
    def send_mac_adress(self, mac, timeout):
        return True, "软件调试"
        """发送mac地址"""
        try:
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = timeout
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            ser.write(mac)
            print(mac)
            rec = ser.read(32)
            ser.close()
            if rec:
                print("成功接收到数...",' '.join('{:02x}'.format(x) for x in rec))
                return True, "收到数据"
            else:
                return False, "校验失败"
        except Exception as e:
            pass
            print(str(e))
            self.is_available = False
            return False,"出现异常"

    def find_port(self):
        """自动识别串口"""
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
                ser.write(self.cmd_query_state)
                print(self.cmd_query_state)
                rec = ser.read(32)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0x53 and rec[1] ==0x4D):
                         print("找到测试架关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
                    elif (rec[0]==0x4D and rec[1] ==0x53):
                        print("自发自收状态找到测试架关联串口:", sp_name)
                        self.port = sp_name[0]
                        return True, self.port
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                print(str(e))
                self.is_available = False
                return False,"发生异常"
        return False, 'None'

class CurrentMeasure(object):
    """docstring for ClassName"""
    is_available = False
    port = "com1"
    baudrate = 9600
    databits = 8
    cmd_get_current = [0x88,0xAE,0x00,0x11]
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
                ser.write(self.cmd_get_current)
                print(self.cmd_get_current)
                rec = ser.read(8)
                ser.close()
                print(rec)
                if rec:
                    if(rec[0]==0xFA and rec[1] ==0xFB):
                         print("找到电流表关联串口:", sp_name)
                         self.port = sp_name[0]
                         return True, self.port
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                print(str(e))
                self.is_available = False
                return False,"出现异常"
        return False, '未找到'

    def get_current(self):
        try:
            import struct
            ser = serial.Serial()
            ser.port  = self.port
            ser.baudrate = self.baudrate
            ser.databits = self.databits
            ser.timeout = 1
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            ser.write(self.cmd_get_current)
            rec = ser.read(8)
            ser.close()
            if rec:
                print("成功接收到数...",' '.join('{:02x}'.format(x) for x in rec))
                if rec[0] == 0xFA and rec[1] == 0xFB:
                    cur = rec[3:7]
                    float_cur = struct.unpack('!f',cur)[0]
                    return True, round(float_cur, 4)
            else:
                return False, "校验失败"
        except Exception as e:
            pass
            print(str(e))
            self.is_available = False
            return False,"出现异常"










