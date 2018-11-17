import sys
import math
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
#from whoosh.index import create_in
#from whoosh.fields import *
#schema = Schema(id = NUMERIC(stored=True), content=TEXT)
#ix = create_in("indexdir", schema)

csv.field_size_limit(1000000)
csvfile = open('en_docs_clean.csv', 'r',encoding='latin-1')
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
for row in spamreader:
	print(row)

query = sys.argv

print(query)

# file_content = doc.readlines()
# document_length = len(file_content)

# cv = CountVectorizer()
# cv_fit=cv.fit_transform(file_content)

# print(cv.get_feature_names())
# print(cv_fit.toarray())

# words = cv.get_feature_names()
# words_in_docs = cv_fit.toarray()
# count_dic = {}
# singular_terms = []
# inverted_array = {}

# # arranje array in {word : number of files where word is present}
# for i in range(len(words)):
# 	occurence_array = []
# 	count = 0
# 	min_frequency = 1000
# 	max_frequency = 0
# 	for number in range(document_length):
# 		if words_in_docs[number][i] > 0:
# 			count += 1
# 			occurence_array.append([number,words_in_docs[number][i]])


# 		# Max term frequency
# 		if words_in_docs[number][i] > max_frequency:
# 			max_frequency = words_in_docs[number][i]

# 		if words_in_docs[number][i] < min_frequency:
# 			min_frequency = words_in_docs[number][i]
			
	
# 	# For singular terms
# 	if count == 1:
# 		singular_terms.append(words[i])
		

# 	count_dic[words[i]] = [count, min_frequency, max_frequency]
# 	inverted_array[words[i]] = occurence_array


# print (count_dic)

# print("Existing documents:" ,document_length)
# print("Existing terms:" ,len(count_dic))
# print("Existing singular terms:", len(singular_terms))


# query_word = sys.argv[1]
# if query_word:
# 	print ("\n\nQuery word", query_word)
# 	print ("Document frequency: ",count_dic[query_word][0])
# 	print ("Min term frequency: ",count_dic[query_word][1])
# 	print ("Max term frequency: ",count_dic[query_word][2])
# 	print ("Inverted Document Frequency: ", math.log10((document_length / count_dic[query_word][0])))


# A = {}


# print(inverted_array)