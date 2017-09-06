import sys,time
from main_window_ui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from serial import *
from chipsea_tools import *


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,csm_helper):
        super(MyApp,self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.csm_helper = csm_helper
        self.setupUi(self)
        #initiate
        self.btn_reset_result.clicked.connect(self.reset_button_clicked)
        self.btn_csm3510_setting.clicked.connect(self.csm3510_btn_setting_clicked)
        self.btn_cc2640_setting.clicked.connect(self.cc2640_btn_setting_clicked)
        self.btn_printer_setting.clicked.connect(self.printer_btn_setting_clicked)
        self.btn_currenter_setting.clicked.connect(self.currenter_btn_setting_clicked)
        #设备
        self.btn_csm3510_autodetect.clicked.connect(self.btn_csm3510_autodetect_call)
        self.btn_cc2640_autodetect.clicked.connect(self.btn_cc2640_autodetect_call)
        self.btn_currenter_autodetect.clicked.connect(self.btn_currenter_autodetect_call)
        self.btn_printer_autodetect.clicked.connect(self.btn_printer_autodetect_call)
        # csm_helper
        self.csm_helper.sin_str.connect(self.sin_str_call)
        self.csm_helper.sin_dis_str.connect(self.sin_dis_str_call)
        self.csm_helper.sin_log_str.connect(self.sin_log_str_call)
    def refresh_app(self):
        qApp.processEvents()
    def sin_str_call(self, info):
        self.lineEdit_result.setText(info)
    def sin_dis_str_call(self, info):
        self.plainText_display.appendPlainText(info)
    def sin_log_str_call(self,info):
        self.textBrowser_log.insertHtml(info)
    def reset_button_clicked(self):
        pass

    def csm3510_btn_setting_clicked(self):
        pass
        self.csm_helper.csm3510.port = self.csm3510_comboBox_port.currentText()
        self.csm3510_head_text.setAutoFillBackground(True)
        QMessageBox.information(self, "提示", "更新成功-->" + self.csm_helper.csm3510.port, QMessageBox.Yes)
        palette = QPalette();palette.setColor(QPalette.Text, Qt.green)
        self.csm3510_head_text.setPalette(palette)

    def cc2640_btn_setting_clicked(self):
        pass

    def printer_btn_setting_clicked(self):
        pass

    def currenter_btn_setting_clicked(self):
        pass

    def btn_printer_autodetect_call(self):
        pass
        self.btn_printer_autodetect.setText("识别中...")
        self.btn_printer_autodetect.setEnabled(False)
        self.refresh_app()
        try:
            result, port = self.csm_helper.printer.find_port()
            if result == True:
                self.plainText_display.appendPlainText("找到串口: " + port)
                self.printer_comboBox_port.clear()
                self.printer_comboBox_port.addItem(port)
                self.printer_comboBox_baudrate.clear()
                self.printer_comboBox_baudrate.addItem("9600")
                self.printer_comboBox_databits.clear()
                self.printer_comboBox_databits.addItem("8")
                self.textBrowser_reuslt.setSource(QUrl("waitting.html"))
                QMessageBox.information(self, "提示", "成功检测CC2640串口-->"+port, QMessageBox.Yes)
            else:
                self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
            self.btn_printer_autodetect.setText("自动识别")
            self.btn_printer_autodetect.setEnabled(True)
        except Exception as e:
            print(str(e))

    def btn_currenter_autodetect_call(self):
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
                self.textBrowser_reuslt.setSource(QUrl("waitting.html"))
                QMessageBox.information(self, "提示", "成功检测CC2640串口-->"+port, QMessageBox.Yes)
            else:
                self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
            self.btn_currenter_autodetect.setText("自动识别")
            self.btn_currenter_autodetect.setEnabled(True)
        except Exception as e:
            print(str(e))

    def btn_cc2640_autodetect_call(self):
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
            self.textBrowser_reuslt.setSource(QUrl("waitting.html"))
            QMessageBox.information(self, "提示", "成功检测CC2640串口-->"+port, QMessageBox.Yes)
        else:
            self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
        self.btn_cc2640_autodetect.setText("自动识别")
        self.btn_cc2640_autodetect.setEnabled(True)



    def btn_csm3510_autodetect_call(self):
        """CSM3510自动识别攒看函数"""
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
            self.textBrowser_reuslt.setSource(QUrl("waitting.html"))
            QMessageBox.information(self, "提示", "成功检测CSM3510串口-->"+port, QMessageBox.Yes)
        else:
            self.plainText_display.appendPlainText("识别失败，请检查连线: " + port)
        self.btn_csm3510_autodetect.setText("自动识别")
        self.btn_csm3510_autodetect.setEnabled(True)


class CSM3510_Helper(QThread):
      sin_str = pyqtSignal(str)
      sin_dis_str = pyqtSignal(str)
      sin_log_str = pyqtSignal(str)
      csm3510 = CSM3510()
      cc2640  = CC2640()
      printer = QrPrinter()
      currenter = CurrentMeasure()
      def  __init__(self):
          super(CSM3510_Helper, self).__init__()
      def run(self):
          pass
          try:
              # 串口工作主流程
              while True:
                  pass
                  time.sleep(2)
                  print(self.csm3510.port)
              # name = self.csm3510.find_port()
              # self.sin_str.emit(name)
              # self.sin_dis_str.emit("找到CSM3510关联串口"+name)
              # self.sin_log_str.emit("<h5>找到csm3510串口</h5>")
          except Exception as e:
              print(str(e))

        # while True:
        #     pass
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




