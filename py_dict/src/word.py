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
from .scraper import Scraper
from .function import *

# https://pythonprogramminglanguage.com/pyqt-line-edit/

class WordUi(QWidget):
	def __init__(self, db_operator):
		super().__init__()
		self.db_operator = db_operator
		self.scraper = Scraper()
		self.initUI()
		self.initAction()
		self.setFont(QFont('Noto San', 9))

	def initAction(self):
		self.cancalButton.clicked.connect(self.cancel)
		self.addButton.clicked.connect(self.add)
		self.clearButton.clicked.connect(self.clear)
		self.onlineButton.clicked.connect(self.online)

	def getWord(self):
		return self.wordEdit.text().strip().lower()

	def validateWord(self, word):
		if word == '':
			self.infoLabel.setText('Need to type in a word.')
			return False
		if not is_a_word(word):
			self.infoLable.setText(f'The word ({word}) is not valid.')
			return False
		return True

	def online(self):
		word = self.getWord()
		if not self.validateWord(word):
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
		word = self.getWord()
		meaning = self.meanEdit.text().strip()
		pronunciation = self.pronEdit.text().strip()
		exchange = self.exchangeEdit.text().strip()
		usage = self.usageEdit.toPlainText().strip()

		if not self.validateWord(word):
			return

		if DEBUG_FLAG:
			print('word', word)
			print('meaning', meaning)
			print('Pronunciation', pronunciation)
			print('exchange', exchange)
			print('Usage', usage)

		res = self.process_word(word, meaning, pronunciation, exchange)
		if not res:
			self.infoLabel.setText('Word doesn\'t exist, gave up insertion of usage.')
			return
		if usage:
			usage = escape_double_quotes(usage)
			self.db_operator.insert_usage(word, usage)
		self.db_operator.db_commit()
		self.db_operator.print_messages()

	def process_word(self, word, meaning, pronunciation, exchange):
		record = self.db_operator.select_word(word)
		esed_meaning = escape_double_quotes(meaning)
		esed_pronunciation = escape_double_quotes(pronunciation)
		esed_exchange = escape_double_quotes(exchange)
		if record is None:
			return self.process_insert_word(
				word, esed_meaning, esed_pronunciation, esed_exchange
			)
		elif self.process_update_word_check(record, meaning, pronunciation, exchange):
			self.process_update_word(
				word, esed_meaning, esed_pronunciation, esed_exchange
			)
		else:
			self.infoLabel.setText('Word not updated, info not enough or the same.')		
		return True

	def process_insert_word(self, word, meaning, pronunciation, exchange):
		res = self.db_operator.insert_word(
			word, meaning, pronunciation, exchange
		)
		if res:
			self.infoLabel.setText('New word added.')
			return True
		else:
			self.infoLabel.setText(
				f'There was an error during insertion; {word} not added.'
			)
		return False

	def process_update_word_check(self, record, meaning, pronunciation, exchange)
		return meaning and pronunciation and \
			(
				record[2] != meaning or \
				record[3] != pronunciation or \
				record[4] != exchange
			)

	def process_update_word(self, word, meaning, pronunciation, exchange):
		res = QMessageBox.question(self, 'Question', 'About to overwrite exisiting record',
			QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
		if res == QMessageBox.Ok:
			res = self.db_operator.update_word(
				word, meaning, pronunciation, exchange
			)
			if res:
				self.infoLabel.setText('Existing word updated.')
			else:
				self.infoLabel.setText(
					f'There was an error during update; {word} not updated.'
				)
		else:
			self.infoLabel.setText('Gave up...')

	def cancel(self):
		self.close()

	def initUI(self):
		self.infoLabel = QLabel('Status: empty')
		self.onlineButton = QPushButton('Search Online')
		self.addButton = QPushButton('Add Record')
		self.clearButton = QPushButton('Clear')
		self.cancalButton = QPushButton('Cancel')

		hbox = QHBoxLayout()
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
		self.exchangeEdit.setPlaceholderText('Word\'s different forms')
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
		vbox_i.addWidget(self.infoLabel)

		vbox = QVBoxLayout()
		vbox.addLayout(vbox_i)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.setGeometry(300, 300, 500, 600)
		self.setWindowTitle('Record Management')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	ex = WordUi(db_operator)
	sys.exit(app.exec_())