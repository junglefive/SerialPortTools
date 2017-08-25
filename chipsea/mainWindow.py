import sys
from PyQt5 import QtWidgets, uic

qtCreatorFile = "main_window.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # self.resetButton.clicked.connect(self.reset_button_clicked)


    def reset_button_clicked(self):
        pass
        # self.plainTextEdit.setPlainText('修改成功')

if __name__ == "__main__":
    try:
        pass
        app = QtWidgets.QApplication(sys.argv)
        window = MyApp()
        window.show()
    except Exception as e:
        print(str(e))
    finally:
        sys.exit(app.exec_())
        input()
