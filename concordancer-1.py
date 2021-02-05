#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 20:11:24 2021

@author: Reed Riggs
Adapted from: https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_5.html
"""

from bs4 import BeautifulSoup
import requests

headers = "{'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'}"

def tokenize(input_string, url):
  tokenized = []
  source = requests.get(url, headers).text
  html = "html5lib"
  soup = BeautifulSoup(source, html)
  get_text = soup.find_all('div', attrs={'class':'tyJCtd mGzaTb baZpAe'})
  input_string = get_text[1].text
  ignore_list = [":", ".", "。", "?", "？", "!", "！", ",", "，", "、", "'", "‘", '"', "“", "\n", "\t", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
  for x in ignore_list:
    input_string = input_string.replace(x, " ")
  input_string = input_string.replace("           ", "          ").replace("          ", "         ").replace("         ", "        ").replace("        ", "       ").replace("       ", "      ").replace("      ", "     ").replace("     ", "    ").replace("    ", "   ").replace("   ", "  ").replace("  ", " ")
  input_list = input_string.split(" ")
  for x in input_list:
    if x not in ignore_list:
      tokenized.append(x)
  return tokenized

def corpus_freq(token_list):
  freq = {}
  for x in token_list:
    if x not in freq:
      freq[x] = 1
    else:
      freq[x] += 1
  return freq

def concord(tok_list, target, nleft, nright):
  hits = [] #empty list for search hits
  for i, x in enumerate(tok_list): #iterate through token list using the enumerate function. i = list index, x = list item
    if x == target: #if the item matches one of the target items
      if i < nleft: #deal with left context if search term comes early in a text
        left = tok_list[:i] #get x number of words before the current one (based on nleft)
      else:
        left = tok_list[i-nleft:i] #get x number of words before the current one (based on nleft)
      t = x #set t as the item
      right = tok_list[i+1:i+nright+1] #get x number of words after the current one (based on nright)
      #n = "\n"
      hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words
  return(hits)

url1 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1a?authuser=0'
url2 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1b?authuser=0'

tokenized_list_1 = tokenize(headers, url1)
tokenized_list_2 = tokenize(headers, url2)

corpus_freq_1 = corpus_freq(tokenized_list_1)
corpus_freq_2 = corpus_freq(tokenized_list_2)

target_1 = "the"
target_2 = "the"

nleft = 3
nright = 5

concord_1 = concord(tokenized_list_1, target_1, nleft, nright)
concord_2 = concord(tokenized_list_2, target_2, nleft, nright)

print(concord_1)
print("\n" + "\n" + "\n")
print(concord_2)

