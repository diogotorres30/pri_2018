# GUESS.PY
# Guess the party of the input placed in the test1.txt text file.
# Change the file to test different inputs
#

import numpy as np
import sklearn
import glob
import sys
import shutil
import io
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier

category=[]

# Get categories
files = glob.glob('training_tasks/*')
for f in files:
    category.append(f.replace('training_tasks/','').replace('.txt', ''))

# Load file -> Count Vectorizer -> Tf-idf
file = load_files('training_tasks_single',encoding='latin-1',decode_error='ignore',shuffle=True)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(file.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# Classifier
clf = LinearSVC(fit_intercept=False, loss='squared_hinge', max_iter=100).fit(X_train_tfidf, file.target)

#using the classifier, open the file with the text and retreive the result
f1 = io.open('test1.txt', 'r+', encoding="utf8")
task1 = f1.read()
docs_new = [task1]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)
predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
	print('Guess: %s \n' % (file.target_names[category]))
