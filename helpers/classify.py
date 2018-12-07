# CLASSIFY.PY
# The classifiers are built in this file and retreive the results of
# precision accuracy f1 and confusion matrix
#

import numpy as np
import sklearn
import glob
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron


# Retrives the categories used
category=[]
files = glob.glob('training_tasks/*')
for f in files:
    category.append(f.replace('training_tasks/','').replace('.txt', ''))


# Not the best function name, but that's what it does
# It uses the classifier from the pipeline and gives us the results
def spit_results(text_clf,docs_test,file_test,file,classifier):
    text_clf.fit(file.data, file.target)
    predicted = text_clf.predict(docs_test)

    print(classifier + ':')
    # print(predicted)
    # print(np.mean(predicted == file_test.target))
    print(metrics.classification_report(file_test.target, predicted, target_names=file_test.target_names))
    print(metrics.confusion_matrix(file_test.target, predicted))


# Load files to be treated
file = load_files('training_tasks_single',encoding='latin-1',decode_error='ignore',shuffle=True)
file_test = load_files('test_tasks_single',encoding='latin-1',decode_error='ignore',shuffle=True)
docs_test = file_test.data

#
# Multinomial Naive Bayes
#
text_clf = Pipeline([
     ('tfidf', TfidfVectorizer(lowercase=False, sublinear_tf=True, ngram_range=(1,2))),
     ('clf', MultinomialNB()),
])

spit_results(text_clf,docs_test,file_test,file,'MultinomialNB')

#
# Stochastic Gradient Descent """stopwords='english'"""
#
text_clf = Pipeline([
     ('tfidf', TfidfVectorizer(lowercase=False, sublinear_tf=True, ngram_range=(1,2))),
     ('clf', SGDClassifier(average=True, early_stopping=True,
           l1_ratio=0.15, learning_rate='optimal', shuffle=True))
])

spit_results(text_clf,docs_test,file_test,file,'SGDClassifier')

#
# Linear Support Vector Classification
#
text_clf = Pipeline([
     ('tfidf', TfidfVectorizer(lowercase=False, sublinear_tf=True, ngram_range=(1,2))),
     ('clf', LinearSVC(fit_intercept=False, loss='squared_hinge', max_iter=100)),
])

spit_results(text_clf,docs_test,file_test,file,'LinearSVC')


#
# Perceptron
#
text_clf = Pipeline([
     ('tfidf', TfidfVectorizer(lowercase=False, sublinear_tf=True, ngram_range=(1,2))),
     ('clf', Perceptron()),
])

spit_results(text_clf,docs_test,file_test,file,'Perceptron')
