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
		title = self.titleEdit.text().strip()
		content = self.contentEdit.toPlainText().strip()

		print('title', title)
		print('content')
		print(content)

		gotArticleRecord = self.db_operator.select_article(title)
		if gotArticleRecord is None:
			self.db_operator.insert_article(
				title, content
			)
		elif title != '' and content != '' and \
			 gotWordRecord[1] != title and gotWordRecord[2] != content:
			self.db_operator.update_word(
				title, content
			)
		self.db_operator.db_commit()
		self.db_operator.print_messages()

	def cancel(self):
		self.close()

	def initUI(self):
		self.addButton = QPushButton('Add the article')
		self.cancalButton = QPushButton('Cancel')

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.addButton)
		hbox.addWidget(self.cancalButton)
		vbox_i = QVBoxLayout()
		vbox_i.addStretch(1)
		titleLabel = QLabel('Title')
		contentLabel = QLabel('Content')
		self.titleEdit = QLineEdit(self)
		self.contentEdit = QTextEdit(self)
		vbox_i.addWidget(titleLabel)
		vbox_i.addWidget(self.titleEdit)
		vbox_i.addWidget(contentLabel)
		vbox_i.addWidget(self.contentEdit)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(vbox_i)
		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.setGeometry(300, 300, 500, 300)
		self.setWindowTitle('Add new article')
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	db_operator = DbOperator()
	ex = WordUi(db_operator)
	sys.exit(app.exec_())