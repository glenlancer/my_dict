#!/usr/bin/python3

import os
import pymysql
from cacheout import LRUCache
from .function import DEBUG_FLAG
from .function import escape_double_quotes

class DbOperator():
    __DB_USERNAME = 'dictuser'
    __DB_PASSWORD = 'dictuser123'
    __DB_DBNAME = 'dict_db'
    __CACHE_MAXSIZE = 512

    # Use extra spaces, since no ordinary key allows this.
    __ALL_WORDS_KEY = ' ALL_WORDS '
    __ALL_ARTICLE_KEY = ' ALL_ARTICLE '

    def __init__(self):
        self.messages = []
        # TODO Implement in memory data handling to avoid unnecessary
        # Database accessing.
        self.words_detail_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)
        self.words_name_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)
        self.usage_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)
        self.article_detail_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)
        self.article_name_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)
        self.reference_cache = LRUCache(maxsize=self.__CACHE_MAXSIZE)

    def __del__(self):
        self.db_close()

    def __cache_analysis(self):
        pass

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
            res = self.cursor.fetchone()
            if res is None:
                return None
            return list(res)
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return None

    def db_fetchall(self, sql):
        try:
            self.cursor.execute(sql)
            return list(map(lambda x: list(x), self.cursor.fetchall()))
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return list()

    def db_execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.messages.append(
                f'SQL failed: {sql}, due to {e.args[-1]}'
            )
            return False
        return True

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

    def select_word(self, word):
        record = self.words_detail_cache.get(word)
        if record:
            return record
        sql = f'SELECT Meaning, Pronunciation, Exchange FROM Words WHERE Word = "{word}"'
        record = self.db_fetchone(sql)
        if record:
            self.words_detail_cache.add(word, record)
        return record

    def select_like_word(self, word, clear_cache=False):
        if clear_cache:
            self.words_name_cache.delete(word)
        else:
            records = self.words_name_cache.get(word)
            if records is not None:
                return records
        sql = f'SELECT Word FROM Words WHERE Word LIKE "%{word}%"'
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.words_name_cache.add(word, records)
        return records

    def select_all_words(self, clear_cache=False):
        if clear_cache:
            self.words_name_cache.delete(self.__ALL_WORDS_KEY)
        else:
            records = self.words_name_cache.get(self.__ALL_WORDS_KEY)
            if records is not None:
                return records
        sql = 'SELECT Word FROM Words'
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.words_name_cache.add(self.__ALL_WORDS_KEY, records)
        return records

    def select_usages(self, word):
        records = self.usage_cache.get(word)
        if records is not None:
            return records
        sql = f'SELECT `Usage` FROM `Usage` WHERE Word = "{word}"'
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.usage_cache.add(word, records)
        return records

    def select_article_for_word(self, word):
        records = self.reference_cache.get(word)
        if records is not None:
            return records
        sql = ''.join([
            'SELECT Article.Title from Article ',
            'JOIN Reference ON Reference.Title = Article.Title ',
            f'WHERE Word = "{word}"'
        ])
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.reference_cache.add(word, records)
        return records

    def select_article(self, title):
        record = self.article_detail_cache.get(title)
        if record:
            return record
        esd_title = escape_double_quotes(title)
        sql = f'SELECT Content FROM Article WHERE Title = "{esd_title}"'
        record = self.db_fetchone(sql)
        if record:
            self.article_detail_cache.add(title, record[0])
        return record if record is None else record[0]

    def select_like_article(self, title, clear_cache=False):
        if clear_cache:
            self.article_name_cache.delete(title)
        else:
            records = self.article_name_cache.get(title)
            if records is not None:
                return records
        esd_title = escape_double_quotes(title)
        sql = f'SELECT Title FROM Article WHERE Title LIKE "%{esd_title}%"'
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.article_name_cache.add(title, records)
        return records

    def select_all_article_titles(self, clear_cache=False):
        if clear_cache:
            self.article_name_cache.delete(self.__ALL_ARTICLE_KEY)
        else:
            records = self.article_name_cache.get(self.__ALL_ARTICLE_KEY)
            if records is not None:
                return records
        sql = 'SELECT Title FROM Article'
        records = self.db_fetchall(sql)
        records = list(map(lambda x: x[0], records))
        self.article_name_cache.add(self.__ALL_ARTICLE_KEY, records)
        return records

    def select_all_articles(self):
        sql = 'SELECT Title, Content FROM Article'
        records = self.db_fetchall(sql)
        self.article_detail_cache.clear()
        count = 0
        for record in records:
            if count < self.__CACHE_MAXSIZE:
                self.article_detail_cache.add(record[0], record[1])
                count += 1
            else:
                break
        return records

    def insert_word(self, word, meaning, pron, exchange):
        esd_meaning = escape_double_quotes(meaning)
        esd_pronunciation = escape_double_quotes(pron)
        esd_exchange = escape_double_quotes(exchange)
        sql = ''.join([
            'INSERT INTO Words\n',
            '(Word, Meaning, Pronunciation, Exchange, `date`)\n',
            'VALUES\n',
            f'("{word}", "{esd_meaning}", "{esd_pronunciation}", "{esd_exchange}", CURDATE())'
        ])
        res = self.db_execute(sql)
        if not res:
            return False
        self.words_detail_cache.add(word, [meaning, pron, exchange])
        self.words_name_cache.clear()
        return True

    def update_word(self, word, meaning, pron, exchange):
        esd_meaning = escape_double_quotes(meaning)
        esd_pronunciation = escape_double_quotes(pron)
        esd_exchange = escape_double_quotes(exchange)
        sql = ''.join([
            f'UPDATE Words SET Meaning="{esd_meaning}", Pronunciation="{esd_pronunciation}", Exchange="{esd_exchange}", `date`=CURDATE()\n',
            f'WHERE Word="{word}"'
        ])
        res = self.db_execute(sql)
        if not res:
            return False
        self.words_detail_cache.set(word, [meaning, pron, exchange])
        return True

    def insert_article(self, title, content):
        esd_title = escape_double_quotes(title)
        esd_content = escape_double_quotes(content)
        sql = f'INSERT INTO Article (Title, Content) VALUES ("{esd_title}", "{esd_content}")'
        res = self.db_execute(sql)
        if not res:
            return False
        self.article_detail_cache.add(title, content)
        self.article_name_cache.clear()
        return True

    def update_article(self, title, content):
        esd_title = escape_double_quotes(title)
        esd_content = escape_double_quotes(content)
        sql = ''.join([
            f'UPDATE Article SET Content="{esd_content}"\n',
            f'WHERE Title="{esd_title}"'
        ])
        res = self.db_execute(sql)
        if not res:
            return False
        self.article_detail_cache.set(title, content)
        return True

    def insert_usage(self, word, usage):
        esd_usage = escape_double_quotes(usage)
        sql = f'INSERT INTO `Usage` (Word, `Usage`) VALUES ("{word}", "{esd_usage}")'
        res = self.db_execute(sql)
        if not res:
            return False
        usages = self.usage_cache.get(word)
        if usages is None:
            usages = []
        usages.append(usage)
        self.usage_cache.set(word, usages)
        return True

    def insert_article(self, title, content):
        esd_title = escape_double_quotes(title)
        esd_content = escape_double_quotes(content)
        sql = f'INSERT INTO Article (Title, Content) VALUES ("{esd_title}", "{esd_content}")'
        res = self.db_execute(sql)
        if not res:
            return False
        self.article_detail_cache.add(title, content)
        self.article_name_cache.clear()
        return True

    def truncate_reference(self):
        sql = 'TRUNCATE TABLE Reference'
        res = self.db_execute(sql)
        if not res:
            return False
        self.reference_cache.clear()
        return True

    def insert_reference(self, word, title):
        esd_title = escape_double_quotes(title)
        sql = f'INSERT INTO Reference (Word, Title) VALUES ("{word}", "{esd_title}")'
        res = self.db_execute(sql)
        if not res:
            return False
        res = self.reference_cache.get(word)
        if res is None:
            self.reference_cache.add(word, [title])
        else:
            self.reference_cache.set(word, res.append(title))
        return True

    def drop_all_tables(self):
        sqls = [
            'DROP TABLE Reference',
            'DROP TABLE `Usage`',
            'DROP TABLE Article',
            'DROP TABLE Words'
        ]
        self.clear_all_caches()
        return self.execute_all_sqls(sqls, False)

    def delete_a_word(self, word):
        sqls = [
            'DELETE FROM Reference WHERE Word="{}"'.format(word),
            'DELETE FROM `Usage` WHERE Word="{}"'.format(word),
            'DELETE FROM Words WHERE Word="{}"'.format(word)
        ]
        res = self.execute_all_sqls(sqls)
        if not res:
            return False
        self.words_detail_cache.delete(word)
        self.usage_cache.delete(word)
        self.reference_cache.delete(word)
        # TODO Do we need to touch words_name_cache?
        # Seems not needed, since used a clear_cache parameter.
        return True

    def delete_a_article(self, title):
        esd_title = escape_double_quotes(title)
        sqls = [
            'DELETE FROM Reference WHERE Title="{}"'.format(esd_title),
            'DELETE FROM Article WHERE Title="{}"'.format(esd_title)
        ]
        res = self.execute_all_sqls(sqls)
        if not res:
            return False
        self.article_detail_cache.delete(title)
        for key in self.reference_cache.keys():
            value = self.reference_cache.get(key)
            if title in value:
                value.remove(title)
            self.reference_cache.set(key, value)
        # TODO Do we need to touch article_name_cache?
        # Seems not needed, since used a clear_cache parameter.
        return True

    def clear_all_caches(self):
        self.words_detail_cache.clear()
        self.words_name_cache.clear()
        self.usage_cache.clear()
        self.article_detail_cache.clear()
        self.article_name_cache.clear()
        self.reference_cache.clear()

    def print_messages(self):
        if DEBUG_FLAG:
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