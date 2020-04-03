#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QHBoxLayout, QVBoxLayout,
    QRadioButton, QButtonGroup, QPushButton,
    QLineEdit, QLabel, QListWidget
)
from PyQt5.QtGui import QFont

from .db import DbOperator
from .show import ShowerUi
from .function import *

class DeleterUi(QWidget):
    def __init__(self, db_operator):
        super().__init__()
        self.deleteType = 'word'
        self.db_operator = db_operator
        self.shower_ui = ShowerUi(self.db_operator, self)
        self.initUI()
        self.initAction()
        self.setFont(QFont('Noto San', 9))
        self.results = None
        self.radioBtnWord.setChecked(True)

    def closeEvent(self, event):
        self.shower_ui.close()

    def searchRecords(self, key=None):
        self.resultList.clear()
        if key in (None, False):
            key = self.searchText.text().strip()
        key = key.lower()
        if self.deleteType == 'word':
            if key == '':
                self.results = self.db_operator.select_all_words()
            else:
                self.results = self.db_operator.select_like_word(key)
        else:
            if key == '':
                self.results = self.db_operator.select_all_articles()
            else:
                self.results = self.db_operator.select_like_article(key)
        self.results = list(self.results)
        self.results = list(map(lambda x: x[0], self.results))
        self.resultList.addItems(self.results)

    def initAction(self):
        self.searchText.textChanged.connect(self.searchRecords)
        self.searchButton.clicked.connect(self.searchRecords)
        self.resultList.clicked.connect(self.resultListClicked)

    def initUI(self):
        hbox_1 = QHBoxLayout()
        self.radioBtnWord = QRadioButton('Word')
        self.radioBtnArticle = QRadioButton('Article')
        self.radioBtnGroup = QButtonGroup()
        self.radioBtnGroup.addButton(self.radioBtnWord)
        self.radioBtnGroup.addButton(self.radioBtnArticle)
        self.radioBtnWord.toggled.connect(
            lambda : self.btnState(self.radioBtnWord)
        )
        self.radioBtnArticle.toggled.connect(
            lambda : self.btnState(self.radioBtnArticle)
        )
        hbox_1.addWidget(self.radioBtnWord)
        hbox_1.addWidget(self.radioBtnArticle)

        hbox_2 = QHBoxLayout()
        self.searchText = QLineEdit(self)
        self.searchButton = QPushButton('Search')
        hbox_2.addWidget(self.searchText)
        hbox_2.addWidget(self.searchButton)

        vbox_i = QVBoxLayout()
        searchLabel = QLabel('Search Result:')
        self.resultList = QListWidget()
        vbox_i.addWidget(searchLabel)
        vbox_i.addWidget(self.resultList)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        vbox.addLayout(vbox_i)
        self.setLayout(vbox)
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('Delete Records')

    def btnState(self, button):
        if button.text() == 'Word' and self.deleteType != 'word':
            self.deleteType = 'word'
            self.searchText.setPlaceholderText('Word to search')
        elif button.text() == 'Article' and self.deleteType != 'article':
            self.deleteType = 'article'
            self.searchText.setPlaceholderText('Title of Article to search')
        self.resultList.clear()

    def clearResultList(self):
        self.resultList.clear()

    def resultListClicked(self, index):
        i = index.row()
        item = self.resultList.item(i).text()
        item = escape_double_quotes(item)
        if self.deleteType == 'word':
            record = self.db_operator.select_word(item)
            usages = self.db_operator.select_usages(item)
            if None in (record, usages):
                content = None
            else:
                content = {
                    'word': record[1],
                    'meaning': record[2],
                    'sound': record[3],
                    'exchange': record[4],
                    'usage': combine_usage_str(usages)
                }
            self.shower_ui.initWebView('show_word', content)
        else:
            record = self.db_operator.select_article(item)
            if record is None:
                content = None
            else:
                content = {
                    'title': record[1],
                    'content': record[2]
                }
            self.shower_ui.initWebView('show_article', content)
        self.shower_ui.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_operator = DbOperator()
    ex = DeleterUi(db_operator)
    ex.show()
    sys.exit(app.exec_())