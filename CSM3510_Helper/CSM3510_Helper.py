import datetime

from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrinterInfo
from PyQt5.QtWidgets import *
from serial.tools.list_ports import *

import qr_code
from chipsea_tools import *
from main_window_ui import *


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,csm_helper):
        super(MyApp,self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.csm_helper = csm_helper
        self.setupUi(self)
        # function initial
        self.init_component_content()
        # size
        self.__desktop = QApplication.desktop()
        qRect = self.__desktop.screenGeometry()  # 设备屏幕尺寸
        self.resize(qRect.width() / 3, qRect.height() *2/3 )
        self.move(qRect.width() / 3, qRect.height()/30)
        #initiate
        self.btn_reset_result.clicked.connect(self.reset_button_clicked)
        self.btn_csm3510_setting.clicked.connect(self.csm3510_btn_setting_clicked)
        self.btn_cc2640_setting.clicked.connect(self.cc2640_btn_setting_clicked)
        self.btn_printer_setting.clicked.connect(self.printer_btn_setting_clicked)
        self.btn_currenter_setting.clicked.connect(self.currenter_btn_setting_clicked)
        self.checkBox_csm3510.clicked.connect(self.sin_checked_csm3510)
        self.checkBox_cc2640.clicked.connect(self.sin_checked_cc2640)
        self.checkBox_printer.clicked.connect(self.sin_checked_printer)
        self.checkBox_currenter.clicked.connect(self.sin_checked_currenter)
        #设备
        self.btn_csm3510_autodetect.clicked.connect(self.btn_csm3510_autodetect_call)
        self.btn_cc2640_autodetect.clicked.connect(self.btn_cc2640_autodetect_call)
        self.btn_currenter_autodetect.clicked.connect(self.btn_currenter_autodetect_call)
        # self.btn_printer_autodetect.clicked.connect(self.btn_printer_autodetect_call)
        # csm_helper
        self.csm_helper.sin_str.connect(self.sin_str_call)
        self.csm_helper.sin_dis_str.connect(self.sin_dis_str_call)
        self.csm_helper.sin_log_str.connect(self.sin_log_str_call)
        self.csm_helper.sin_result_int.connect(self.sin_result_int_call)
        #else
        self.textBrowser_help.setSource(QUrl("help.html"))
        self.textBrowser_result.setSource(QUrl("waitting.html"))


    def init_component_content(self):
        # port
        list_port = serial.tools.list_ports.comports()
        for name in list_port:
            self.csm3510_comboBox_port.addItem(name[0])
            self.cc2640_comboBox_port.addItem(name[0])
            self.currenter_comboBox_port.addItem(name[0])
            # self.printer_name.addItem(name[0])

        list_baudrate = [9600, 1200,4800,14400,19200,28800,57600,115200]
        for bd in list_baudrate:
            self.csm3510_comboBox_baudrate.addItem(str(bd))
            self.cc2640_comboBox_baudrate.addItem(str(bd))
            self.currenter_comboBox_baudrate.addItem(str(bd))
            # self.printer_name.addItem(str(bd))
        self.cc2640_comboBox_baudrate.setCurrentText(str(list_baudrate[7]))

        list_dataBit = [8,5,6,7]
        for len in list_dataBit:
            self.csm3510_comboBox_databits.addItem(str(len))
            self.cc2640_comboBox_databits.addItem(str(len))
            self.currenter_comboBox_databits.addItem(str(len))

        printerInfo = QPrinterInfo()
        self.set_green_text(self.printer_head_text)
        self.printer_name.setText("当前默认打印机:"+printerInfo.defaultPrinterName())


    def set_green_text(self, comp):
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.darkGreen)
        comp.setPalette(palette)
        self.refresh_app()
        pass


    def set_gray_text(self, comp):
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.lightGray)
        comp.setPalette(palette)
        self.refresh_app()
        pass

    def refresh_app(self):
        qApp.processEvents()


    def sin_checked_printer(self):
        if self.checkBox_printer.isChecked():
            self.csm_helper.printer_is_checked = True
        else:
            self.csm_helper.printer_is_checked = False

    def sin_checked_currenter(self):
        if self.checkBox_currenter.isChecked():
            self.csm_helper.currenter_is_checked = True
        else:
            self.csm_helper.currenter_is_checked = False

    def sin_checked_cc2640(self):
        if self.checkBox_cc2640.isChecked():
            self.csm_helper.cc2640_is_checked = True
        else:
            self.csm_helper.cc2640_is_checked = False

    def sin_checked_csm3510(self):
        print("点击-sin_checked_csm3510")
        if self.checkBox_csm3510.isChecked():
            self.csm_helper.csm3510_is_checked = True
        else:
            self.csm_helper.csm3510_is_checked = False

    def sin_str_call(self, info):
        self.lineEdit_result.setText(info)
    def sin_dis_str_call(self, info):
        self.plainText_display.appendPlainText(info)
    def sin_log_str_call(self,info):
        self.plainTextEdit_log.appendPlainText(info)
    def reset_button_clicked(self):
        self.textBrowser_result.setSource(QUrl("waitting.html"))
        self.plainText_display.clear()
        self.plainText_display.appendPlainText("等待中......")
        self.csm_helper.had_test_flag = False
        print("点击复位")
        pass
    def sin_result_int_call(self, value):
        if value == self.csm_helper.test_PASS:
            self.textBrowser_result.setSource(QUrl("pass.html"))
        elif value == self.csm_helper.test_FAIL:
            self.textBrowser_result.setSource(QUrl("fail.html"))
        elif value == self.csm_helper.test_WAIT:
            self.textBrowser_result.setSource(QUrl("waitting.html"))
            self.plainText_display.clear()
            self.plainText_display.appendPlainText("等待中......")
        self.refresh_app()


    def csm3510_btn_setting_clicked(self):
        self.set_gray_text(self.csm3510_head_text)
        self.csm_helper.csm3510.port = self.csm3510_comboBox_port.currentText()
        self.csm_helper.csm3510.baudrate = self.csm3510_comboBox_baudrate.currentText()
        self.csm_helper.csm3510.databits = self.csm3510_comboBox_databits.currentText()
        QMessageBox.information(self, "提示", "更新成功-->" + self.csm_helper.csm3510.port, QMessageBox.Yes)
        self.set_green_text(self.csm3510_head_text)

    def cc2640_btn_setting_clicked(self):
        self.set_gray_text(self.cc2640_head_text)
        self.csm_helper.cc2640.port = self.cc2640_comboBox_port.currentText()
        self.csm_helper.cc2640.baudrate = self.cc2640_comboBox_baudrate.currentText()
        self.csm_helper.cc2640.databits = self.cc2640_comboBox_databits.currentText()
        QMessageBox.information(self, "提示", "更新成功-->" + self.csm_helper.cc2640.port, QMessageBox.Yes)
        self.set_green_text(self.cc2640_head_text)

    def printer_btn_setting_clicked(self):
        pass
        printerInfo = QPrinterInfo()
        printer = printerInfo.defaultPrinter()
        setup = QPrintDialog()
        # /* 打印预览 */
        setup.show()
        #
        try:
            MyPrinter.print_img_info("mac: hello world")
        except Exception as e:
            print(str(e))
        print("正在打印测试信息.")
        # 更新默认打印机信息
        self.set_green_text(self.printer_head_text)
        printerInfo = QPrinterInfo()
        self.printer_name.setText("当前默认打印机:" + printerInfo.defaultPrinterName())



    def currenter_btn_setting_clicked(self):
        self.set_gray_text(self.currenter_head_text)
        self.csm_helper.currenter.port = self.currenter_comboBox_port.currentText()
        self.csm_helper.currenter.baudrate = self.currenter_comboBox_baudrate.currentText()
        self.csm_helper.currenter.databits = self.currenter_comboBox_databits.currentText()
        QMessageBox.information(self, "提示", "更新成功-->" + self.csm_helper.currenter.port, QMessageBox.Yes)
        self.set_green_text(self.currenter_head_text)

    def btn_printer_autodetect_call(self):
        pass
        try:
            pass
        except Exception as e:
            print(str(e))

    def btn_currenter_autodetect_call(self):

        self.set_gray_text(self.currenter_head_text)
        self.btn_currenter_autodetect.setText("识别中...")
        self.btn_currenter_autodetect.setEnabled(False)
        self.refresh_app()
        try:
            result, port = self.csm_helper.currenter.find_port()
            if result == True:
                self.plainText_display.appendPlainText("找到串口: " + port)
                self.currenter_comboBox_port.clear()
                self.currenter_comboBox_port.addItem(port)
                self.currenter_comboBox_baudrate.clear()
                self.currenter_comboBox_baudrate.addItem("9600")
                self.currenter_comboBox_databits.clear()
                self.currenter_comboBox_databits.addItem("8")
                self.textBrowser_result.setSource(QUrl("waitting.html"))
                self.set_green_text(self.currenter_head_text)
                self.csm_helper.currenter.is_available = True
                QMessageBox.information(self, "提示", "成功检测电流表串口-->"+port, QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提示", "识别失败，请检测连线", QMessageBox.Yes)
                self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
            self.btn_currenter_autodetect.setText("自动识别")
            self.btn_currenter_autodetect.setEnabled(True)
        except Exception as e:
            print(str(e))


    def btn_cc2640_autodetect_call(self):
        self.set_gray_text(self.cc2640_head_text)
        self.btn_cc2640_autodetect.setText("识别中...")
        self.btn_cc2640_autodetect.setEnabled(False)
        self.refresh_app()
        result, port = self.csm_helper.cc2640.find_port()
        if result == True:
            self.plainText_display.appendPlainText("找到串口: " + port)
            self.cc2640_comboBox_port.clear()
            self.cc2640_comboBox_port.addItem(port)
            self.cc2640_comboBox_baudrate.clear()
            self.cc2640_comboBox_baudrate.addItem("9600")
            self.cc2640_comboBox_databits.clear()
            self.cc2640_comboBox_databits.addItem("8")
            self.textBrowser_result.setSource(QUrl("waitting.html"))
            self.set_green_text(self.cc2640_head_text)
            QMessageBox.information(self, "提示", "成功检测CC2640串口-->"+port, QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "识别失败，请检测连线", QMessageBox.Yes)
            self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
        self.btn_cc2640_autodetect.setText("自动识别")
        self.btn_cc2640_autodetect.setEnabled(True)



    def btn_csm3510_autodetect_call(self):
        """CSM3510自动识别攒看函数"""
        self.set_gray_text(self.csm3510_head_text)
        self.btn_csm3510_autodetect.setText("识别中...")
        self.btn_csm3510_autodetect.setEnabled(False)
        self.refresh_app()
        result, port = self.csm_helper.csm3510.find_port()
        if result == True:
            self.plainText_display.appendPlainText("找到串口: " + port)
            self.csm3510_comboBox_port.clear()
            self.csm3510_comboBox_port.addItem(port)
            self.csm3510_comboBox_baudrate.clear()
            self.csm3510_comboBox_baudrate.addItem("9600")
            self.csm3510_comboBox_databits.clear()
            self.csm3510_comboBox_databits.addItem("8")
            self.textBrowser_result.setSource(QUrl("waitting.html"))
            self.set_green_text(self.csm3510_head_text)
            self.csm_helper.csm3510.is_available = True
            QMessageBox.information(self, "提示", "成功检测CSM3510串口-->"+port, QMessageBox.Yes)

        else:
            QMessageBox.information(self, "提示", "识别失败，请检测连线", QMessageBox.Yes)
            self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
        self.btn_csm3510_autodetect.setText("自动识别")
        self.btn_csm3510_autodetect.setEnabled(True)

class MyPrinter:
    @staticmethod
    def print_img_info(str):
        print_Info = QPrinterInfo()
        printer_name = print_Info.defaultPrinterName()
        p = QPrinter()
        for item in print_Info.availablePrinters():
            if printer_name == item.printerName():
                p = QPrinter(item)
                print("匹配到打印机")
        painter = QPainter(p)
        qr_code.GeneateQRCode.gen_qr_code(str)

        image_info =Image.open ("mac.png")
        image_logo = Image.open("logo.jpg")
        x, y = image_info.size
        print("resize_logo:", x, y)
        image_logo = image_logo.resize((x,y),Image.ANTIALIAS)

        pre_image = Image.new("RGBA", (2*x, y))
        pre_image.paste(image_info, (0,0))
        pre_image.paste(image_logo, (x,0))
        pre_image.save("result.png")
        image = QImage()
        image.load("result.png")
        rect = painter.viewport()
        size = image.size()
        size.scale(rect.size(), Qt.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        print(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(image.rect())


        painter.drawImage(0, 0, image)
        painter.end()



class CSM3510_Helper(QThread):
      # const
      test_PASS = 0x01; test_FAIL = 0x02;test_WAIT = 0x03
      # flag
      had_test_flag = False;
      csm3510_is_checked = True; cc2640_is_checked = True; currenter_is_checked = True; printer_is_checked = True;
      #single-slot
      sin_str = pyqtSignal(str)
      sin_log_str = pyqtSignal(str)
      sin_dis_str = pyqtSignal(str)
      sin_serial_lost_str = pyqtSignal(bool)
      sin_result_int = pyqtSignal(int)
      # object
      csm3510 = CSM3510()
      cc2640  = CC2640()
      currenter = CurrentMeasure()
      def  __init__(self):
          super(CSM3510_Helper, self).__init__()

      def run(self):
          pass
          try:
              # 串口工作主流程
              #主循环#
              while True:
                    pass
                    print("测试中")
                    time.sleep(0.1)
                    #同一循环，下面函数只跑其中一个
                    ###############################################
                    self.run_with_only_csm3510()
                    ###############################################
                    self.run_with_csm3510_and_currenter()
                    # ###############################################
                    self.run_with_csm3510_currenter_cc2640()
                    ###############################################
          except Exception as e:
                print(str(e))

      def run_with_csm3510_currenter_cc2640(self):
        #打印机只需要在检测结果出来时进行调用即可
             if self.currenter_is_checked == True and self.cc2640_is_checked == True:
                 pass
                 if self.csm3510.is_available==True and self.currenter.is_available == True:
                     self.check_current()
                     result, cur = self.get_current()
                     if result == True and abs(cur) > 3.0:
                         print("当前电流:" + str(result) + "->" + str(cur))
                         result = self.check_csm3510_state()
                         if result == True:
                             if self.had_test_flag == False:
                                # 1 - 发送复位cc2640指令
                                self.cc2640.send_command(self.cc2640.cmd_reset, timeout = 1)
                                # 2 获取MAC地址和版本号
                                result = self.get_device_info()
                                if result == True:
                                    # 3 发送mac地址给CC2640
                                    result, info = self.cc2640.send_mac_adress(self.csm3510.mac_address, timeout = 1)
                                    self.print_dis("03. 发送MAC地址给测试架:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 4 发送命令获取广播的RSSI
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_adv_rssi, timeout = 1)
                                    self.print_dis("04. 获取广播RSSI:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 5 设置广播通道为adv_37
                                    result = self.csm3510.send_command(self.csm3510.cmd_set_adv_37)
                                    self.print_dis("05. 发送广播通道37:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 6 获取当前广播内容
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_adv_data, timeout = 1)
                                    self.print_dis("06. 接收广播通道37:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 7设置广播通道为adv_38
                                    result = self.csm3510.send_command(self.csm3510.cmd_set_adv_38)
                                    self.print_dis("07. 发送广播通道38:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 8 读取广播通道38的内容
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_adv_data, timeout = 1)
                                    self.print_dis("08. 接收广播通道38:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 9 设置广播通道adv_39
                                    result = self.csm3510.send_command(self.csm3510.cmd_set_adv_39)
                                    self.print_dis("09. 发送广播通道39:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 10 获取广播通道39内容
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_adv_data, timeout = 1)
                                    self.print_dis("10. 发送广播通道39:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 11 设置广播通道到默认
                                    result = self.csm3510.send_command(self.csm3510.cmd_set_adv_default)
                                    self.print_dis("11. 重置广播到默认" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 12 读取此时广播电流
                                    result, cur = self.get_current()
                                    self.print_dis("12. 读取广播电流:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 13 要求cc2640连接上csm3510
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_connect, timeout = 5)
                                    self.print_dis("13. 连接蓝牙:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 14 获取连接RSSI和详细版本号
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_device)
                                    self.print_dis("14. 获取详细版本号和连接RSSI:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 15 发送数据给3510
                                    result = self.csm3510.send_data(self.csm3510.cmd_send_notify_data)
                                    self.print_dis("15. Tx发送数据给CSM3510:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 16 接收透传notify数据
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_notify)
                                    self.print_dis("16. 接收Notify数据:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 17 接收notify数据
                                    result, info = self.cc2640.send_command(self.cc2640.cmd_get_notify)
                                    self.print_dis("17. 发送Notify数据:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 18 接收数据到csm3510
                                    result, info = self.csm3510.read_app_data()
                                    self.print_dis("18. CSM3510接收Notify下传数据:" + str(result)+ "->" + str(info));
                                    result = True  #test
                                if result == True:
                                    # 19 读取当前连接电流
                                    result, cur = self.get_current()
                                    self.print_dis("19. 读取连接电流:" + str(result)+ "->" + str(cur));
                                if result == True:
                                    # 20 要求断开连接
                                    result , info = self.cc2640.send_command(self.cc2640.cmd_disconnect, timeout = 1)
                                    self.print_dis("20. 断开连接:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 21 让csm3510强制进入睡眠
                                    result  = self.csm3510.send_command(self.csm3510.cmd_set_force_sleep)
                                    self.print_dis("21. CSM3510进入睡眠:" + str(result)+ "->" + str(info));
                                if result == True:
                                    # 22 读取当前连接电流
                                    time.sleep(0.2)
                                    result, cur = self.get_current()
                                    self.print_dis("22. 读取睡眠电流:" + str(result)+ "->" + str(cur));
                                if result == True:
                                         pass
                                         # 23 测量完成
                                         self.had_test_flag = True
                                         self.print_result(self.test_PASS)
                                else:
                                    self.print_result(self.test_FAIL)
                                    self.had_test_flag = True
                         else:
                             self.had_test_flag = False
                     else:
                         pass
                     # 连续2次没查到CSM3510状态，则认为是人为拿下模块
                     result = self.check_csm3510_state()
                     if result == False:
                         result = self.check_csm3510_state()
                         if result == False:
                             self.had_test_flag = False
                             self.print_result(self.test_WAIT)
                 else:

                    print("不可用, 连接已失效")

             else:
                 pass

      def run_with_csm3510_and_currenter(self):
            # 只有CSM3510 和 电流表
            if self.currenter_is_checked == True and self.cc2640_is_checked == False:
                if self.csm3510.is_available==True and self.currenter.is_available == True:
                    #
                    self.check_current()
                    result, cur = self.get_current()
                    if result == True and abs(cur) > 3.0:
                        self.poweron_current = cur
                        print("当前电流:" + str(result) + "->" + str(cur))
                        result = self.check_csm3510_state()
                        if result == True:
                            if self.had_test_flag == False:
                                result = self.get_device_info()
                                if result == True:
                                    result, cur = self.get_current()
                                if result == True:
                                    print("发送强制睡眠命令")
                                    result = self.csm3510.send_command(self.csm3510.cmd_set_force_sleep)
                                    time.sleep(0.2)
                                if result == True:
                                    result, cur = self.get_current()
                                if result == True:
                                    self.sleep_current = cur
                                    self.print_dis("03. 睡眠电流:" + str(result) + "->" + str(cur))
                                    self.had_test_flag = True
                                    self.print_result(self.test_PASS)
                                if self.printer_is_checked == True:
                                    info = "MAC:"+self.mac_address+"\nVERSION:"+self.version+"\nPOWERON_CURRENT:"+str(self.poweron_current)+"\nSLEEP_CURRENT:"+str(self.sleep_current)+"\nRESULT: PASS"
                                    print("打印机打印中:"+info)
                                    try:
                                        MyPrinter.print_img_info(info)
                                    except Exception as e:
                                        print(str(e))
                                    print("正在打印测试信息.")
                                    self.print_dis("================")
                                    self.print_dis("4. 请取下模块CSM3510")
                                    self.print_dis("================")
                                    print("测试结束")
                        else:
                            self.had_test_flag = False
                    else:
                        pass
                    # 连续2次没查到CSM3510状态，则认为是人为拿下模块
                    result = self.check_csm3510_state()
                    if result == False :
                        result = self.check_csm3510_state()
                        if result == False:
                            self.had_test_flag = False
                            self.print_result(self.test_WAIT)

      def run_with_only_csm3510(self):
         ################################################
          # 只选择了CSM3510
          if self.currenter_is_checked == False and self.cc2640_is_checked == False and self.printer_is_checked == False:
              result = self.check_csm3510_state()
              if result == True:
                  if self.had_test_flag == False:
                      result = self.get_device_info()
                      if result == True:
                          self.had_test_flag = True
                          self.print_dis("================")
                          self.print_dis("3. 请取下模块CSM3510")
                          self.print_dis("================")
                          self.print_result(self.test_PASS)
                          print("测试结束")

              else:
                  self.had_test_flag = False
                  self.print_result(self.test_WAIT)


      def check_current(self):
          result, cur = self.get_current()
          if result == True:
              if cur > 8.0:
                  self.print_result(self.test_FAIL)
              else:
                  if self.had_test_flag == False:
                      self.print_result(self.test_WAIT)


      def get_current(self):
          if self.currenter_is_checked == True:
              if self.currenter.is_available == True:
                      result, cur = self.currenter.get_current()
                      if result == True:
                          # 成功获取上电电流
                            print('读取到电流： '+ str(cur))
                            return True, cur
              else:
                  print("异常，电流表不可用")
                  return False, "fail"
          else:
              return False,"fail"

      def get_device_info(self):
          result, mac = self.csm3510.get_mac_address()
          self.print_dis("01. 获取mac地址:" + str(result) + "->" + mac);
          self.mac_address = mac
          self.print_log("mac地址:" + str(result) + "->" + mac)
          if result == True:
              print("成功获取mac地址", mac)
              result, version = self.csm3510.get_soft_version()
              self.version = version
              self.print_dis("02. 获取版本号:" + str(result) + "->" + version);
              self.print_log("版本号:" + str(result) + "->" + version)
              if result == True:
                  print("成功获取版本号:", version)
                  return  True
          else:
              self.print_result(self.test_FAIL)
              return  False

      def check_csm3510_state(self):
            if self.csm3510_is_checked == True:
                if self.csm3510.is_available == True:
                    result = self.csm3510.query_work_state()
                    if result == True:
                        self.print_log("找到CSM3510");
                        print("CSM3510在广播状态");
                        print("搜索到CSM3510")
                        return True
                    else:
                        print("未查询到CSM3510状态")
                        # self.print_result(self.test_WAIT)
                        return  False
            else:
                # self.print_result(self.test_WAIT)
                return False


      def print_log(self, info):
          self.sin_log_str.emit(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"=>"+info)

      def print_dis(self, info):
          self.sin_dis_str.emit(info)

      def print_result(self, const):
          self.sin_result_int.emit(const)

      def mainloop_app(self):
          try:
              pass
              app = QtWidgets.QApplication(sys.argv)
              window = MyApp(self)
              window.show()
              pass
          except Exception as e:
              print(str(e))
          finally:
              sys.exit(app.exec_())

if __name__ == "__main__":
    csm_helper = CSM3510_Helper()
    csm_helper.start()
    csm_helper.mainloop_app()




