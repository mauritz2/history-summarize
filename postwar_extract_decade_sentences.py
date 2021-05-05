'''
Reads a PDF of the book Postwar by Tony Judt and outputs
txt files with all sentences referening a deacade, e.g. "1950s"
'''

import PyPDF2
import re
from pprint import pprint 

def clean_text(text):
	# Removed unnecessary new lines that prevent sentence identification
	text = text.replace("\n", "")
	# Fixed the hyphen character
	text = text.replace("Š", " - ")
	# Remove book title that appears on every other page
	text = text.replace("POSTWAR: A HISTORY OF EUROPE SINCE 1945", "")
	# Remove chapter titles (all caps) that appears on every other page
	text = re.sub('^[A-Z]+ *[A-Z]* *[A-Z]* *[A-Z]* *[A-Z]* *[A-Z] ', '', text)
	return text

file = open('postwar.pdf', 'rb')
fileReader = PyPDF2.PdfFileReader(file)
pageNum = fileReader.getNumPages()
# Regex that matches the full sentence that a decade appear in format "1950s"
decade_regex = re.compile('[^.]*19[4-8]0s[^.]*\.')
decade_dict = {}
write_file = open("decade_sentences.txt", "w")
for i in range(pageNum):
	page = fileReader.getPage(i) #i
	text = page.extractText()
	text = clean_text(text)
	matches = re.findall(decade_regex, text)
	if len(matches) > 0:
		for match in matches:
			write_file.write(match)
write_file.close()