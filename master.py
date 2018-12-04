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
import io
import glob
nlp = spacy.load('en_core_web_sm') #Loading english language for Named entity recognition with spaCy
nlp.max_length = 10000000 #Increasing maximum file size to be processed

#party_names and party_manifestos were created for easier and faster manipulation of the provided data
party_names = ["Conservative Party", "Democratic Unionist Party", "Green Party of England and Wales", "Labour Party", "Liberal Democrats", "Scottish National Party", "Social Democratic and Labour Party", "The Party of Wales", "Ulster Unionist Party", "United Kingdom Independence Party", "We Ourselves"]
party_manifestos = dict()
name_counter = 0
party_manifesto_entities = []
all_parties_manifestos_entities = []

#Loading files containing each party's complete manifestos organized line by line
for filepath in glob.iglob('helpers/training_tasks/*.txt'):	
	party_manifestos[party_names[name_counter]] = io.open(filepath, 'r+').read()
	name_counter = name_counter + 1 
name_counter = 0

#Populating index, from original csv file, to be used by Whoosh Search Engine
schema = Schema(manifesto_id = TEXT(stored=True), content=TEXT(stored=True, analyzer=analysis.StandardAnalyzer(stoplist=None)), party = TEXT(stored=True), date = TEXT(stored=True), title = TEXT(stored=True))
ix = create_in("indexdir", schema)
writer = ix.writer()

csv.field_size_limit(1000000)
csvfile = open('en_docs_clean.csv', 'r',encoding="utf8")
spamreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)

for row in spamreader:
	writer.add_document(manifesto_id=row[1],content=row[0],party=row[2],date=row[3],title=row[4])
writer.commit()

print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')
#Findind each party's entities and declraring which are the most commonly used by each one and in total.
#We chose spaCy for its ease of use

# for p in party_manifestos.keys():
# 	print("The most mentioned entities by the " + p + " are:")
# 	doc = nlp(" ".join(party_manifestos.get(p).split()))
# 	for t in doc.ents:
# 		party_manifesto_entities.append(t.text)
# 		all_parties_manifestos_entities.append(t.text)
# 	print(FreqDist(party_manifesto_entities).most_common(5))
# 	print()
# 	party_manifesto_entities.clear()
# print("The most mentioned entities by all are:")
# print(FreqDist(all_parties_manifestos_entities).most_common(5))
print('****************************************************************************')
print('****************************************************************************')
print('****************************************************************************')



#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////
user_query = sys.argv[1]
ix = open_dir("indexdir")
parties = dict()
mentioned_by_others = [0,0,0,0,0,0,0,0,0,0,0]
mentions_others = [0,0,0,0,0,0,0,0,0,0,0]
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
			
			
			print(p, ': ', " ".join(party_manifestos.get(p).split()).lower().count(sub_query.lower()))
			
		print('****************************************************************************')
		

for p in party_manifestos.keys():
	for ppp in party_manifestos.keys():
		if ppp != p:
			mentioned_by_others[name_counter] = mentioned_by_others[name_counter] + " ".join(party_manifestos.get(ppp).split()).lower().count(p.lower())
	print("The " + p + " is mentioned by other parties", mentioned_by_others[name_counter], "times.")
	print()
	name_counter = name_counter + 1
name_counter = 0
print("iuyghisdughiudghiuhgiusfdhguiodsfhgiudsnjxczbhdsbgiasdgbiadgbiuaghiadsbghsagbishabfuhdsabfudsbusabfuybzubgbguydgbuyabguyadbg")
for p in party_manifestos.keys():
	for ppp in party_manifestos.keys():
		if ppp != p:
			mentions_others[name_counter] = mentions_others[name_counter] + " ".join(party_manifestos.get(p).split()).lower().count(ppp.lower())
	print("The " + p + " mentions other parties", mentions_others[name_counter], "times.")
	print()
	name_counter = name_counter + 1
name_counter = 0

#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////