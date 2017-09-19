#------------------------- printer.py ----------------------
# 直接打印,不预览
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtPrintSupport import QPrinterInfo, QPrinter

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
    def printing(printer, context):
        printerInfo = QPrinterInfo()
        p = QPrinter()
        for item in printerInfo.availablePrinters():
            if printer == item.printerName():
                p = QPrinter(item)
        doc = QTextDocument()
        doc.setHtml(u'%s' % context)
        doc.setPageSize(QSizeF(p.logicalDpiX() *32/25.4, p.logicalDpiY() *16/25.4))
        print(p.logicalDpiX())
        print(p.logicalDpiY())
        print(p.physicalDpiX())
        print(p.physicalDpiY())

        p.setOutputFormat(QPrinter.NativeFormat)
        doc.print_(p)

    @staticmethod
    def print_imag(self):
       printerInfo = QPrinterInfo()
       p = QPrinter()
       for item in printerInfo.availablePrinters():
           if printer == item.printerName():
               p = QPrinter(item)
       # pImag =

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
    printer_jh.printing(p,html)
    print("printing ...... ")
    sys.exit(app.exec_())
    input()