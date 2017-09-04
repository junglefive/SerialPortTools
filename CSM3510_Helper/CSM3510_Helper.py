import sys
from main_window_ui import *
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # self.resetButton.clicked.connect(self.reset_button_clicked)


    def reset_button_clicked(self):
        pass
        # self.plainTextEdit.setPlainText('修改成功')

def initiate_app():
    try:
        pass
        app = QtWidgets.QApplication(sys.argv)
        window = MyApp()
        window.show()
        log = open("./log.md", "w+")
    except Exception as e:
        log.write(str(e))
        log.close()
        print(str(e))
    finally:
        sys.exit(app.exec_())

if __name__ == "__main__":
    initiate_app()

