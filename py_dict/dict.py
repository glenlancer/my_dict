#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QGridLayout, QHBoxLayout,
    QAction, qApp, QWidget,
    QLabel, QTextEdit,
    QPushButton, QLineEdit,
    QListWidget, QFileDialog,
    QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from src.word import WordUi
from src.article import ArticleUi
from src.mapping import MappingUi
from src.deleter import DeleterUi
from src.show import ShowerUi
from src.function import *
from src.db import DbOperator

# https://pythonspot.com/pyqt5-horizontal-layout/

'''
Road Map:
(1) Use qtawesome
(2) Analysing cacheout
(3) Implement some function to export Db to csv, pdf, etc.
'''

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Glen's Personal Dictionary"
        self.icon = QIcon('images/logo.ico')
        self.left = 10
        self.top = 10
        self.width = 820
        self.height = 500
        self.setupMenus()
        self.initUI()
        self.initAction()
        self.setFont(QFont('Noto San', 9))
        self.results = None
        self.db_operator = DbOperator()
        self.word_ui = WordUi(self.db_operator, self.icon)
        self.article_ui = ArticleUi(self.db_operator, self.icon)
        self.mapping_ui = MappingUi(self.db_operator, self.icon)
        self.deleter_ui = DeleterUi(self.db_operator, self.icon)
        self.shower_ui = ShowerUi(None, self.icon)
        ret_code, ret_message = self.db_operator.try_db_connect()
        if ret_code == 0:
            return
        elif ret_code == 2003:
            self.handleMysqlDown(ret_message)
        elif ret_code in (1044, 1049):
            self.handleDbConnectionIssue(ret_code, ret_message)
        elif ret_code == 1045:
            self.handleUserNotExist(ret_message)
        sys.exit(0)

    def closeEvent(self, event):
        self.word_ui.close()
        self.article_ui.close()
        self.mapping_ui.close()
        self.deleter_ui.close()
        self.shower_ui.close()
        self.db_operator.db_close()

    def initAction(self):
        self.wordEdit.textChanged.connect(self.searchRecords)
        self.searchBtn.clicked.connect(self.searchRecords)
        self.wordList.clicked.connect(self.wordListClicked)
        self.articleList.clicked.connect(self.articleListClicked)

    def getWord(self):
        return self.wordEdit.text().strip().lower()

    def showWordDetail(self, word):
        record = self.db_operator.select_word(word)
        if record is None:
            self.statusBar().showMessage(
                f'Chosen word ({word}) doesn\'t exist, re-generating word list.'
            )
            self.wordList.clear()
            self.searchRecords(self.getWord(), clear_cache=True)
            return
        self.meaning.setText(record[0])
        self.meaning.setCursorPosition(0)
        self.sound.setText(record[1])
        self.sound.setCursorPosition(0)
        self.exchange.setText(record[2])
        self.exchange.setCursorPosition(0)
        usages = self.db_operator.select_usages(word)
        self.usageEdit.setText(combine_usage_str(usages))
        res_articles = self.db_operator.select_article_for_word(word)
        if res_articles is None:
            res_articles = []
        for title in res_articles:
            self.articleList.addItem(title)

    def wordListClicked(self, index):
        self.clearRightPanel()
        i = index.row()
        item = self.wordList.item(i).text()
        self.showWordDetail(item)

    def articleListClicked(self, index):
        i = index.row()
        item = self.articleList.item(i).text()
        article_content = self.db_operator.select_article(item)
        if article_content:
            content = {
                'title': item,
                'content': article_content
            }
        else:
            content = {
                'title': 'No record',
                'content': 'There is no relevant article found.'
            }
        self.shower_ui.initWebView('show_article', content)
        self.shower_ui.show()
        self.shower_ui.setFocus()
        self.shower_ui.activateWindow()

    def clearUi(self):
        self.wordList.clear()
        self.clearRightPanel()

    def clearRightPanel(self):
        self.meaning.setText('')
        self.sound.setText('')
        self.exchange.setText('')
        self.usageEdit.setPlainText('')
        self.articleList.clear()

    def searchRecords(self, key=None, clear_cache=False):
        self.clearUi()
        if key in (None, False):
            key = self.getWord()
        if not is_a_word(key):
            self.statusBar().showMessage(f'The word ({key}) is not valid.')
            return
        if key == '':
            self.results = self.db_operator.select_all_words(clear_cache)
        else:
            self.results = self.db_operator.select_like_word(key, clear_cache)
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
        self.setWindowIcon(self.icon)
        self.statusBar().showMessage('Ready')
        self.show()

    def show_word_ui(self):
        self.word_ui.show()
        self.word_ui.setFocus()
        self.word_ui.activateWindow()
    
    def show_article_ui(self):
        self.article_ui.show()
        self.article_ui.setFocus()
        self.article_ui.activateWindow()

    def show_deleter_ui(self):
        self.deleter_ui.show()
        self.deleter_ui.setFocus()
        self.deleter_ui.activateWindow()

    def show_mapping_ui(self):
        self.mapping_ui.show()
        self.mapping_ui.setFocus()
        self.mapping_ui.activateWindow()

    def setupMenus(self):
        menuBar = self.menuBar()
        appMenu = menuBar.addMenu('&App')

        addWordAction = QAction('&Record', self)
        addWordAction.setStatusTip('Add Word & Usage')
        addWordAction.triggered.connect(self.show_word_ui)
        appMenu.addAction(addWordAction)

        addArticleAction = QAction('&Article', self)
        addArticleAction.setStatusTip('Add Article')
        addArticleAction.triggered.connect(self.show_article_ui)
        appMenu.addAction(addArticleAction)

        deleteAction = QAction('Delete &Records', self)
        deleteAction.setStatusTip('Delete Records')
        deleteAction.triggered.connect(self.show_deleter_ui)
        appMenu.addAction(deleteAction)

        matchAction = QAction('&Matchmaking', self)
        matchAction.setStatusTip('Mapping Words and Articles')
        matchAction.triggered.connect(self.show_mapping_ui)
        appMenu.addAction(matchAction)

        self.exitAction = QAction('&Exit', self)
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        appMenu.addAction(self.exitAction)

        dbMenu = menuBar.addMenu('&Db Operations')
        exportDbToFileAction = QAction('&Export', self)
        exportDbToFileAction.setStatusTip('Export Db to File')
        exportDbToFileAction.triggered.connect(self.export_db_to_file)
        dbMenu.addAction(exportDbToFileAction)

        importFileToDbAction = QAction('&Import', self)
        importFileToDbAction.setStatusTip('Import File to Db')
        importFileToDbAction.triggered.connect(self.import_file_to_db)
        dbMenu.addAction(importFileToDbAction)

    def export_db_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            'Export Db to File',
            './',
            'Sql Files (*.sql)'
        )
        if not file_name:
            return
        res = self.db_operator.db_export_to_file(file_name)
        if res:
            QMessageBox.information(
                self,
                'Information',
                f'Export Db to {file_name} failed, error code is {res}')
        else:
            QMessageBox.information(
                self,
                'Information',
                f'Export Db to {file_name} succeeded.'
            )

    def import_file_to_db(self):
        res = QMessageBox.warning(
            self,
            'Warning',
            'This function probably shouldn\'t be used!\n'
            'To use this function, make sure of the following 3 points.\n'
            '(1) The file used for importing must make sense and correct.\n'
            '(2) This process will overwrite existing db, all current data WILL BE LOST!\n'
            '(3) The implementation of this function is very simple, so try manually if fail.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if res == QMessageBox.No:
            return
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            'Select Db file',
            './',
            'Sql Files (*.sql)')
        if not file_name:
            return
        res = self.db_operator.drop_all_tables()
        if not res:
            QMessageBox.information(
                self,
                'Information',
                'Drop all tables failed'
            )
            return
        res = self.db_operator.db_import_from_file(file_name)
        if res:
            QMessageBox.information(
                self,
                'Information',
                f'Import {file_name} to Db failed, error code is {res}')
        else:
            QMessageBox.information(
                self,
                'Information',
                f'Import {file_name} to Db succeeded.'
            )

    def handleMysqlDown(self, message):
        QMessageBox.information(
            self,
            'Information',
            'Error: 2003\n'
            f'Message: {message}\n'
            'This is possibly due to MySql service is not up or installed.\n'
            'Please start or install Mysql service first and try again.')

    def handleDbConnectionIssue(self, code, message):
        res = QMessageBox.question(
            self,
            'Question',
            f'Error: {code}\n'
            f'Message: {message}\n'
            'This is possibly due to db doesn\'t exist.\n'
            'Try to create database (and tables) before exit?',
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if res == QMessageBox.Ok:
            self.db_operator.db_create_database()

    def handleUserNotExist(self, message):
        QMessageBox.information(
            self,
            'Information',
            'Error: 1045\n'
            f'Message: {message}\n'
            'This is possibly due to user doesn\'t exist for the database.\n'
            'Please do something similar to below then try again.\n\n'
            "> create user 'dictuser'@'localhost' identified by 'dictuser123';\n"
            "> grant all privileges on `dict_db`.* to 'dictuser'@'localhost' identified by 'dictuser123';\n"
            "> flush privileges;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())