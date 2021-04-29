# -*- coding: utf-8 -*-#
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_Giulia1 import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from TopStock import StockTable



class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)






if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # win.showMaximized()
    app.exec_()