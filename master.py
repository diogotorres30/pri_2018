import sys
import math
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh.fields import *
# schema = Schema(manifesto_id = TEXT(stored=True), content=TEXT, party = TEXT(stored=True), date = TEXT(stored=True), title = TEXT(stored=True))
# ix = create_in("indexdir", schema)
# writer = ix.writer()

# firstline = True
# csv.field_size_limit(1000000)
# csvfile = open('en_docs_clean.csv', 'r',encoding="utf8")
# spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
# for row in spamreader:
# 	if firstline:
# 		firstline = False
# 		continue
# 	print(row[1])
# 	writer.add_document(manifesto_id=row[1],content=row[0],party=row[2],date=row[3],title=row[4])
# writer.commit()

user_query = ' '.join(sys.argv[1:])
ix = open_dir("indexdir")
parties = dict()
print()
print('Results for query:', user_query)
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema, group=OrGroup).parse(user_query)
	results = searcher.search(query,limit=100)
	for r in results:
		parties.setdefault(r["party"],[]).append(r["manifesto_id"]) 
		print(r["manifesto_id"])
	print("Number of results:", results.scored_length())
	print()
	print('****************************************************************************')
	print('Number of manifestos per party in results')
	print('****************************************************************************')
	for p in parties.keys():
		print(p, ': ', len(list(set(parties.get(p)))))	


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