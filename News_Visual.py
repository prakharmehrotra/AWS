#!/usr/bin/env python

import os
import flask
from flask import Flask
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import url_for
import MySQLdb
import sys
import urllib2
from nltk import bigrams



# MySQL connection variables
host = 'localhost'
user = 'root'
passwd = ''
db = 'NewsFeed'

def connect_db(host, user, passwd, db):
    try:
        return MySQLdb.connect(host, user, passwd, db,charset='utf8', use_unicode=True)
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR]%d: %s\n" %(e.args[0], e.args[1]))
        return False


# Connecting with database
database = connect_db(host, user, passwd, db)
cur = database.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    file = open('keywords.txt')
    f = file.readlines()
    keyword = []
    for i in f:
        keyword.append(eval(i))

    key = []
    news_list = []
    wiki = []
    wiki_url = str('http://en.wikipedia.org/wiki/')


    for j in range(0, len(keyword)):
        q = '%'+str(keyword[j][0])+' '+str(keyword[j][1])+'%'
        #print q
        cur.execute('''select Distinct Title, Source, Summary, Link, Timestamp from News where Title like ("%s") group by Title limit 5''' %q)
        data_news = cur.fetchall()
        #print '******'
        #print len(data_news)
        if len(data_news) == 0:
            q1 = '%'+str(keyword[j][0])+'%'
            cur.execute('''select Distinct Title, Source, Summary, Link, Timestamp from News where Title like ("%s") group by Title limit 5''' %q1)
            data_news1 = cur.fetchall()
            q2 = '%'+str(keyword[j][1])+'%'
            cur.execute('''select Distinct Title, Source, Summary, Link, Timestamp from News where Title like ("%s") group by Title limit 5''' %q2)
            data_news2 = cur.fetchall()
            if ((len(data_news1)!= 0 and len(data_news2)!=0) and (len(data_news2)>len(data_news1))):
                data_news = data_news2

            elif ((len(data_news1) != 0 and len(data_news2)!=0) and (len(data_news2)<=len(data_news1))):
                data_news = data_news1
            else:
                continue


            key.append((str(keyword[j][0])+' '+str(keyword[j][1])).title())
            #news_list.append( [[thing.replace('\x97',"'") for thing in item] for item in data_news])#   (data_news).replace('\x92',"'"))
            news_list.append(data_news)
            temp_wiki = wiki_url + (str(keyword[j][0])+'_'+str(keyword[j][1])).title()
            wiki.append(temp_wiki)
        else:
            key.append((str(keyword[j][0])+' '+str(keyword[j][1])).title())
            news_list.append(data_news)
            temp_wiki = wiki_url + (str(keyword[j][0])+'_'+str(keyword[j][1])).title()
            wiki.append(temp_wiki)

    #print "News List: ", news_list
    print '######## ENTERING UNIQUENESS TESTING#######'
    print 'Key is:',key
    # comparing the uniqueness in the news
    u = []
    for m in range(0, len(key)-1):
        for n in range(m+1, len(key)):
            if news_list[m][0][0] == news_list[n][0][0]:
                print 'Match found at:', m, 'and at n = ', n
                u.append(n)

    u.sort()
    c = 0
    for i in range(0, len(u)):
        if (u[i] < 7):
            j = key.pop(u[i]-c)
            news_list.pop(u[i]-c)
            wiki.pop(u[i]-c)
            print j
            c = c+1

    # Creating a meaningful wiki recommendation
    w = []
    for i in range(0, 7):
        url = wiki[i]
        try:
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            con = urllib2.urlopen(req)
            w.append(url)
        except urllib2.HTTPError, error:
            try:
                x = (key[i].lower()).split()
                url = 'http://en.wikipedia.org/wiki/'+ x[0]+'_'+x[1]
                req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
                con = urllib2.urlopen(req)
                w.append(url)
            except urllib2.HTTPError,e:
                w.append(url)


    return render_template('News_Visual.html', key = key, news_list = news_list, wiki = w)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 8080))
    app.debug = True
    #app.run(host='192.168.1.33', port=5000)
    app.run(host='0.0.0.0', port=8080)
