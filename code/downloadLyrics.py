import os,codecs,plyr,sys,re,requests
from bs4 import BeautifulSoup
from PyLyrics import *

path = '/Users/vadasg/research/songs/code/new/data/'

vendors = ['pylyrics','lyricsdotcom','plyr']


delchars = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
delchars = delchars.replace('_','')

#userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'

def checkName(s):
    return  s == '_' or s.isalnum() 


def getLyrics(artist,track,vendor):
    if vendor == 'plyr':
        query = plyr.Query(artist=artist, title=track, get_type='lyrics',timeout=1,verbosity=3,parallel=40,useragent=userAgent)
        items = query.commit()
        lyrics = items[0].data
    elif vendor == 'lyricsdotcom':
        artistF = filter(checkName, artist.replace(' ','_')).replace('_','-')
        trackF = filter(checkName, track.replace(' ','_')).replace('_','-')
        artistF = re.sub('-+','-',artistF).lower()
        trackF = re.sub('-+','-',trackF).lower()
        lyricsdotcom = 'http://www.lyrics.com/'
        lyriclink = lyricsdotcom+trackF + '-lyrics-' +artistF + '.html'
        req = requests.get(lyriclink)
        lyricsoup = BeautifulSoup(req.content)
        lyrics = lyricsoup.find_all('div',{'id':re.compile('lyric_space|lyrics')})[0].text
    elif vendor == 'pylyrics':
        lyrics = PyLyrics.getLyrics(artist,track)
    return lyrics


if __name__ == '__main__':

    y = sys.argv[1]
    f = codecs.open(path + str(y) + '/' + str(y) +'_songs.txt','r',encoding='utf-8')
    g = codecs.open(path + str(y) + '/' + str(y) +'_download_status.txt','w',encoding='utf-8')
    data = f.readlines()
    f.close()

    for line in data:
        artist = line.split('\t')[0].replace('\n','').strip().encode('ascii','ignore')
        track = line.split('\t')[1].replace('\n','').strip().encode('ascii','ignore')

        artistF = filter(checkName, artist.replace(' ','_'))
        trackF = filter(checkName, track.replace(' ','_'))

        lyricFileName = path + str(y) + '/lyrics/' + str(y) + '__' + artistF + '__' + trackF + '__lyrics.txt'

        if os.path.isfile(lyricFileName): continue 

        for v in vendors:
            try:
                lyrics = getLyrics(artist,track,v)
                if len(lyrics) > 0:
                    status = 'success'
                    l = open(lyricFileName,'w')
                    l.write(lyrics)
                    l.close()
                    continue
                else:
                    status = 'not_found'
            except:
                status = 'error'
        print artist, track, status
        g.write(line + '\t' + status + '\n')
    g.close()

