#!/usr/bin/python3

import re

DEBUG_FLAG = True

def is_a_word(word):
    ''' check if given word is valid '''
    chars = '^[a-zA-Z ]*$'
    return re.match(chars, word)

def escape_double_quotes(content):
	''' escape double quotes for mysql syntax '''
	return content.replace('"', '\\"')
