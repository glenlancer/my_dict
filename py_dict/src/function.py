#!/usr/bin/python3

import re

DEBUG_FLAG = False

def is_a_word(word):
    ''' check if given word is valid '''
    chars = '^[a-zA-Z ]*$'
    return re.match(chars, word)

def escape_double_quotes(content):
    ''' escape double quotes for mysql syntax '''
    return content.replace('"', '\\"')

def combine_usage_str(usages=None):
    if usages is None:
        usages = []
    all_usage = ''
    for usage in usages:
        if all_usage != '':
            all_usage += '\n\n'
        all_usage += usage[0]
    return all_usage