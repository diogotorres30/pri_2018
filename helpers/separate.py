import csv
import os
import glob

files = glob.glob('training_tasks/*')
for f in files:
    os.remove(f)

csv.field_size_limit(1000000)
csvfile = open('../en_docs_clean.csv', 'r')
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
for row in spamreader:
	file_to_open = 'training_tasks/' + row[2].replace(" ", "") + '.txt'
	file = open(file_to_open, "a")  # a for append instead of w for write
	file.write(row[0] + '\n') 
	file.close() 

os.remove("training_tasks/party.txt")