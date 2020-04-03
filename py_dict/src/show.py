#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from .db import DbOperator
from .function import *

class ShowerUi(QWidget):
    def __init__(self, db_operator=None, parent_win=None):
        super().__init__()
        self.type = 'show_word'
        self.content = None
        self.parent_win = parent_win
        self.db_operator = db_operator
        if self.db_operator:
            self.setWindowModality(Qt.WindowModal)
            self.deletion_count = 0
        self.initUI()
        self.initAction()
        self.setFont(QFont('Noto San', 9))

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

    def closeEvent(self, event):
        if self.parent_win and self.deletion_count > 0:
            self.parent_win.clearResultList()

    def initWebView(self, show_type, content):
        self.type = show_type
        self.content = content
        if self.content is None:
            self.webView.setHtml('<p>Content 404 :(</p>')
            self.setWindowTitle('The record is nil')
        elif self.type == 'show_word':
            self.content["usage"] = self.content["usage"].replace('\n', '<br>')
            self.webView.setHtml(f'''
        <strong>{self.content["word"]}</strong>
        <p>
            {self.content["meaning"]}<br>
            {self.content["sound"]}<br>
            {self.content["exchange"]}
        </p>
        <p>
            <span>Usage:</span><br>
            {self.content["usage"]}
        </p>
            ''')
            self.setWindowTitle('Word\'s details')
        else:
            html = f'<h5>{self.content["title"]}</h5>'
            paragraphs = self.content['content'].split('\n\n')
            for paragraph in paragraphs:
                html += f'<p>{paragraph}</p>'
            self.webView.setHtml(html)
            self.setWindowTitle(f'{self.content["title"]}')

    def initAction(self):
        if self.db_operator:
            self.deleteButton.clicked.connect(self.deleteRecord)

    def deleteRecord(self):
        res = None
        if self.type == 'show_word' and self.content:
            res = self.db_operator.delete_a_word(self.content['word'])
        elif self.content:
            res = self.db_operator.delete_a_article(
                escape_double_quotes(self.content['title'])
            )
        self.db_operator.print_messages()
        if res:
            self.deletion_count += 1
            self.infoLabel.setText('Recrod has been deleted.')
        else:
            self.infoLabel.setText('There is an error happened during deletion.')

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
    ex = ShowerUi(db_operator)
    ex.initWebView(content2['type'], content2)
    ex.show()
    sys.exit(app.exec_())