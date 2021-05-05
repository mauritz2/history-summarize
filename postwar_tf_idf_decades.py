'''
Reads a folder with text files extracted by 
postwar_extract_decade_sentences.py 
and outputs the TF-IDF significance to CSV
'''

import PyPDF2
import nltk
import numpy as np
import re
import sys
import os
import csv
from nltk.corpus import stopwords
from math import log
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
np.set_printoptions(threshold=sys.maxsize)
file = open('postwar.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
filepath = os.path.dirname(os.path.abspath(__file__))+'\decade_txts'
files = os.listdir(filepath)
number_of_docs = len(files)
DF = {}
IDF = {}
TF = {}
TF_IDF = {}

def to_lowercase(words):
	return np.char.lower(words)

def remove_stopwords(words):
	# remove common words
	updated_words = []
	for word in words:
		if word not in stopwords.words('english'):
			updated_words.append(word)
	return updated_words

def remove_numbers(words):
	updated_words = []
	number_regex = re.compile('.*[0-9]+.*')
	for word in words:
		if re.match(number_regex, word) == None:
			updated_words.append(word)
	return updated_words

def remove_punctuation(words):
	updated_words = []
	symbols = ",()$'-./:;?\n"
	for word in words:
			for i in symbols:
				word = word.replace(i, "") 
			else:
				updated_words.append(word)
	return updated_words

def remove_short_words(words):
	updated_words = []
	for word in words:
		if len(word) > 2:
			updated_words.append(word)
	return updated_words

def lemmatize_words(words):
	updated_words = []
	for word in words:
		updated_words.append(lemmatizer.lemmatize(word))
	return updated_words

def preprocess(text):
	text = text.split(" ")
	text = to_lowercase(text)
	text = remove_stopwords(text)
	text = remove_numbers(text)
	text = remove_punctuation(text)
	text = lemmatize_words(text)
	text = remove_short_words(text)
	return text

# Get DF
for f in files:
	# Finds the files a word exists and then turns that into a number using len() 
	file = open(filepath + "\\" + f, 'r')
	text = file.read()
	file.close()
	processed_text = preprocess(text)
	
	for word in processed_text:
		# This if/else setup ensures that a file can only be added once per word (DF)
		if word in DF:
			DF[word].add(f)
		else:
			DF[word] = {f}

		if word in TF:
			TF[word] += 1
		else:
			TF[word] = 1
else:
	for word in DF:
		DF[word] = len(DF[word])

# Get IDF
for word in DF:
	IDF[word] = log(number_of_docs / DF[word] + 1)

# Get TF-IDF for document and write to document
for f in files:
	# Reset TF for each file since TF should be document-specific
	TF = {}
	file = open(filepath + "\\" + f, 'r')
	text = file.read()
	file.close()
	processed_text = preprocess(text)

	# Calculate the TF for this document
	for word in processed_text:
		if word in TF:
			TF[word] += 1
		else:
			TF[word] = 1
	# Calculate TF-IDF for this document and write to a CSV
	# Reset so that TF-IDF is calculated per document
	TF_IDF = {}
	for word in processed_text:
		TF_IDF[word] = TF[word] * IDF[word]
	else:
		output_filename = f.replace(".", "") + ".csv"
		output_file = open(output_filename, 'w', newline='')
		writer = csv.writer(output_file)
		writer.writerow(["Source", "Word", "TF-IDF"])
		for key, value in TF_IDF.items():
			writer.writerow([output_filename, key, value])
		output_file.close()





