import sys
import math
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import csv
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh.fields import *
import whoosh.lang
import nltk
from nltk.probability import FreqDist
import spacy
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 10000000
import io
f1 = io.open('helpers/training_tasks/WeOurselves/WeOurselves.txt', 'r+', encoding="utf8")
ladida = f1.read()
print(ladida.split())
# schema = Schema(manifesto_id = TEXT(stored=True), content=TEXT(stored=True, analyzer=analysis.StandardAnalyzer(stoplist=None)), party = TEXT(stored=True), date = TEXT(stored=True), title = TEXT(stored=True))
# ix = create_in("indexdir", schema)
# writer = ix.writer()
text_in_list_form = []
firstline = True
csv.field_size_limit(1000000)
csvfile = open('en_docs_clean.csv', 'r',encoding="utf8")
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
party_manifestos = dict()
for row in spamreader:
	if firstline:
		firstline = False
		continue
	if row[2] not in party_manifestos:
		party_manifestos[row[2]] = row[0]
	else:
		party_manifestos[row[2]] = party_manifestos.get(row[2]) + " " + row[0]
	

	# writer.add_document(manifesto_id=row[1],content=row[0],party=row[2],date=row[3],title=row[4])
# writer.commit()
# doc = nlp(party_manifestos.get("We Ourselves"))
# # print(doc.ents)
# for t in doc.ents:
# 	text_in_list_form.append(t.text)
# print(FreqDist(text_in_list_form).most_common(5))
# fdist1 = FreqDist(party_manifestos["We Ourselves"].split())
# print(fdist1.most_common(5))

print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')
for p in party_manifestos.keys():
	print(p)
# 	# print(party_manifestos.get(p))
	doc = nlp(party_manifestos.get(p))
	for t in doc.ents:
		text_in_list_form.append(t.text)
	print(FreqDist(text_in_list_form).most_common(5))
	text_in_list_form.clear()
# 	# for entity in doc.ents:
# 	# 	print(entity.text, entity.label_)
print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')

#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////
user_query = sys.argv[1]
ix = open_dir("indexdir")
parties = dict()
parties2 = dict()
manifestos_results = []
print()
print()
print('Results for query: "', user_query,'"')
print('----------------------------------------------------------------------------')
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse(user_query)
	results = searcher.search(query,limit=None)
	for r in results:
		parties.setdefault(r["party"],[]).append(r["manifesto_id"]) 
		manifestos_results.append(r["manifesto_id"])
	print(list(set(manifestos_results)))
	print("Total of number of manifestos:", len(list(set(manifestos_results))))
	print('****************************************************************************')
	print()
	print('Number of manifestos per party in results')
	print('----------------------------------------------------------------------------')
	for p in parties.keys():
		print(p, ': ', len(list(set(parties.get(p)))))
	print('****************************************************************************')
	print()
	print('/////////////////////////////////////////////////////////////////////////////')
	print()
	# print(user_query.split())
	########################################################################################
	for sub_query in user_query.split():
		# if not whoosh.lang.stopwords_for_language('english').__contains__(sub_query):
		# query = QueryParser("content", ix.schema).parse(sub_query)
		# results = searcher.search(query,limit=None)
		# for r in results:
		# 	if parties2.get(r["party"]) is None:
		# 		parties2[r["party"]] = 0 + r["content"].lower().count(sub_query.lower())
		# 	else:
		# 		parties2[r["party"]] = parties2.get(r["party"]) + r["content"].lower().count(sub_query.lower())
		print()
		print('Number of manifestos per party for the keyword: "', sub_query, '"')
		print('----------------------------------------------------------------------------')
		for p in party_manifestos.keys():
			print(p, ': ', party_manifestos.get(p).lower().count(sub_query.lower()))
		print('****************************************************************************')
		parties2.clear()
#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////