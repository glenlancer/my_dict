#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMessageBox,
    QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from PyQt5.QtGui import QIcon, QFont
from .function import *
from .db import DbOperator

# https://pythonprogramminglanguage.com/pyqt-line-edit/

class ArticleUi(QWidget):
    def __init__(self, db_operator, icon):
        super().__init__()
        self.db_operator = db_operator
        self.icon = icon
        self.initUI()
        self.initAction()
        self.setFont(QFont('Noto San', 9))

    def initAction(self):
        self.cancalButton.clicked.connect(self.cancel)
        self.addButton.clicked.connect(self.add)

    def getTitle(self):
        return self.titleEdit.text().strip().lower()

    def add(self):
        title = self.getTitle()
        content = self.contentEdit.toPlainText().strip()

        if title == '' or content == '':
            self.infoLabel.setText('The title and content can\'t be empty...')
            return

        if DEBUG_FLAG:
            print('title', title)
            print('content')
            print(content)

        record = self.db_operator.select_article(title)
        if record is None:
            self.process_insert_article(title, content)
        elif record[1] != content:
            print('old', record[1])
            print('new', content)
            self.process_update_article(title, content)
        else:
            self.infoLabel.setText('Article is unchanged.')
        self.db_operator.db_commit()
        self.db_operator.print_messages()

    def process_insert_article(self, title, content):
        res = self.db_operator.insert_article(
                title, content
            )
        if res:
            self.infoLabel.setText('Article is added.')
        else:
            self.infoLabel.setText('Article failed to be added.')

    def process_update_article(self, title, content):
        res = QMessageBox.question(self, 'Question', 'About to update exisiting article',
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if res == QMessageBox.Ok:
            res = self.db_operator.update_article(
                title, content
            )
            if res:
                self.infoLabel.setText('Article is updated.')
            else:
                self.infoLabel.setText('Article failed to be updated')
        else:
            self.infoLabel.setText('Gave up...')

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
        self.contentEdit.setPlaceholderText('Put the content of the article here')
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
        self.setWindowIcon(self.icon)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_operator = DbOperator()
    ex = ArticleUi(db_operator)
    sys.exit(app.exec_())