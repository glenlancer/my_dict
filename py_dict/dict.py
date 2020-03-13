#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
	QApplication, QMainWindow,
	QGridLayout, QHBoxLayout,
	QAction, qApp, QWidget,
	QLabel, QTextEdit,
	QPushButton, QLineEdit, QListWidget
)
from PyQt5.QtGui import QIcon, QFont
from src.word import WordUi
from src.article import ArticleUi
from src.mapping import MappingUi
from src.deleter import DeleterUi
from src.show import ShowerUi
from src.function import *
from src.db import DbOperator

# https://pythonspot.com/pyqt5-horizontal-layout/
class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = "Glen's Personal Dictionary"
		self.left = 10
		self.top = 10
		self.width = 820
		self.height = 500
		self.db_operator = DbOperator()
		self.word_ui = WordUi(self.db_operator)
		self.article_ui = ArticleUi(self.db_operator)
		self.mapping_ui = MappingUi(self.db_operator)
		self.deleter_ui = DeleterUi(self.db_operator)
		self.shower_ui = ShowerUi()
		self.setupMenus()
		self.initUI()
		self.initAction()
		self.setFont(QFont('Arial', 11))
		self.results = None
		self.articles = {}

	def initAction(self):
		self.wordEdit.textChanged.connect(self.searchRecords)
		self.searchBtn.clicked.connect(self.searchRecords)
		self.wordList.clicked.connect(self.wordListClicked)
		self.articleList.clicked.connect(self.articleListClicked)

	def showWordDetail(self, word):
		record = self.db_operator.select_word(word)
		self.meaning.setText(record[2])
		self.sound.setText(record[3])
		self.exchange.setText(record[4])
		usages = self.db_operator.select_usages(word)
		all_usage = ''
		for usage in usages:
			if all_usage != '':
				all_usage += '\n'
			all_usage += usage[0]
		self.usageEdit.setText(all_usage)
		res_articles = self.db_operator.select_article_for_word(word)
		for article in res_articles:
			self.articles[article[0]] = article[1]
		for key in self.articles.keys():
			self.articleList.addItem(key)

	def wordListClicked(self, index):
		self.clearRightPanel()
		i = index.row()
		item = self.wordList.item(i).text()
		self.showWordDetail(item)

	def articleListClicked(self, index):
		i = index.row()
		item = self.articleList.item(i).text()
		article_record = self.db_operator.select_article(item)
		if article_record:
			content = {
				'title': article_record[1],
				'content': article_record[2]
			}
		else:
			conent = {
				'title': 'No record',
				'content': 'There is no relevant article found.'
			}
		self.shower_ui.initWebView('show_article', content)
		self.shower_ui.show()

	def clearUi(self):
		self.wordList.clear()
		self.clearRightPanel()

	def clearRightPanel(self):
		self.meaning.setText('')
		self.sound.setText('')
		self.exchange.setText('')
		self.usageEdit.setPlainText('')
		self.articleList.clear()
		self.articles.clear()

	def searchRecords(self, key=None):
		self.clearUi()
		if key in (None, False):
			key = self.wordEdit.text().strip()
		key = key.lower()
		if key == '':
			self.results = self.db_operator.select_all_words()
		else:
			self.results = self.db_operator.select_like_word(key)
		self.results = list(self.results)
		self.results = list(map(lambda x: x[0], self.results))
		self.wordList.addItems(self.results)

	def initUI(self):
		main = QHBoxLayout()

		grid = QGridLayout()
		grid.setSpacing(10)
		self.wordEdit = QLineEdit()
		self.wordEdit.setPlaceholderText('Word to search')
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
		self.exchange = QLineEdit()
		usageLabel = QLabel('Usage')
		articleLabel = QLabel('Article')
		self.usageEdit = QTextEdit()
		self.articleList = QListWidget()
		grid2.addWidget(self.meaning, 1, 1)
		self.meaning.setPlaceholderText('Word\'s meaning to show here.')
		grid2.addWidget(self.sound, 2, 1)
		self.sound.setPlaceholderText('Word\'s pronunciation to show here.')
		grid2.addWidget(self.exchange, 3, 1)
		self.exchange.setPlaceholderText('Word\'s different types to show here.')
		grid2.addWidget(usageLabel, 4, 1)
		grid2.addWidget(self.usageEdit, 5, 1, 4, 1)
		self.usageEdit.setPlaceholderText('Word\'s usage to show here')
		grid2.addWidget(articleLabel, 9, 1)
		grid2.addWidget(self.articleList, 10, 1, 5, 1)
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

		addWordAction = QAction('&Record', self)
		addWordAction.setStatusTip('Add Word & Usage')
		addWordAction.triggered.connect(self.word_ui.show)
		appMenu.addAction(addWordAction)

		addArticleAction = QAction('&Article', self)
		addArticleAction.setStatusTip('Add Article')
		addArticleAction.triggered.connect(self.article_ui.show)
		appMenu.addAction(addArticleAction)

		deleteAction = QAction('Delete &Records', self)
		deleteAction.setStatusTip('Delete Records')
		deleteAction.triggered.connect(self.deleter_ui.show)
		appMenu.addAction(deleteAction)

		matchAction = QAction('&Matchmaking', self)
		matchAction.setStatusTip('Mapping Words and Articles')
		matchAction.triggered.connect(self.mapping_ui.show)
		appMenu.addAction(matchAction)

		exitAction = QAction('&Exit', self)
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)		
		appMenu.addAction(exitAction)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())