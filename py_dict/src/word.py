import sys
from PyQt5.QtWidgets import (
	QWidget, QPushButton,
	QHBoxLayout, QVBoxLayout,
	QLabel, QLineEdit, QTextEdit,
	QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from db import DbOperator
from scraper import Scraper

# https://pythonprogramminglanguage.com/pyqt-line-edit/

class WordUi(QWidget):
	def __init__(self, db_operator):
		super().__init__()
		self.db_operator = db_operator
		self.scraper = Scraper()
		self.initUI()
		self.initAction()
		self.setFont(QFont('monospace', 10))

	def initAction(self):
		self.cancalButton.clicked.connect(self.cancel)
		self.addButton.clicked.connect(self.add)
		self.clearButton.clicked.connect(self.clear)
		self.onlineButton.clicked.connect(self.online)

	def online(self):
		word = self.wordEdit.text().strip()
		if word == '':
			self.infoLabel.setText('Word field empty...')
			return
		self.infoLabel.setText('Searching online...')
		online_info = self.scraper.get_info_from_php(word)
		if online_info['mean']:
			self.meanEdit.setText(online_info['mean'])
		if online_info['pron']:
			self.pronEdit.setText(online_info['pron'])
		if online_info['exchange']:
			self.exchangeEdit.setText(online_info['exchange'])
		if online_info['usage']:
			self.usageEdit.setPlainText(online_info['usage'])
		self.infoLabel.setText('Searching done...')

	def clear(self):
		self.wordEdit.setText('')
		self.pronEdit.setText('')
		self.meanEdit.setText('')
		self.exchangeEdit.setText('')
		self.usageEdit.setPlainText('')
		self.infoLabel.setText('Cleared...')

	def add(self):
		# word are stored in lower case.
		word = self.wordEdit.text().strip().lower()
		meaning = self.meanEdit.text().strip()
		pronunciation = self.pronEdit.text().strip()
		exchange = self.exchangeEdit.text().strip()
		usage = self.usageEdit.toPlainText().strip()

		if not word:
			self.infoLabel.setText('Word field empty...')
			return

		print('word', word)
		print('meaning', meaning)
		print('Pronunciation', pronunciation)
		print('exchange', exchange)
		print('Usage', usage)

		gotWordRecord = self.db_operator.select_word(word)
		if gotWordRecord is None:
			self.db_operator.insert_word(
				word, meaning, pronunciation, exchange
			)
			self.infoLabel.setText('New word added...')
		elif meaning != '' and pronunciation != '' and \
			 (gotWordRecord[2] != meaning or gotWordRecord[3] != pronunciation \
			 or gotWordRecord[4] != exchange):
			res = QMessageBox.question(self, 'Question', 'About to overwrite exisiting record',
        		QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
			if res == QMessageBox.Ok:
				self.db_operator.update_word(
					word, meaning, pronunciation, exchange
				)
				self.infoLabel.setText('Existing word updated...')
			else:
				self.infoLabel.setText('Gave up...')
		else:
			self.infoLabel.setText('Record not updated, info empty or the same...')
		if usage:
			self.db_operator.insert_usage(word, usage)
		self.db_operator.db_commit()
		self.db_operator.print_messages()

	def cancel(self):
		self.close()

	def initUI(self):
		self.infoLabel = QLabel('Status: empty')
		self.onlineButton = QPushButton('Search Online')
		self.addButton = QPushButton('Add Record')
		self.clearButton = QPushButton('Clear')
		self.cancalButton = QPushButton('Cancel')

		hbox = QHBoxLayout()
		hbox.addWidget(self.infoLabel, 0, Qt.AlignLeft)
		hbox.addWidget(self.onlineButton)
		hbox.addWidget(self.addButton)
		hbox.addWidget(self.clearButton)
		hbox.addWidget(self.cancalButton)

		vbox_i = QVBoxLayout()
		wordLabel = QLabel('New Word')
		meanLabel = QLabel('Meaning')
		pronLabel = QLabel('Pronunciation')
		exchangeLabel = QLabel('Exchange')
		usageLabel = QLabel('Usage')
		self.wordEdit = QLineEdit(self)
		self.wordEdit.setPlaceholderText('The word')
		self.meanEdit = QLineEdit(self)
		self.meanEdit.setPlaceholderText('Word\'s meaning')
		self.pronEdit = QLineEdit(self)
		self.pronEdit.setPlaceholderText('Word\'s pronunciation')
		self.exchangeEdit = QLineEdit(self)
		self.exchangeEdit.setPlaceholderText('Word\'s different forms.')
		self.usageEdit = QTextEdit(self)
		self.usageEdit.setPlaceholderText('Word\'s usage examples...')
		vbox_i.addWidget(wordLabel)
		vbox_i.addWidget(self.wordEdit)
		vbox_i.addWidget(meanLabel)
		vbox_i.addWidget(self.meanEdit)
		vbox_i.addWidget(pronLabel)
		vbox_i.addWidget(self.pronEdit)
		vbox_i.addWidget(exchangeLabel)
		vbox_i.addWidget(self.exchangeEdit)
		vbox_i.addWidget(usageLabel)
		vbox_i.addWidget(self.usageEdit)	

		vbox = QVBoxLayout()
		vbox.addLayout(vbox_i)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.setGeometry(300, 300, 700, 600)
		self.setWindowTitle('Add Record')
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	ex = WordUi(db_operator)
	sys.exit(app.exec_())