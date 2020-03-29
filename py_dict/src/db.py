#!/usr/bin/python3

import pymysql

class DbOperator():
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='dictuser',
            password='dictuser123',
            database='dict_db',
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self.messages = []

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def db_commit(self):
        self.conn.commit()

    def db_fetchone(self, sql):
        try:
            self.cursor.execute(sql)
            # When result is empty, fetchone() returns None.
            return self.cursor.fetchone()
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return None

    def db_fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return tuple()

    def db_execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return False
        return True

    def select_word(self, word):
        sql = f'SELECT * FROM Words WHERE Word = "{word}"'
        return self.db_fetchone(sql)

    def select_like_word(self, word):
        sql = f'SELECT Word FROM Words WHERE Word LIKE "%{word}%"'
        return self.db_fetchall(sql)

    def select_usages(self, word):
        sql = f'SELECT `Usage` FROM `Usage` WHERE Word = "{word}"'
        return self.db_fetchall(sql)

    def select_article_for_word(self, word):
        sql = ''.join([
            'SELECT Article.Title, Content from Article ',
            'JOIN Reference ON Reference.Title = Article.Title ',
            f'WHERE Word = "{word}"'
        ])
        return self.db_fetchall(sql)

    def select_article(self, title):
        sql = f'SELECT * FROM Article WHERE Title = "{title}"'
        return self.db_fetchone(sql)

    def select_like_article(self, title):
        sql = f'SELECT Title FROM Article WHERE Title LIKE "%{title}%"'
        return self.db_fetchall(sql)

    def select_all_articles(self):
        sql = 'SELECT Title FROM Article'
        return self.db_fetchall(sql)	

    def select_all_articles_for_mapping(self):
        sql = 'SELECT Title, Content FROM Article'
        return self.db_fetchall(sql)

    def select_all_words(self):
        sql = 'SELECT Word FROM Words'
        return self.db_fetchall(sql)

    def insert_article(self, title, content):
        sql = f'INSERT INTO Article (Title, Content) VALUES ("{title}", "{content}")'
        return self.db_execute(sql)

    def insert_word(self, word, meaning, pron, exchange):
        sql = ''.join([
            'INSERT INTO Words\n',
            '(Word, Meaning, Pronunciation, Exchange, `date`)\n',
            'VALUES\n',
            f'("{word}", "{meaning}", "{pron}", "{exchange}", CURDATE())'
        ])
        return self.db_execute(sql)

    def update_article(self, title, content):
        sql = ''.join([
            f'UPDATE Article SET Content="{content}"\n',
            f'WHERE Title="{title}"'
        ])
        return self.db_execute(sql)

    def update_word(self, word, meaning, pron, exchange):
        sql = ''.join([
            f'UPDATE Words SET Meaning="{meaning}", Pronunciation="{pron}", Exchange="{exchange}", `date`=CURDATE()\n',
            f'WHERE Word="{word}"'
        ])
        return self.db_execute(sql)

    def insert_usage(self, word, usage):
        sql = f'INSERT INTO `Usage` (Word, `Usage`) VALUES ("{word}", "{usage}")'
        return self.db_execute(sql)

    def insert_article(self, title, content):
        sql = f'INSERT INTO Article (Title, Content) VALUES ("{title}", "{content}")'
        return self.db_execute(sql)

    def truncate_reference(self):
        sql = 'TRUNCATE TABLE Reference'
        return self.db_execute(sql)

    def insert_reference(self, word, title):
        sql = f'INSERT INTO Reference (Word, Title) VALUES ("{word}", "{title}")'
        return self.db_execute(sql)

    def delete_a_word(self, word):
        sqls = [
            'DELETE FROM Reference WHERE Word="{}"'.format(word),
            'DELETE FROM `Usage` WHERE Word="{}"'.format(word),
            'DELETE FROM Words WHERE Word="{}"'.format(word)
        ]
        try:
            for sql in sqls:
                self.cursor.execute(sql)
            self.db_commit()
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sqls}, due to {e.args[-1]}'
            )
            return False
        return True

    def delete_a_article(self, title):
        sqls = [
            'DELETE FROM Reference WHERE Title="{}"'.format(title),
            'DELETE FROM Article WHERE Title="{}"'.format(title)
        ]
        try:
            for sql in sqls:
                self.cursor.execute(sql)
            self.db_commit()
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sqls}, due to {e.args[-1]}'
            )
            return False
        return True

    def print_messages(self):
        print('--- All messages ---')
        for message in self.messages:
            print(message)
        self.messages = []
        print('--- End of all messages ---')

def db_access_test(db_operator):
    pass

if __name__ == '__main__':
    # db_operator = DbOperator()
    # db_access_test(db_operator)
    pass