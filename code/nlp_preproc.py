__author__="Sasha Gutfraind"

import os, sys
import nltk

brown_tagged = nltk.corpus.brown.tagged_words(categories='fiction', tagset='universal')
cfdBrown = nltk.ConditionalFreqDist(brown_tagged)

def get_wordnet_pos(word, treebank_tag):
    wn = nltk.wordnet.wordnet
    if treebank_tag.startswith('J'):# or treebank_tag == 'CD':
        return wn.ADJ
    elif treebank_tag.startswith('V') or treebank_tag == 'MD':
        return wn.VERB
    elif treebank_tag.startswith('N'):# or treebank_tag.startswith('PR'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        brownTags = cfdBrown[word]
        if len(brownTags) == 0:
            return ''
        brownTag = brownTags.most_common()[0][0]
        #print (word, brownTag)
        if brownTag in (wn.ADJ, wn.VERB, wn.NOUN, wn.ADV):
            return brownTag
        else:
            return ''

def loadCrimeAndPunishment():
    import urllib
    #os.chdir(u'/Users/sgutfraind/nltk-learning')
    urlCrimeAndPunishment = "http://www.gutenberg.org/files/2554/2554.txt"
    rawCrimeAndPunishment = urllib.urlopen(urlCrimeAndPunishment).read()
    print len(rawCrimeAndPunishment)

    with open('data/rawCrimeAndPunishment.txt', 'w') as f:
        f.write(rawCrimeAndPunishment)


    with open('data/rawCrimeAndPunishment.txt', 'r') as f:
        rawCrimeAndPunishment = f.readlines()

    print("Remove header and footer")
    header = "On an exceptionally hot evening"
    ender  = "End of Project Gutenberg"
    rawText = rawCrimeAndPunishment[rawCrimeAndPunishment.index(header):rawCrimeAndPunishment.index(ender)-1]

    #print("Divide by chapter & do word freq analysis")
    #chapters = rawCrimeAndPunishment.split("CHAPTER")

def cleanThisText(rawText, removeProperNouns=False):
    print("Tokenize")
    tokenized = nltk.word_tokenize(rawText)
    tokenized = [w.lower() for w in tokenized if w.isalpha()]
    #list of words.
    #-punctuation is in its own element
    #-breaks up "It's" -> ["It", "'s']
    #-does not stem plurals

    print("Remove stop words")
    from nltk.corpus import stopwords
    swEn = stopwords.words('english')  #includes "don" "s".  all lowercase
    tokenized_noSW = [w for w in tokenized if w not in swEn]

    #stemmer = nltk.stem.SnowballStemmer("english")
    stemmer = nltk.stem.LancasterStemmer()
    stemmed = [stemmer.stem(w) for w in tokenized_noSW]

    if removeProperNouns:
        print("Remove proper nouns")
        text_vocab = set(w.lower() for w in stemmed if w.isalpha())
        english_vocab = set(stemmer.stem(w.lower()) for w in nltk.corpus.words.words())
        unusual = text_vocab.difference(english_vocab)
        #not completely OK.  misses girls, constitutes
        print(".. Removed %d words like: %s"%(len(unusual), str(list(unusual)[:min(len(text_vocab),20)])))
        removed_proper = [w for w in stemmed if w not in unusual]

        return removed_proper
    else:
        return stemmed

def cleanThisTextLemmatized(rawText, removeProperNouns=False):
    print("Tokenize")
    tokenized = nltk.word_tokenize(rawText)
    tokenized = [w.lower() for w in tokenized if w.isalpha()]
    #list of words.
    #-punctuation is in its own element
    #-breaks up "It's" -> ["It", "'s']
    #-does not stem plurals

    print("Remove stop words")
    from nltk.corpus import stopwords
    swEn = stopwords.words('english')  #includes "don" "s".  all lowercase
    tokenized_noSW = [w for w in tokenized if w not in swEn]

    print("Part-of-speech tagging (wait...)")
    pos_tagged = nltk.pos_tag(tokenized_noSW)
    #default tags from https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    #tag_types = set(t for (w,t) in pos_tagged)

    pos_tagged_simple = [(w, get_wordnet_pos(w, t)) for (w, t) in pos_tagged]

    #mistagged = [(w,t) for (w,t) in pos_tagged if len(t)<2]
    #this is often empty, but some common words like "young" are not tagged correctly as as "IN" etc.

    #make all nouns
    #pos_tagged_simple2 = [(w, t if t != '' else wn.NOUN) for (w, t) in pos_tagged_simple]


    #mistagged_freq = nltk.FreqDist((w,t) for (w, t) in pos_tagged_simple if t == '')
    #print(mistagged_freq.most_common())
    # #brown corpus categories:
    # # [u'mystery', u'belles_lettres', u'humor', u'government', u'fiction', u'reviews', u'religion', u'romance', u'science_fiction', u'adventure', u'editorial', u'hobbies', u'lore', u'news', u'learned']
    # brown_tagged = nltk.corpus.brown.tagged_words(categories='fiction', tagset='universal')
    # print([(w,t) for (w,t) in brown_tagged])

    #nText = nltk.Text(rawText)

    print("Lemmatize")
    wnl = nltk.WordNetLemmatizer()  #WordNet's lemmatizer
    lemmatized = [wnl.lemmatize(w, t) for (w, t) in pos_tagged_simple if t != '']

    #OLD: a lot of errors when the word could be used as an adjective
    #assert('.' not in tokenized)
    #wnl = nltk.WordNetLemmatizer()  #WordNet's lemmatizer
    #lemmatized = [wnl.lemmatize(t.lower()) for t in tokenized]  #wishlist: use POS tagger to improve this

    #leaves some noise: remembered (POS issue?), unicode versions of words

    if removeProperNouns:
        print("Remove proper nouns")
        text_vocab = set(w.lower() for w in lemmatized if w.isalpha())
        english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        unusual = text_vocab.difference(english_vocab)
        #not completely OK.  misses girls, constitutes

        removed_proper = [w for w in lemmatized if w not in unusual]

        return removed_proper
    else:
        return lemmatized

def demo():
    print("Beatles: Here comes the sun")

    # from bs4 import BeautifulSoup
    # sunUrl = "http://www.metrolyrics.com/here-comes-the-sun-lyrics-beatles.html"
    # rawText = urllib.urlopen(sunUrl).read()
    # soup = BeautifulSoup(rawText, 'html.parser')
    # print(soup.get_text())

    txt = "Here comes the sun, here comes the sun And I say it's all right Little darling, it's been a long cold lonely winter Little darling, it feels like years     since it's been here Here comes the sun, here comes the sun And I say it's all right Little darling, the smiles returning to the faces Little darling, it seems like years since it's been here Here comes the sun, here comes the sun And I say it's all right Sun, sun, sun, here it comes Sun, sun, sun, here     it comes Sun, sun, sun, here it comes Sun, sun, sun, here it comes Sun, sun    , sun, here it comes Little darling, I feel that ice is slowly melting Little darling, it seems like years since it's been clear Here comes the sun, here comes the sun And I say it's all right Here comes the sun, here comes the     sun It's all right, it's all right"
    cleaned_text = cleanThisTextLemmatized(txt)
    print("The cleaned version")
    print(set(cleaned_text))

#demo()
