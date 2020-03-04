import sys
from PyQt5.QtWidgets import (
	QWidget, QPushButton,
	QHBoxLayout, QVBoxLayout,
	QLabel, QLineEdit, QTextEdit,
	QApplication
)

from db import DbOperator

# https://pythonprogramminglanguage.com/pyqt-line-edit/

class WordUi(QWidget):
	def __init__(self, db_operator):
		super().__init__()
		self.db_operator = db_operator
		self.initUI()
		self.initAction()

	def initAction(self):
		self.cancalButton.clicked.connect(self.cancel)
		self.addButton.clicked.connect(self.add)

	def add(self):
		word = self.wordEdit.text().strip()
		meaning = self.meanEdit.text().strip()
		pronunciation = self.pronEdit.text().strip()
		usage = self.usageEdit.toPlainText().strip()

		print('word', word)
		print('meaning', meaning)
		print('Pronunciation', pronunciation)
		print('Usage', usage)

		gotWordRecord = self.db_operator.select_word(word)
		if gotWordRecord is None:
			self.db_operator.insert_word(
				word, meaning, pronunciation
			)
		elif meaning != '' and pronunciation != '' and \
			 gotWordRecord[2] != meaning and gotWordRecord[3] != pronunciation:
			self.db_operator.update_word(
				word, meaning, pronunciation
			)
		if usage:
			self.db_operator.insert_usage(word, usage)
		self.db_operator.db_commit()
		self.db_operator.print_messages()

	def cancel(self):
		self.close()

	def initUI(self):
		self.addButton = QPushButton('Add new word')
		self.cancalButton = QPushButton('Cancel')

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.addButton)
		hbox.addWidget(self.cancalButton)

		vbox_i = QVBoxLayout()
		vbox_i.addStretch(1)
		wordLabel = QLabel('New Word')
		meanLabel = QLabel('Meaning')
		pronLabel = QLabel('Pronunciation')
		usageLabel = QLabel('Usage')
		self.wordEdit = QLineEdit(self)
		self.meanEdit = QLineEdit(self)
		self.pronEdit = QLineEdit(self)
		self.usageEdit = QTextEdit(self)
		vbox_i.addWidget(wordLabel)
		vbox_i.addWidget(self.wordEdit)
		vbox_i.addWidget(meanLabel)
		vbox_i.addWidget(self.meanEdit)
		vbox_i.addWidget(pronLabel)
		vbox_i.addWidget(self.pronEdit)
		vbox_i.addWidget(usageLabel)
		vbox_i.addWidget(self.usageEdit)	

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(vbox_i)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.setGeometry(300, 300, 500, 400)
		self.setWindowTitle('Add new word')
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	ex = WordUi(db_operator)
	sys.exit(app.exec_())