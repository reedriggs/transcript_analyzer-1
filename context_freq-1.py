#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:14:29 2021

@author: Reed Riggs
"""

from bs4 import BeautifulSoup
import requests
import nltk
nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
import re

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

def freq_update(tok_list,freq_dict): #this takes a list (tok_list) and a dictionary (freq_dict) as arguments
	for x in tok_list: #for x in list
		if x not in freq_dict: #if x not in dictionary
			freq_dict[x] = 1 #create new entry
		else: #else: add one to entry
			freq_dict[x] += 1
            
def context_freq(tok_list,target,nleft = 10,nright = 10):
	left_freq = {} #frequency of items to the left
	right_freq = {} #frequency of items to the right
	combined_freq = {} #combined left and right frequency
	target_freq = {} #frequency dictionary for all target hits
	corp_freq = {} #total frequency for all words

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		freq_update([x],corp_freq) #here we update the corpus frequency for all words. Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

		hit = False #set Boolean value to False - this will allow us to use a list or a regular expression as a search term
		if type(target) == str and re.compile(target).match(x) != None: #If the target is a string (i.e., a regular expression) and the regular expression finds a match in the string (the slightly strange syntax here literally means "if it doesn't not find a match")
			hit = True #then we have a search hit
		elif type(target) == list and x in target: #if the target is a list and the current word (x) is in the list
			hit = True #then we have a search hit

		if hit == True: #if we have a search hit:

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
				freq_update(left,left_freq) #update frequency dictionary for the left context
				freq_update(left,combined_freq) #update frequency dictionary for the all contexts
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)
				freq_update(left,left_freq) #update frequency dictionary for the left context
				freq_update(left,combined_freq) #update frequency dictionary for the all contexts
			t = x
			freq_update([t],target_freq) #update frequency dictionary for target hits; Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			freq_update(right,right_freq) #update frequency dictionary for the right context
			freq_update(right,combined_freq) #update frequency dictionary for the all contexts

	output_dict = {"left_freq" : left_freq,"right_freq" : right_freq, "combined_freq" : combined_freq, "target_freq" : target_freq, "corp_freq" : corp_freq}
	return(output_dict)

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
#print(corpus_freq_1)
#print(lemmatized_list_1)
#print("\n" + "\n" + "\n")
#print(corpus_freq_2)
#print(lemmatized_list_2)

#use the context_freq() function to search for collocates of "I" and "we" (with 5 words of left context and 5 words of right context)
I_freqs = context_freq(tokenized_list_1,["I"],5,5)
print(I_freqs["target_freq"]) #print the "target_freq" dictionary
print("\n|")
print(I_freqs["left_freq"]) #print the "left_freq" dictionary
print("\n|" + "\n|")
my_freqs = context_freq(tokenized_list_1,["my"],5,5)
print(my_freqs["target_freq"]) #print the "target_freq" dictionary
print("\n|")
print(my_freqs["left_freq"]) #print the "left_freq" dictionary
