#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
	QWidget, QPushButton,
	QHBoxLayout, QVBoxLayout,
	QLabel, QApplication
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont

from db import DbOperator

class ShowerUi(QWidget):
	def __init__(self, type=None, content=None, db_operator=None):
		super().__init__()
		self.type = type
		self.content = content
		self.db_operator = db_operator
		self.initUI()
		self.initAction()
		self.setFont(QFont('Arial', 11))

	def initUI(self):
		self.infoLabel = QLabel('Status: empty')
		self.deleteButton = QPushButton('Delete Record')

		hbox = QHBoxLayout()
		hbox.addWidget(self.infoLabel)
		hbox.addWidget(self.deleteButton)

		vbox_i = QVBoxLayout()
		self.webView = QWebEngineView()
		vbox_i.addWidget(self.webView)

		vbox = QVBoxLayout()
		vbox.addLayout(vbox_i)
		if self.db_operator:
			vbox.addLayout(hbox)

		self.setLayout(vbox)
		self.setGeometry(300, 300, 400, 400)
		if self.type == 'show_word':
			self.setWindowTitle('Word\'s details')
		else:
			title = self.content['title']
			self.setWindowTitle(f'{self.content["title"]}')
		self.initWebView()

	def initWebView(self):
		if self.type == 'show_word':
			self.webView.setHtml(f'''
        <strong>{self.content["word"]}</strong>
        <p>
        	<span>
        	Meaning: {self.content["meaning"]}
        	</span><br>
        	<span>
        	Pronunciation: {self.content["sound"]}
        	</span><br>
        	<span>
        	Forms: {self.content["exchange"]}
        	</span>
        </p>
        <p>
        	<span>Usage:</span><br>
        	{self.content["usage"]}
        </p>
			''')
		else:
			html = f'<h5>{self.content["title"]}</h5>'
			paragraphs = self.content['content'].split('\n\n')
			print(paragraphs)
			for paragraph in paragraphs:
				html += f'<p>{paragraph}</p>'
			self.webView.setHtml(html)

	def initAction(self):
		if self.db_operator:
			self.deleteButton.clicked.connect(self.deleteRecord)

	def deleteRecord(self):
		pass

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	content1 = {
		'type': 'show_word',
		'word': 'test',
		'meaning': 'test is test',
		'sound': '[test]',
		'exchange': 'testing, etc',
		'usage': 'This is a test.'
	}
	content2 = {
		'type': 'show_article',
		'title': 'What is my name',
		'content': '''
This is 1st paragraph.

This is 2nd paragraph.

This is a thrid.
		'''
	}
	ex = ShowerUi(content2['type'], content2)
	ex.show()
	sys.exit(app.exec_())