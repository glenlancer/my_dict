#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
	QApplication, QMainWindow,
	QGridLayout, QHBoxLayout,
	QAction, qApp, QWidget,
	QLabel, QTextEdit,
	QPushButton, QLineEdit, QListWidget
)
from PyQt5.QtGui import QIcon

# https://pythonspot.com/pyqt5-horizontal-layout/
class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "Glen's Personal Dictionary"
		self.left = 10
		self.top = 10
		self.width = 820
		self.height = 500
		self.setupMenus()
		self.initUI()

	def initUI(self):
		main = QHBoxLayout()

		grid = QGridLayout()
		grid.setSpacing(10)
		self.wordEdit = QLineEdit()
		self.searchBtn = QPushButton('Search')
		self.wordList = QListWidget()
		grid.addWidget(self.wordEdit, 1, 1, 1, 2)
		grid.addWidget(self.searchBtn, 1, 3, 1, 1)
		grid.addWidget(self.wordList, 2, 1, 6, 3)
		gridWidget = QWidget()
		gridWidget.setLayout(grid)

		grid2 = QGridLayout()
		grid2.setSpacing(10)
		self.meaning = QLineEdit()
		self.sound = QLineEdit()
		usageLabel = QLabel('Usage')
		articleLabel = QLabel('Article')
		self.usageEdit = QTextEdit()
		self.articleList = QListWidget()
		grid2.addWidget(self.meaning, 1, 1)
		grid2.addWidget(self.sound, 2, 1)
		grid2.addWidget(usageLabel, 3, 1)
		grid2.addWidget(self.usageEdit, 4, 1, 4, 1)
		grid2.addWidget(articleLabel, 8, 1)
		grid2.addWidget(self.articleList, 9, 1, 5, 1)
		gridWidget2 = QWidget()
		gridWidget2.setLayout(grid2)

		main.addWidget(gridWidget)
		main.addWidget(gridWidget2)
		widget = QWidget()
		widget.setLayout(main)
		self.setCentralWidget(widget)
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)		
		self.statusBar().showMessage('Ready')
		self.show()

	def setupMenus(self):
		menuBar = self.menuBar()
		appMenu = menuBar.addMenu('&App')

		addWordAction = QAction('Add &Word', self)
		addWordAction.setStatusTip('Add new word')
		appMenu.addAction(addWordAction)

		addArticleAction = QAction('Add &Article', self)
		addArticleAction.setStatusTip('Add new article')
		appMenu.addAction(addArticleAction)

		deleteAction = QAction('Delete &Record', self)
		deleteAction.setStatusTip('Delete a record')
		appMenu.addAction(deleteAction)

		matchAction = QAction('&Match Article', self)
		matchAction.setStatusTip('Match articles with words')
		appMenu.addAction(matchAction)

		exitAction = QAction('&Exit', self)
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)		
		appMenu.addAction(exitAction)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())