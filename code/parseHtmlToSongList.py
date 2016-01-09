from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import re,codecs

years = range(1900,2016)

onlyRows = SoupStrainer('td')

for y in years:
    print y

    f = open('./data/' + str(y) + '/' + str(y) +'.html','r')
    g = codecs.open('./data/' + str(y) + '/' + str(y) +'_songs.txt','w',encoding='utf-8')
    data = f.read()
    f.close()

    soup = bs(data,'html.parser', parse_only=onlyRows)
    count = 0
    for s in soup:
        if '> by <' in str(s):
            data = s.get_text().replace('videoMP3','').strip().split(' by ')

            # replace specific unicode characters (circled numbers)
            track = data[0].replace(u'\u2460','').replace(u'\u2461','').replace(u'\u2462','').replace(u'\u2463','') .replace(u'\u2464','').strip()
            artist = data[1].replace('CDMP3','').strip()
            artist = artist.split('from')[0].strip()
            artist = re.sub(r'\(.*\)','',artist).strip()
            track = re.sub(r'\(.*\)','',track).strip()
            track = re.sub(r'\[.*\]','',track).strip()
            artist = re.sub(r'\[.*\]','',artist).strip()
            g.write(artist + '\t' + track +'\n')

            if '/' in artist:
                if not artist == 'M/A/R/R/S':
                    print artist
                    print track
    g.close()
            
