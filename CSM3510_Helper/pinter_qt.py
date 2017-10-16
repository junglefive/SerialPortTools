#------------------------- printer.py ----------------------
# 直接打印,不预览
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import  qrcode
from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter

def gen_qr_code(str):
    qr = qrcode.QRCode(
        version= 1,
        error_correction= qrcode.constants.ERROR_CORRECT_L,
        box_size= 2,
        border = 3,
    )
    qr.add_data(str)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("mac.png")
    return img

class Printer:

    #打印机列表
    @staticmethod
    def printerList():
        printer = []
        printerInfo = QPrinterInfo()
        print('availablePrinterNames', printerInfo.availablePrinterNames() )
        print('defaultPrinterName', printerInfo.defaultPrinterName())

        for item in printerInfo.availablePrinters():
           printer.append(item.printerName())
        return printer

    @staticmethod
    def print_img(printer_name):
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer_name == item.printerName():
                p = QPrinter(item)
        painter = QPainter(p)
        gen_qr_code("DevName:CSM3510\nmac:C8B21E1E1E1E\nmac:C8B21E1E1E1E\nmac:C8B21E1E1E1E\nversion:CS2.3\nSleep:5uA\nresult:PASS\n")
        image = QImage()
        image.load("ide.ico")
        rect = painter.viewport()
        size = image.size()
        size.scale(rect.size(),Qt.KeepAspectRatio)
        painter.setViewport(rect.x(),rect.y(),size.width(),size.height())
        painter.setWindow(image.rect())
        painter.drawImage(10,0,image)
        painter.end()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    printerInfo = QPrinterInfo()
    printer_jh = Printer()
    printer_jh.printerList()
    p = printerInfo.defaultPrinterName()
    file = open("print.html", 'r')
    html = file.read()
    file.close()
    printer_jh.print_img(p)
    print("print successful")
    sys.exit(app.exec_())
    print("end")
    input()