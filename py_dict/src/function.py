#!/usr/bin/python3

import re

def is_a_word(word):
    ''' check if given word is valid '''
    chars = '^[a-zA-Z ]*$'
    return re.match(chars, word)

def escape_double_quotes(content):
	return content.replace('"', '\\"')
