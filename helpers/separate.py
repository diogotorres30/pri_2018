# SEPARATE.PY
# Picks the main csv file and distributes it in folders with a text file
# filed with the text from the parties
#

import csv
import os
import glob

files = glob.glob('training_tasks/*')
for f in files:
    os.remove(f)

csv.field_size_limit(1000000)
csvfile = open('../en_docs_clean.csv', 'r',encoding="utf-8")
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
for row in spamreader:
	file_to_open = 'training_tasks/' + row[2].replace(" ", "") + '/' + row[2].replace(" ", "") + '.txt'

	if not os.path.exists('training_tasks/' + row[2].replace(" ", "")):
    		os.makedirs('training_tasks/' + row[2].replace(" ", ""))

	file = open(file_to_open, "a")  # a for append instead of w for write
	file.write(row[0] + '\n')
	file.close()

# os.remove("training_tasks/party")
