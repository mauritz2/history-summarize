''' 
Reads a PDF of the book Postwar: A History of Europe Since 1945 by Tony Judt and extracts and plots the frequency of years 
'''

import PyPDF2
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = open('postwar.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
pageNum = fileReader.getNumPages()
all_years_dict = {}

def clean_text(text):
	# Removes unnecessary new lines that prevent sentence identification
	text = text.replace("\n", "")
	# Fix the hyphen character
	text = text.replace("Š", " - ")
	# Remove book title that appears on every other page
	text = text.replace("POSTWAR: A HISTORY OF EUROPE SINCE 1945", "")
	# Remove chapter titles (all caps) that appears on every other page
	text = re.sub('^[A-Z]+ *[A-Z]* *[A-Z]* *[A-Z]* *[A-Z]* *[A-Z] ', '', text)
	return text

def update_dict(frequency_dict, match):
	# Takes a dict + year and updates the counts of the relevant key
	if match in frequency_dict:
		frequency_dict[match] +=1
	else:
		frequency_dict[match] = 1
	return frequency_dict

# Generate a key for each year between 1900-2000 to be able to visualize years not specially mentioned
for i in range(1900, 2000):
	all_years_dict[i] = 0

# The main loop to scan the book for years and count their frequency
for i in range(pageNum):
	page = fileReader.getPage(i)
	text = page.extractText()
	# Without cleaning the text we will match the chapter/book title that appears on every page and contains years
	text = clean_text(text)

	# Matches a year between 1900-1999 with format "1945" followed by any special char
	# Letter s is excluded to avoid matching an entire decade in format "1950s"
	year_regex = re.compile("19[0-9]{2}[^s]")
	years = re.findall(year_regex, text)
	for match in years:
		# We get the first 4 numbers since it's a convenient way of getting rid of trailing special chars .,? etc.
		match = match[:4]
		# Unless we use int() here we get an index that contains both strings and integers and we can't visualuze
		all_years_dict = update_dict(all_years_dict, int(match))

	# Matches and adds the start and end years for mentioend ranges of years in format "1939-45" and "1914-1919"
	# The part after the ? forces the numbers after the hyphen to be 2 or 4 numbers (not 3)
	# Otherwise it will match 3-digit page numbers that appear immediately after a valid year in two cases
	# If there are four numbers after the hyphen we also make sure the year is during the 20th century
	double_year_regex = re.compile('19[0-9]{2}-(?:[0-9]{2}|19[0-9]{2})')
	double_years = re.findall(double_year_regex, text)
	for i in range(len(double_years)):
		double = double_years.pop()
		double = double.split("-")
		if len(double[1]) == 2:
			# If we've matched the 1945-47 format we add 19 to 47 to create a full year
			double[1] = ("19" + double[1])
		
		# We get the first 4 numbers since it's a convenient way of getting rid of trailing special chars .,? etc.
		match1 = double[0][:4]
		match2 = double[1][:4]
		# Unless we use int() here we get an index that contains both strings and integers and we can't visualize
		all_years_dict = update_dict(all_years_dict, int(match1))
		all_years_dict = update_dict(all_years_dict, int(match2))

# Creates a dataframe of the frequency so it can be visualized
year_df = pd.DataFrame.from_dict(all_years_dict, orient='index', columns=["Frequency"])
# Sort index so that we go from 1900-1999 ascending
year_df = year_df.sort_index(axis=0)

# Visualize the years
plt.style.use("seaborn-pastel")
g = year_df.plot(kind='area')
g.set_title("Amount of times a specific year between 1900-1999 is mentioned")
# This makes sure every other year has a label (every label gets too busy)
plt.xticks(np.arange(min(year_df.index), max(year_df.index)+1, 2.0))
plt.xticks(rotation=45)
plt.show()
