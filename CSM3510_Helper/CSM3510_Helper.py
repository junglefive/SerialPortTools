import sys,time
from main_window_ui import *
from PyQt5.QtCore import *

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,csm_helper):
        super(MyApp,self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.csm_helper = csm_helper
        self.setupUi(self)
        # self.resetButton.clicked.connect(self.reset_button_clicked)
        self.pushButtonReset.clicked.connect(self.reset_button_clicked)
        self.csm_helper.sinstr.connect(self.sin_str_call)

    def sin_str_call(self, info):
        self.set_line_result(info)
    def reset_button_clicked(self):
        pass
        self.set_line_result("FAIL")
        # self.plainTextEdit.setPlainText('修改成功')
    def set_line_result(self, str_result):
        self.lineEdit_result.setText(str_result)



class CSM3510_Helper(QThread):
      sinstr = pyqtSignal(str)
      def  __init__(self):
          super(CSM3510_Helper, self).__init__()
      def run(self):
          while True:
              time.sleep(2)
              self.sinstr.emit("FAIL")
              time.sleep(2)
              self.sinstr.emit("PASS")

      def initiate_app(self):
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
    csm_helper.initiate_app()




