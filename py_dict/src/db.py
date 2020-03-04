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
			return False		

	def insert_word(self, word, meaning, pron):
		sql = ''.join([
			'INSERT INTO Words\n',
		    '(Word, Meaning, Pronunciation, `date`)\n',
		    'VALUES\n',
		    f'("{word}", "{meaning}", "{pron}", CURDATE())\n'
		])
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of {word} failed due to {e.args[-1]}'
			)
			return False
		return True

	def update_word(self, word, meaning, pron):
		sql = ''.join([
			f'UPDATE Words SET Meaning="{meaning}", Pronunciation="{pron}", `date`=CURDATE()\n',
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
		print('sql', sql)
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion usage for {word} failed due to {e.args[-1]}'
			)
			return False
		return True

	def insert_article(self, content):
		sql = f'INSERT INTO Article (Content) VALUES ("{content}")'
		try:
			self.cursor.execute(sql)
		except Exception as e:
			self.messages.append(
				f'Insertion of article failed due to {e.args[-1]}'
			)
			return False
		return True

	def print_messages(self):
		print('here1')
		print('--- All messages ---')
		for message in self.messages:
			print(message)
		print('--- End of all messages ---')

def db_access_test(db_operator):
	db_operator.insert_word(
		'unfathomable',
		'adj.难以理解的;莫测高深的;(表情)难以琢磨的，微妙的',
		'美 [ʌnˈfæðəməbl]'
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