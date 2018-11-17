import numpy as np
import sklearn
import glob

category=[]

files = glob.glob('training_tasks/*')
for f in files:
    category.append(f.replace('training_tasks/','').replace('.txt', ''))
        
print(category)

from sklearn.datasets import load_files
file = load_files('training_tasks',encoding='latin-1',decode_error='ignore',shuffle=True,random_state=42)



from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(file.data)
X_train_counts.shape

# print(X_train_counts)
# print(X_train_counts.shape)

from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# #classifier
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, file.target)

from sklearn.pipeline import Pipeline

from sklearn.linear_model import SGDClassifier


from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
	                     ('tfidf', TfidfTransformer()),
	                     ('clf', MultinomialNB()),
])

text_clf = text_clf.fit(file.data, file.target)
#_ = text_clf.fit(file.data, file.target)
docs_test = file.data

import shutil
import io

f1 = io.open('test1.txt', 'r+', encoding="latin-1")
# f2 = io.open('teste2.txt', 'r+', encoding="latin-1")
# f3 = io.open('teste3.txt', 'r+', encoding="latin-1")
# f4 = io.open('teste4.txt', 'r+', encoding="latin-1")
# f5 = io.open('teste5.txt', 'r+', encoding="latin-1")
# f6 = io.open('teste6.txt', 'r+', encoding="latin-1")

task1 = f1.read()
# task2 = f2.read()
# task3 = f3.read()
# task4 = f4.read()
# task5 = f5.read()
# task6 = f6.read()

docs_new = [task1]

X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)

task_number=1
for doc, category in zip(docs_new, predicted):
 	number_str = str(task_number)
 	print("Task number " + number_str + ":")
	
 	print('%s \n' % (file.target_names[category]))
 	task_number= task_number + 1

# #print(docs_new[0]) 

#docs_new = ['will not put the broader']
	
#predicted = text_clf.predict(docs_new[0])

#print(predicted)

