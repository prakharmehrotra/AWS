import urllib2
from BeautifulSoup import BeautifulSoup
from nltk import bigrams


title = "JFK's bomber jacket sells for $570,000 at auction"


x = (title.replace(',','').replace(':','').replace("'",'').replace(';','')).split()
bg = bigrams(x)
wiki = []

for bigram in bg:
    url = 'http://en.wikipedia.org/wiki/'+bigram[0]+'_'+bigram[1]
    try:
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen(req)
        wiki.append(url)
    except urllib2.HTTPError, error:
        print "Page Does Not Exist"

print 'The wiki url for this news is: ', wiki
