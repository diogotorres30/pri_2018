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

user_query = sys.argv[1]
ix = open_dir("indexdir")
parties = dict()
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
		if not whoosh.lang.stopwords_for_language('english').__contains__(sub_query):
			query = QueryParser("content", ix.schema).parse(sub_query)
			results = searcher.search(query,limit=None)
			for r in results:
				parties.setdefault(r["party"],[]).append(r["manifesto_id"]) 
				manifestos_results.append(r["manifesto_id"])
			# print(list(set(manifestos_results)))
			# print("Number of results:", len(list(set(manifestos_results))))
			print()
			print('Number of manifestos per party for the keyword: "', sub_query, '"')
			print('----------------------------------------------------------------------------')
			for p in parties.keys():
				print(p, ': ', len(list(set(parties.get(p)))))
			print('****************************************************************************')