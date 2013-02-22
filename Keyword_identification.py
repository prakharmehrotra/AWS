#-------------------------------------------------------------------------------
# Name:        Retreiving the unigrams/bigrams with there frequencies from database and identify top five keywords
# DataBase:    NewsFeed -> News
# Purpose:     Insight Data Science
#
# Author:      Prakhar
#
# Created:     26/01/2013
# Copyright:   (c) Prakhar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import nltk
import MySQLdb
import sys
import twitter
import httplib
import time
import os

def connect_db(host, user, passwd, db):
    try:
        return MySQLdb.connect(host, user, passwd, db)
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR]%d: %s\n" %(e.args[0], e.args[1]))
        return False

def authenticate():
    OAUTH_TOKEN="108131861-YCrWohWlYIU4a4ZAGHwRCkSfDnqA1RAeiHtE0haG"
    OAUTH_SECRET="BSIDLW8C48olLVBbwtf4sr3T5ZX6aIEEWInK9APyjM"
    CONSUMER_KEY = "p5H5F7lczyzLVSlzxSFSIA"
    CONSUMER_SECRET = "Yq8PfAKsWSENImfBNr8LUH4D5nRYViMQVEMRzSWDnHU"
    return twitter.OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

def twittersearch(query, auth=None, limit=50, lang = 'en'):
    if not auth:
        auth = authenticate()
    if limit > 100:
        print "limit %d is too large, resetting to 100" % limit
        limit = 100

    ts = twitter.Twitter(domain="search.twitter.com", auth=auth)

    sc = [] # counting number of tweets per query (bigram)
    for i in range(0, len(query)):
        temp = 0
        #print query[i]

        remaining_attempts = 3
        while True:
            try:
                print "in try block"
                res = ts.search(q=query[i],result_type="recent",rpp=limit,include_entities = 'true')
                break

            except httplib.IncompleteRead:
                print "in except block"
                remaining_attempts -=1
                time.sleep(50-10*remaining_attempts)
                if remaining_attempts == 0:
                    raise

        for tweet in res['results']:
            temp = temp + 1
        sc.append(temp)
    return sc


def tsearch_gms(cur, database):
    query_bg = []
    query_tg = []
    freq_bg = []
    freq_tg = []

    cur.execute('SELECT * FROM FILTERED_GRAMS Where Id>=1000 AND Id <10000')
    data_bg = cur.fetchall()
    nrows_bg = int(cur.rowcount)

    # searching bigrams tweets
    for i in range(0, nrows_bg):
        freq_bg.append((eval(data_bg[i][1]), int(data_bg[i][2])))
        query_bg.append((eval(data_bg[i][1]))[0] + (eval(data_bg[i][1]))[1])
    print '*** ENTEREING TWITTER SEARCH: Bigrams*****'

    tweetcount_bg = twittersearch(query_bg)

    cur.execute('SELECT * FROM FILTERED_GRAMS Where Id>=10000')
    data = cur.fetchall()
    nrows = int(cur.rowcount)

    # searching trigrams tweets
    for i in range(0, nrows):
        freq_tg.append((eval(data[i][1]), int(data[i][2])))
        #query_tg.append((eval(data[i][1]))[0] + (eval(data[i][1]))[1] + (eval(data[i][1]))[2])
        query_tg.append(eval(data[i][1]))
    print '*** ENTEREING TWITTER SEARCH: TRIGRAMS*****'
    tweetcount_tg = twittersearch(query_tg)


    return (tweetcount_bg, query_bg,freq_bg, tweetcount_tg, query_tg, freq_tg)

def main():
# MySQL connection variables
    host = 'localhost'
    user = 'root'
    passwd = ''
    db = 'NewsFeed'

    # Connecting with database
    database = connect_db(host, user, passwd, db)
    cur = database.cursor()

    # Convert from latin-1 to utf8 format
    database.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    # Reading the Ngrams from filtered ngrams list. This list has no duplicates
    (tweetcount_bg, query_bg, freq_bg, tweetcount_tg, query_tg, freq_tg) = tsearch_gms(cur, database)

    print '\n'
    print '******BI GRAMS TWEET RESULTS******'
    print tweetcount_bg
    print query_bg
    print '\n'
    print '******TRI GRAMS TWEET RESULTS******'
    print tweetcount_tg
    print query_tg

    score_bg = []
    score_bg_u = []
    for i in range(0, len(tweetcount_bg)):
        if tweetcount_bg[i] > 30:
            score_bg.append(freq_bg[i][0])   # bigram, hashtag, score
        else:
            score_bg_u.append(freq_bg[i][0])
    print '\n'
    print '****BIGRAM TWEET > 30*****'
    print score_bg

    print '\n'
    print '****BIGRAM TWEET < 30*****'
    print score_bg_u

    score_tg = []
    for i in range(0, len(tweetcount_tg)):
        if tweetcount_tg[i] > 30:
            score_tg.append(freq_tg[i][0])   # trigram, hashtag, score
    print '\n'
    print '****TRIGRAM TWEET > 30 SCORE*****'
    print score_tg


    # estimate delta based on filtered bigrams/twigrams from twitter
    delta = []
    for i in range(0, len(score_bg)):
        for j in range(0, len(score_tg)):
            x = set(score_bg[i]) & set(score_tg[j])
            if len(x)>0:
                delta.append((score_bg[i], score_tg[j], freq_bg[i][1] - freq_tg[j][1]))

    print '*****DELTA*****'
    print delta
    print '\n'
    database.close()

    final_keyword = []
    for i in range(0, len(score_bg)):
        for j in range(0, len(delta)):
            y = set(score_bg[i]) & set(delta[j][1])  # comparing bigram and trigram
            if len(y) > 1 and delta[j][2] < 2:
                final_keyword.append((delta[j][1]))
                break
            elif len(y) > 1 and delta[j][2]  >= 2:
                final_keyword.append((delta[j][0]))
                break
            elif len(y) == 1 and delta[j][2]  >= 2:
                final_keyword.append((delta[j][0]))
                break
            elif len(y) ==1 and delta[j][2]  < 2:
                final_keyword.append((delta[j][0]))
                break
            elif len(y) == 0 and j == len(delta)-1:
                final_keyword.append((score_bg[i]))

    for i in score_bg_u:
        for j in score_tg:
            y = set(i) & set(j)
            if len(y) > 1:
                final_keyword.append(i)


    print '\n'
    print '**** FINAL RECOMMENDATION ****'
    print '\n'
    print final_keyword

    word_file = 'keywords.txt'
    f = open(word_file,'w')
    for i in final_keyword:
        f.write(str(i)+"\n")



if __name__ == "__main__":
    main()