#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
	QWidget, QPushButton,
	QHBoxLayout, QVBoxLayout,
	QLabel, QLineEdit, QTextEdit,
	QApplication, QMessageBox
)
from PyQt5.QtGui import QFont

from .db import DbOperator

# https://pythonprogramminglanguage.com/pyqt-line-edit/

class ArticleUi(QWidget):
	def __init__(self, db_operator):
		super().__init__()
		self.db_operator = db_operator
		self.initUI()
		self.initAction()
		self.setFont(QFont('Arial', 11))

	def initAction(self):
		self.cancalButton.clicked.connect(self.cancel)
		self.addButton.clicked.connect(self.add)

	def add(self):
		title = self.titleEdit.text().strip().lower()
		content = self.contentEdit.toPlainText().strip()

		if title == '' or content == '':
			self.infoLabel.setText('The title and content can\'t be empty...')
			return

		print('title', title)
		print('content')
		print(content)

		gotArticleRecord = self.db_operator.select_article(title)
		print(gotArticleRecord)
		if gotArticleRecord is None:
			self.db_operator.insert_article(
				title, content
			)
			self.infoLabel.setText('Article is added...')
		elif gotArticleRecord[2] != content:
			res = QMessageBox.question(self, 'Question', 'About to update exisiting article',
					QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
			if res == QMessageBox.Ok:
				self.db_operator.update_article(
					title, content
				)
				self.infoLabel.setText('Article is updated...')
			else:
				self.infoLabel.setText('Gave up...')
		else:
			self.infoLabel.setText('Article is unchanged...')
		self.db_operator.db_commit()
		self.db_operator.print_messages()

	def cancel(self):
		self.close()

	def initUI(self):
		self.infoLabel = QLabel('Status: empty')
		self.addButton = QPushButton('Add Article')
		self.cancalButton = QPushButton('Cancel')

		hbox = QHBoxLayout()
		hbox.addWidget(self.addButton)
		hbox.addWidget(self.cancalButton)
		vbox_i = QVBoxLayout()
		titleLabel = QLabel('Title')
		contentLabel = QLabel('Content')
		self.titleEdit = QLineEdit(self)
		self.titleEdit.setPlaceholderText('The title of the article')
		self.contentEdit = QTextEdit(self)
		self.contentEdit.setPlaceholderText('Put the content of the artile here')
		vbox_i.addWidget(titleLabel)
		vbox_i.addWidget(self.titleEdit)
		vbox_i.addWidget(contentLabel)
		vbox_i.addWidget(self.contentEdit)
		vbox_i.addWidget(self.infoLabel)

		vbox = QVBoxLayout()
		vbox.addLayout(vbox_i)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.setGeometry(300, 300, 500, 600)
		self.setWindowTitle('Article Management')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	ex = ArticleUi(db_operator)
	sys.exit(app.exec_())