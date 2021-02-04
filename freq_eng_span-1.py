#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:24:36 2021

@author: Reed Riggs
Adapted from:
    - https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_4.html
    - https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
"""

from bs4 import BeautifulSoup
import requests
import nltk
nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer

spanishStemmer = SnowballStemmer("spanish", ignore_stopwords=True)
porter = PorterStemmer()

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

def stemEnglish(text):
    stem_sentence=[]
    for word in text:
        stem_sentence.append(porter.stem(word))
    return stem_sentence

def stemSpanish(text):
    stem_sentence = []
    for word in text:
        stem_sentence.append(spanishStemmer.stem(word))
    return stem_sentence

def corpus_freq(raw_text):
  freq = {}
  for x in raw_text:
    if x not in freq:
      freq[x] = 1
    else:
      freq[x] += 1
  return freq

url1 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1a?authuser=0'
url2 = 'https://sites.google.com/view/tildatabase/the-database/english/2013enmoer/2013enmoer-more/transcript-1b?authuser=0'

tokenized_list_1 = tokenize(headers, url1)
tokenized_list_2 = tokenize(headers, url2)

lemmatized_En_list_1 = stemEnglish(tokenized_list_1)
lemmatized_En_list_2 = stemEnglish(tokenized_list_2)

lemmatized_Sp_list_1 = stemSpanish(lemmatized_En_list_1)
lemmatized_Sp_list_2 = stemSpanish(lemmatized_En_list_2)

corpus_freq_1 = corpus_freq(lemmatized_Sp_list_1)
corpus_freq_2 = corpus_freq(lemmatized_Sp_list_2)
print(corpus_freq_1)
#print(lemmatized_list_1)
print("\n" + "\n" + "\n")
print(corpus_freq_2)
#print(lemmatized_list_2)



