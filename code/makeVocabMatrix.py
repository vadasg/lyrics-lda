import re,pylab,numpy,lda,textmining,glob,pysrt,nltk,codecs,os
from nlp_preproc import *
from collections import Counter

tdm = textmining.TermDocumentMatrix()

files = glob.glob('/Users/vadasg/research/songs/code/new/data/*/lyrics/*__lyrics.txt')

print len(files)

for f in files:
    #print f
    inFile = codecs.open(f,encoding='utf-8',errors='ignore')
    text = inFile.read()
    inFile.close()
    if len(text) == 0:
        print f
        #os.remove(f)
    if 'LyricsYour' in text:
        print f
        continue
    words = cleanThisTextLemmatized(text)

    #words = textmining.simple_tokenize_remove_stopwords(text)
    #words = [word for word in words if not word in stopwords]
    cleantext = ''
    for w in words:
        cleantext += w + ' '
    #tdm.add_doc(cleantext)
    tdm.add_doc(cleantext.encode('ascii',errors='ignore'))
tdm.write_csv('matrix.csv', cutoff=3)

f = open('matrix.csv','r')
lines = f.readlines()
f.close()

f = open('vocab.csv','w')
f.write(lines.pop(0))
f.close()

f = open('matrix.csv','w')
for line in lines:
    f.write(line + '\n')
f.close()

