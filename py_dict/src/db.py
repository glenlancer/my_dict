#!/usr/bin/python3

import os
import pymysql

class DbOperator():
    __DB_USERNAME = 'dictuser'
    __DB_PASSWORD = 'dictuser123'
    __DB_DBNAME = 'dict_db'

    def __init__(self):
        self.messages = []
        # TODO Implement in memory data handling to avoid unnecessary
        # Database accessing.
        self.in_memory_data = {
            'Words': {},
            'Usage': {},
            'Article': {},
            'Reference': {}
        }

    def __del__(self):
        self.db_close()

    def try_db_connect(self):
        try:
            self.db_connect()
        except Exception as e:
            '''
            Error code:
            (1) 2003 - Can't connect to server, possibly due to MySql service is not up or installed.
            (2) 1044 - Access denied, possibly due to db doesn't exist.
            (3) 1045 - Access denied, possibly due to user doesn't exist.
            (4) 1049 - Unknown database, possibly due to db doesn't exist.
            '''
            return e.args
        return (0, 'Success')

    def db_connect(self):
        self.conn = pymysql.connect(
            host='localhost',
            user=self.__DB_USERNAME,
            password=self.__DB_PASSWORD,
            database=self.__DB_DBNAME,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def db_connect_with_no_specified_db(self):
        self.conn = pymysql.connect(
            host='localhost',
            user=self.__DB_USERNAME,
            password=self.__DB_PASSWORD,
            charset='utf8')
        self.cursor = self.conn.cursor()

    def db_create_database(self):
        try:
            self.db_connect_with_no_specified_db()
        except Exception as e:
            os.system(f'cat {e.args[0]}:{e.args[1]} > dict_error.log')
            return
        self.db_create_db_and_tables()

    def db_create_db_and_tables(self):
        sqls = [
            'create database if not exists dict_db',
            'use dict_db',
            '''
                create table Words (
                    WID           serial,
                    Word          varchar(50) not null unique,
                    Meaning       varchar(250) not null,
                    Pronunciation varchar(50),
                    Exchange      varchar(100),
                    `date`        datetime not null,
                    primary key (Word)
                ) ENGINE=InnoDB Default Charset=utf8
            ''',
            '''
                create table `Usage` (
                    UID     serial,
                    Word    varchar(50) not null,
                    `Usage` text not null,
                    primary key (UID),
                    foreign key (Word) references Words(Word)
                ) ENGINE=InnoDB Default Charset=utf8
            ''',
            '''
                create table Article (
                    AID     serial,
                    Title   varchar(100) not null unique,
                    Content text not null,
                    primary key (AID)
                ) ENGINE=InnoDB Default Charset=utf8
            ''',
            '''
                create table Reference (
                    RID serial,
                    Word varchar(50) not null,
                    Title varchar(100) not null,
                    primary key (RID),
                    foreign key (Word) references Words(Word),
                    foreign key (Title) references Article(Title)
                ) ENGINE=InnoDB Default Charset=utf8
            '''
        ]
        self.execute_all_sqls(sqls, False)

    def db_close(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

    def db_commit(self):
        self.conn.commit()

    def db_export_to_file(self, file_name):
        return os.system(f'mysqldump -u{self.__DB_USERNAME} -p{self.__DB_PASSWORD} {self.__DB_DBNAME} > {file_name}')

    def db_import_from_file(self, file_name):
        return os.system(f'mysql -u{self.__DB_USERNAME} -p{self.__DB_PASSWORD} {self.__DB_DBNAME} < {file_name}')

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

    def drop_all_tables(self):
        sqls = [
            'DROP TABLE Reference',
            'DROP TABLE `Usage`',
            'DROP TABLE Article',
            'DROP TABLE Words'
        ]
        return self.execute_all_sqls(sqls, False)

    def delete_a_word(self, word):
        sqls = [
            'DELETE FROM Reference WHERE Word="{}"'.format(word),
            'DELETE FROM `Usage` WHERE Word="{}"'.format(word),
            'DELETE FROM Words WHERE Word="{}"'.format(word)
        ]
        return self.execute_all_sqls(sqls)

    def delete_a_article(self, title):
        sqls = [
            'DELETE FROM Reference WHERE Title="{}"'.format(title),
            'DELETE FROM Article WHERE Title="{}"'.format(title)
        ]
        return self.execute_all_sqls(sqls)

    def execute_all_sqls(self, sqls, need_commit=True):
        try:
            for sql in sqls:
                self.cursor.execute(sql)
            if need_commit:
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