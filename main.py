# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from JUN21_v3 import *

if __name__ == '__main__':
   """
   main function
   """
   app = QApplication(sys.argv)
   mainWindow = QMainWindow()
   ui = Ui_Dialog()
   ui.setupUi(mainWindow)
   mainWindow.show()
   sys.exit(app.exec_())