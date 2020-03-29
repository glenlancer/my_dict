#!/usr/bin/python3

import sys, re
from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from .db import DbOperator

class MappingUi(QWidget):
    def __init__(self, db_operator):
        super().__init__()
        self.db_operator = db_operator
        self.initUI()
        self.initAction()
        self.setFont(QFont('Noto San', 9))

    def closeEvent(self, event):
        self.progressBar.setValue(0)

    def initAction(self):
        self.createButton.clicked.connect(self.create)
        self.cancelButton.clicked.connect(self.cancel)

    def create(self):
        all_words = self.db_operator.select_all_words()
        all_articles = self.db_operator.select_all_articles_for_mapping()
        if all_words is None:
            self.infoLabel.setText('There are no word found.')
            return
        if all_articles is None:
            self.infoLabel.setText('There are no article found.')
            return
        self.total_count = len(all_words)
        self.total_article = len(all_articles)
        self.create_mapping(all_words, all_articles)
        self.infoLabel.setText(
            f'{self.count} mappings have been made '
            f'between {self.total_count} words and {self.total_article} articles.')

    def create_mapping(self, all_words, all_articles):
        index = 0
        self.count = 0
        self.db_operator.truncate_reference()
        for word in all_words:
            for article in all_articles:
                res = re.search(
                    word[0],
                    article[1],
                    flags=re.IGNORECASE
                )
                if res is None:
                    continue
                self.db_operator.insert_reference(word[0], article[0])
                self.count += 1
            index += 1
            self.make_progress(index)
        self.db_operator.db_commit()
        self.db_operator.print_messages()

    def make_progress(self, step):
        value = int(step / self.total_count * 99 + 1)
        self.progressBar.setValue(value)

    def cancel(self):
        self.close()

    def initUI(self):
        self.infoLabel = QLabel('Status: empty')
        self.aboutLabel = QLabel(
            'Clicking the button here will create a mapping\n'
            'between Words and Article table'
        )
        self.aboutLabel.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar()
        self.createButton = QPushButton('Create')
        self.cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addWidget(self.createButton)
        hbox.addWidget(self.cancelButton)

        vbox_i = QVBoxLayout()
        vbox_i.addWidget(self.aboutLabel)
        vbox_i.addWidget(self.progressBar)
        vbox_i.addWidget(self.infoLabel)

        vbox = QVBoxLayout()
        vbox.addLayout(vbox_i)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 450, 60)
        self.setWindowTitle('Mapping')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_operator = DbOperator()
    ex = MappingUi(db_operator)
    sys.exit(app.exec_())