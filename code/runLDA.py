import re,pylab,numpy,lda,textmining,glob,pysrt,csv
from collections import Counter

with open('vocab.csv', 'rb') as f:
    reader = csv.reader(f)
    vocab = list(reader)[0]

X = numpy.loadtxt('matrix.csv',dtype='int',delimiter=',')

files = glob.glob('/Users/vadasg/research/songs/code/new/data/*/lyrics/*__lyrics.txt')

model = lda.LDA(n_topics=10, n_iter=1500, random_state=1)
model.fit(X)  # model.fit_transform(X) is also available
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 20
for i, topic_dist in enumerate(topic_word):
    topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
