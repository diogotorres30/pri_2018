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

#Loading english language for Named entity recognition with spaCy
nlp = spacy.load('en_core_web_sm') 
#Increasing maximum file size to be processed
nlp.max_length = 10000000 

#party_names and party_manifestos were created for easier and faster manipulation of the provided data
party_names = ["Conservative Party", "Democratic Unionist Party", "Green Party of England and Wales", "Labour Party", "Liberal Democrats", "Scottish National Party", "Social Democratic and Labour Party", "The Party of Wales", "Ulster Unionist Party", "United Kingdom Independence Party", "We Ourselves"]
party_manifestos = dict()
name_counter = 0
party_manifesto_entities = []
all_parties_manifestos_entities = []
print_aux = dict()

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





# print()
# print("What are the most mentioned entities for each party?")
# print('----------------------------------------------------------------------------')
# for p in party_manifestos.keys():
# 	#Discover all named entities mentioned in the manifestos. We chose spaCy for its ease of use
# 	print( p + ":")
# 	doc = nlp(" ".join(party_manifestos.get(p).split()))
# 	for t in doc.ents:
# 		party_manifesto_entities.append(t.text)
# 		all_parties_manifestos_entities.append(t.text)
# 	#What are the most mentioned entities for each party?
# 	for r in FreqDist(party_manifesto_entities).most_common(5):
# 		print(r[1],"-",r[0])
# 	print()
# 	party_manifesto_entities.clear()
# #What are the most mentioned entities globally?
# print()
# print("What are the most mentioned entities globally?")
# print('----------------------------------------------------------------------------')
# for r in FreqDist(all_parties_manifestos_entities).most_common(5):
# 		print(r[1],"-",r[0])



#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////
#Getting user query
user_query = sys.argv[1] 
#Openning previously populated and stored index folder for Whoosh Search Engine
ix = open_dir("indexdir")

parties = dict()
mentioned_by_others = [0,0,0,0,0,0,0,0,0,0,0]
mentions_others = [0,0,0,0,0,0,0,0,0,0,0]
manifestos_results = []
print()
print()
print('Return all the manifestos containing such keywords :', '"' + user_query + '"')
print('----------------------------------------------------------------------------')
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse(user_query)
	results = searcher.search(query,limit=None) #Searching for given query in our manisfestos
	for r in results:
		#For each party, how many manifestos are in the results returned
		parties.setdefault(r["party"],[]).append(r["manifesto_id"])
		#Return all the manifestos containing query
		manifestos_results.append(r["manifesto_id"])
# print(list(set(manifestos_results)))
print("Total of number of manifestos:", len(list(set(manifestos_results))))
print()
for i,item in enumerate(list(set(manifestos_results))):
    if (i+1)%5 == 0:
        print(item)
    else:
        print(item,end=' ')

print()
print()
print('For each party, how many manifestos are in the results returned?')
print('----------------------------------------------------------------------------')
for p in parties.keys():
	print_aux[p] = len(list(set(parties.get(p))))
for w in sorted(print_aux, key=print_aux.get, reverse=True):
	print(print_aux[w],':',w)
print_aux.clear()	  
print()

#////////////////////////////////////////  ALINEA a) /////////////////////////////////////////////

#How many times each party mentions each keyword
print()
print('How many times does each party mention each keyword?')
print('----------------------------------------------------------------------------')
for sub_query in user_query.split():
	#Commented line was previously used to ignore stop words to reduce the algorithm
	# if not whoosh.lang.stopwords_for_language('english').__contains__(sub_query):
	print('"' + sub_query + '"')
	for p in party_manifestos.keys():
		if(" ".join(party_manifestos.get(p).split()).lower().count(sub_query.lower()) != 0):
			print_aux[p] = " ".join(party_manifestos.get(p).split()).lower().count(sub_query.lower())
	for w in sorted(print_aux, key=print_aux.get, reverse=True):
  		print(print_aux[w],':',w)
	print_aux.clear()	  
	print()

#Which party is mentioned more times by the other parties?
print()
print("Which party is mentioned more times by the other parties?")
print('----------------------------------------------------------------------------')
for p in party_manifestos.keys():
	for ppp in party_manifestos.keys():
		if ppp != p:
			mentioned_by_others[name_counter] = mentioned_by_others[name_counter] + " ".join(party_manifestos.get(ppp).split()).lower().count(p.lower())
	print(mentioned_by_others[name_counter], ':', p)
	name_counter = name_counter + 1
name_counter = 0

#How many times does any given party mention other parties?
print()
print("How many times does any given party mention other parties?")
print('----------------------------------------------------------------------------')
for p in party_manifestos.keys():
	for ppp in party_manifestos.keys():
		if ppp != p:
			mentions_others[name_counter] = mentions_others[name_counter] + " ".join(party_manifestos.get(p).split()).lower().count(ppp.lower())
	print(mentions_others[name_counter], ':', p)
	name_counter = name_counter + 1
name_counter = 0