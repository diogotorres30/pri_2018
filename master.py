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
import glob
import re
party_names = ["Conservative Party", "Democratic Unionist Party", "Green Party of England and Wales", "Labour Party", "Liberal Democrats", "Scottish National Party", "Social Democratic and Labour Party", "The Party of Wales", "Ulster Unionist Party", "United Kingdom Independence Party", "We Ourselves"]
party_manifestos = dict()
name_counter = 0

for filepath in glob.iglob('helpers/training_tasks/*.txt'):	
	party_manifestos[party_names[name_counter]] = io.open(filepath, 'r+').read()
	name_counter = name_counter + 1 
name_counter = 0
for p in party_manifestos.keys():
	print(p)
# schema = Schema(manifesto_id = TEXT(stored=True), content=TEXT(stored=True, analyzer=analysis.StandardAnalyzer(stoplist=None)), party = TEXT(stored=True), date = TEXT(stored=True), title = TEXT(stored=True))
# ix = create_in("indexdir", schema)
# writer = ix.writer()
text_in_list_form = []
big_boy = []
firstline = True
csv.field_size_limit(1000000)
csvfile = open('en_docs_clean.csv', 'r',encoding="utf8")
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
# 	writer.add_document(manifesto_id=row[1],content=row[0],party=row[2],date=row[3],title=row[4])
# writer.commit()

print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')
for p in party_manifestos.keys():
	print("The most mentioned entities by the " + p + " are:")
	doc = nlp(" ".join(party_manifestos.get(p).split()))
	for t in doc.ents:
		text_in_list_form.append(t.text)
		big_boy.append(t.text)
	print(FreqDist(text_in_list_form).most_common(5))
	print()
	text_in_list_form.clear()
print("The most mentioned entities by all are:")
print(FreqDist(big_boy).most_common(5))
print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')



#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////
user_query = sys.argv[1]
ix = open_dir("indexdir")
parties = dict()
mentioned_by_others = [0,0,0,0,0,0,0,0,0,0,0,0]
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
	########################################################################################
	for sub_query in user_query.split():
		# if not whoosh.lang.stopwords_for_language('english').__contains__(sub_query):
		print()
		print('Number of manifestos per party for the keyword: "', sub_query, '"')
		print('----------------------------------------------------------------------------')
		for p in party_manifestos.keys():
			for ppp in party_manifestos.keys():
				if ppp != p:
					mentioned_by_others[name_counter] = mentioned_by_others[name_counter] + " ".join(party_manifestos.get(ppp).split()).lower().count(p.lower())
			
			print(p, ': ', " ".join(party_manifestos.get(p).split()).lower().count(sub_query.lower()))
			name_counter = name_counter +1
		print('****************************************************************************')
		name_counter = 0
		
	print(mentioned_by_others)
#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////