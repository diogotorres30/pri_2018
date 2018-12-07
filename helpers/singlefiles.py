# SINGLEFILES.PY
# Gets training tasks or test tasks and puts each sentence in a single txt file
#

import csv
import os
import glob
import re

categories=[]
stopwords = []

# Get categories
files = glob.glob('training_tasks/*')
for f in files:
    categories.append(f.replace('training_tasks/','').replace('.txt', ''))


# Most common stopwords from sql website
stopwords= ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


for category in categories:
    file_to_open = 'test_tasks_split/' + category + '/' + category + '.txt'
    fp = open(file_to_open, 'r')
    lines = fp.readlines()
    for i in range(0,len(lines)):

        # if os.path.exists('training_tasks_single/' + category + '/1.txt'):
        #     append_write = 'a' # append if already exists
        # else:
        #     append_write = 'w+' # make a new file if not

        # file_to_write = 'training_tasks_single/' + category + '/1.txt'

        file_to_write = 'test_tasks_single/' + category + '/' + str(i) + '.txt'
        f = open(file_to_write,'w+')

        #remove stopwords
        # string_to_add = lines[i]
        # edit_string_as_list = string_to_add.split()
        # final_list = [word for word in edit_string_as_list if word not in stopwords]
        # final_string = ' '.join(final_list)

        #remove ponctuation
        # sentence_to_add = re.sub(r'[^\w\s]','',final_string)
        f.write(lines[i])

    # for i in range(len(lines) - 50,len(lines)):
    #     file_to_write = 'test_tasks_single/' + category + '/' + str(i) + '.txt'
    #     f = open(file_to_write,'w+')
    #     f.write(lines[i])
