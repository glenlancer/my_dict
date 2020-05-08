#!/usr/bin/python3

import requests
import json
from bs4 import BeautifulSoup

class Scraper():
    def get_request_url(self):
        return 'http://www.iciba.com/{}'.format(self.word)

    def get_php_request_url(self):
        return 'http://www.iciba.com/index.php?a=getWordMean&c=search&word={}'.format(self.word)

    def get_json_text(self):
        try:
            return requests.get(self.get_php_request_url()).text
        except Exception as e:
            return ''

    def get_html_text(self):
        return requests.get(self.get_request_url()).text

    def get_info_from_php(self, word):
        self.word = word
        html = self.get_json_text()
        try:
            response = json.loads(html)
        except json.decoder.JSONDecodeError as e:
            print('A JSONDecodeError has happened', e.args[-1])
            response = {}
        return {
            'pron': self.get_pronunciation_json(response),
            'mean': self.get_meaning_json(response),
            'exchange': self.get_exchange_json(response),
            'usage': self.get_usage_json(response)
        }

    def get_usage_json(self, json_response):
        if not 'sentence' in json_response:
            return None
        usage = ''
        for sentence in json_response['sentence']:
            if usage != '':
                usage += '\n'
            usage += ''.join([
                sentence['Network_en'], '\n', sentence['Network_cn']
            ])
        return usage.strip()

    def get_exchange_json(self, json_response):
        if not 'baesInfo' in json_response or \
            not 'exchange' in json_response['baesInfo']:
            return None
        exchange = json_response['baesInfo']['exchange']
        exchange_str = ''
        for key, value in exchange.items():
            if value not in ([], ['']):
                value_str = ','.join(value)
                exchange_str += f" {key.lstrip('word_')}:{value_str}"
        return exchange_str.strip()

    def get_meaning_json(self, json_response):
        if not 'baesInfo' in json_response or \
            not 'symbols' in json_response['baesInfo']:
            return None
        if len(json_response['baesInfo']['symbols']) < 1 or \
            not 'parts' in json_response['baesInfo']['symbols'][0]:
            return None
        meaning_str = ''
        for part in json_response['baesInfo']['symbols'][0]['parts']:
            part_str = ''.join([
                part['part'],
                ','.join(part['means'])
            ])
            if meaning_str != '':
                meaning_str += ';'
            meaning_str += part_str
        return meaning_str

    def get_pronunciation_json(self, json_response):
        if not 'baesInfo' in json_response or \
            not 'symbols' in json_response['baesInfo']:
            return None
        if len(json_response['baesInfo']['symbols']) < 1:
            return None
        symbols = json_response['baesInfo']['symbols'][0]
        pron_str = ''
        if 'ph_en' in symbols:
            pron_str += ''.join(['EN:[', symbols['ph_en'], '] '])
        if 'ph_am' in symbols:
            pron_str += ''.join(['AM:[', symbols['ph_am'], '] '])
        return pron_str.strip()

    # The bs methods are not used.
    def get_info_bs(self, word):
        self.word = word
        html = self.get_html_text()
        bsoup = BeautifulSoup(html, 'lxml')
        pron = self.get_pronunciation_bs(bsoup)
        mean = self.get_meaning_bs(bsoup)
        return pron, mean

    @staticmethod
    def get_meaning_bs(bsoup):
        meaning_tag = bsoup.find(class_='base-list switch_part')
        if meaning_tag is None:
            return None
        meaning_str = ''
        for span_area in meaning_tag.find_all('span'):
            meaning_str += span_area.get_text()
        return meaning_str

    @staticmethod
    def get_pronunciation_bs(bsoup):
        pron_tag = bsoup.find(class_='base-speak')
        if pron_tag is None:
            return None
        pron_str = ''
        for span_area in pron_tag.find_all('span'):
            if span_area.span is None:
                continue
            if pron_str != '':
                pron_str += '; '
            pron_str += span_area.span.get_text()
        return pron_str

if __name__ == '__main__':
    s = Scraper()
    s.get_info_from_php('take')