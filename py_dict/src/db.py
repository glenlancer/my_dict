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

	def select_word(self, word):
		sql = ''.join([
			'select * from Words\n',
		    f'Where Word = "{word}"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchone()
		except Exception as e:
			self.messages.append(
				f'Selection of {word} failed due to {e.args[-1]}'
			)
			return None

	def select_usages(self, word):
		sql = ''.join([
			'select `Usage` from `Usage`\n',
		    f'Where Word = "{word}"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of usage for {word} failed due to {e.args[-1]}'
			)
			return None		

	def select_like_word(self, word):
		sql = ''.join([
			'SELECT Word FROM Words\n',
		    f'WHERE Word like "%{word}%"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of {word} failed due to {e.args[-1]}'
			)
			return None

	def select_article_for_word(self, word):
		sql = ''.join([
			'select Article.Title, Content from Article\n',
			'join Reference on Reference.Title = Article.Title\n',
			f'where Word = "{word}"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of Article for {word} failed due to {e.args[-1]}'
			)
			return None

	def select_article(self, title):
		sql = ''.join([
			'select * from Article\n',
		    f'where title = "{title}"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchone()
		except Exception as e:
			self.messages.append(
				f'Selection of {title} failed due to {e.args[-1]}'
			)
			return None

	def select_like_article(self, title):
		sql = ''.join([
			'SELECT Title FROM Article\n',
		    f'WHERE Title like "%{title}%"'
		])
		try:
			self.cursor.execute(sql)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of {word} like articles failed due to {e.args[-1]}'
			)
			return None

	def select_all_articles(self):
		try:
			self.cursor.execute(
				'select Title from Article'
			)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of all titles of articles failed due to {e.args[-1]}'
			)
			return None		

	def select_all_articles_for_mapping(self):
		try:
			self.cursor.execute(
				'select Title, Content from Article'
			)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of all articles failed due to {e.args[-1]}'
			)
			return None

	def select_all_words(self):
		try:
			self.cursor.execute(
				'select Word from Words'
			)
			return self.cursor.fetchall()
		except Exception as e:
			self.messages.append(
				f'Selection of all words failed due to {e.args[-1]}'
			)
		return None

	def insert_article(self, title, content):
		sql = ''.join([
			'INSERT INTO Article\n',
		    '(Title, Content)\n',
		    'VALUES\n',
		    f'("{title}", "{content}")\n'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of {title} failed due to {e.args[-1]}'
			)
			return False
		return True

	def insert_word(self, word, meaning, pron, exchange):
		sql = ''.join([
			'INSERT INTO Words\n',
		    '(Word, Meaning, Pronunciation, Exchange, `date`)\n',
		    'VALUES\n',
		    f'("{word}", "{meaning}", "{pron}", "{exchange}", CURDATE())'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of {word} failed due to {e.args[-1]}'
			)
			return False
		return True

	def update_article(self, title, content):
		sql = ''.join([
			f'UPDATE Article SET Content="{content}"\n',
			f'WHERE Title="{title}"'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Update of {title} failed due to {e.args[-1]}'
			)
			return False
		return True	

	def update_word(self, word, meaning, pron, exchange):
		sql = ''.join([
			f'UPDATE Words SET Meaning="{meaning}", Pronunciation="{pron}", Exchange="{exchange}", `date`=CURDATE()\n',
			f'WHERE Word="{word}"'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Update of {word} failed due to {e.args[-1]}'
			)
			return False
		return True

	def insert_usage(self, word, usage):
		sql = ''.join([
			'INSERT INTO `Usage`\n',
		    '(Word, `Usage`)\n',
		    'VALUES\n',
		    f'("{word}", "{usage}")\n'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion usage for {word} failed due to {e.args[-1]}'
			)
			return False
		return True

	def insert_article(self, title, content):
		sql = f'INSERT INTO Article (Title, Content) VALUES ("{title}", "{content}")'
		print(sql)
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of article failed due to {e.args[-1]}'
			)
			return False
		return True

	def truncate_reference(self):
		try:
			self.cursor.execute('TRUNCATE TABLE Reference')
		except Exception as e:
			self.messages.append(
				f'Truncate table Referebce failed due to {e.args[-1]}'
			)
			return False
		return True

	def insert_reference(self, word, title):
		sql = f'INSERT INTO Reference (Word, Title) VALUES ("{word}", "{title}")'
		print(sql)
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of reference {word}<->{title} failed due to {e.args[-1]}'
			)
			return False
		return True

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
				f'Deletion of {word} failed due to {e.args[-1]}'
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
				f'Deletion of {title} failed due to {e.args[-1]}'
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
	db_operator.insert_word(
		'unfathomable',
		'adj.难以理解的;莫测高深的;(表情)难以琢磨的，微妙的',
		'美 [ʌnˈfæðəməbl]',
		'exchange placeholder'
	)
	db_operator.insert_usage(
		'unfathomable',
		'Her gray eyes were dark with some unfathomable emotion'
	)
	db_operator.insert_article(
'''
THEFT
By Katherine Anne Porter
She had the purse in her hand when she came in. Standing in the middle of
the floor, holding her bathrobe around her and trailing a damp towel in
one hand, she surveyed the immediate past and remembered everything
clearly. Yes, she had opened the flap and spread it out on the bench
after she had dried the purse with her handkerchief.
'''
	)
	db_operator.print_messages()

def db_access_revert(db_operator):
	pass

if __name__ == '__main__':
	# db_operator = DbOperator()
	# db_access_test(db_operator)
	# db_access_revert(db_operator)
	# db_operator.db_close()
	pass