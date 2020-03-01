#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QGroupBox, QGroupBox, QDialog, QVBoxLayout, QGridLayou
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# https://pythonspot.com/pyqt5-horizontal-layout/
class App(QDialog):
	def __init__(self):
		super().__init__()
		self.title = "Glen's Personal Dictionary"
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		#self.statusBar().showMessage('Message in statusbar.')
		self.createGridLayout()
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.horizontalGroupBox)
		
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())