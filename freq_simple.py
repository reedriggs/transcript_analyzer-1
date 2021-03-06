#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 13:18:18 2021

@author: Reed Riggs
Adapted from: https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_4.html
"""

from bs4 import BeautifulSoup
import requests

headers = "{'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'}"

#convert the original text into a python-readable tokenized list
def tokenize(input_string, url):
  tokenized = []
  source = requests.get(url, headers).text
  html = "html5lib"
  soup = BeautifulSoup(source, html)
  get_text = soup.find_all('div', attrs={'class':'tyJCtd mGzaTb baZpAe'})
  input_string = get_text[1].text
  ignore_list = [":", ".", "。", "?", "？", "!", "！", ",", "，", "、", "'", "‘", '"', "“", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
  #iterate through the punctuation list and replace each item with a space + the item
  for x in ignore_list:
    input_string = input_string.replace(x, " ")
    #then we split the string into a list
  input_string = input_string.replace("           ", "          ").replace("          ", "         ").replace("         ", "        ").replace("        ", "       ").replace("       ", "      ").replace("      ", "     ").replace("     ", "    ").replace("    ", "   ").replace("   ", "  ").replace("  ", " ")
  input_list = input_string.split(" ")
  for x in input_list:
    if x not in ignore_list: #if item is not in the ignore list
      tokenized.append(x) #add it to the list "tokenized"
  return(tokenized)

def freq_simple(tok_list):
	freq = {}
	for x in tok_list:
		if x not in freq:
			freq[x] = 1
		else:
			freq[x] += 1
	return(freq)

url1 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1a?authuser=0'
url2 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1b?authuser=0'
tokenized_list_1 = tokenize(headers, url1)
tokenized_list_2 = tokenize(headers, url2)

freq_simple_1 = freq_simple(tokenized_list_1)
freq_simple_2 = freq_simple(tokenized_list_2)
search_term = "a"
term_freq = freq_simple_1[search_term]

print(freq_simple_1)
print("\n" + "\n" + "\n")
print(freq_simple_2)
print("\n" + "\n" + "\n")
print(f'The search term "{search_term}" was found {term_freq} times.')
