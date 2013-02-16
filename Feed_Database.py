#-------------------------------------------------------------------------------
# Name:        Collecting Feed from the News Channels and Storing them in Database
# DataBase:    NewsFeed -> News
# Purpose:     Insight Data Science
#
# Author:      Prakhar
#
# Created:     26/01/2013
# Copyright:   (c) Prakhar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import feedparser
import nltk
import MySQLdb
import sys

# Function to connect to database
def connect_db(host, user, passwd, db):
    try:
        return MySQLdb.connect(host, user, passwd, db)
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR]%d: %s\n" %(e.args[0], e.args[1]))
        return False


# Function to create database
def create_database(cur):
    cur.execute('CREATE DATABASE IF NOT EXISTS NewsFeed')
    cur.execute('USE NewsFeed')
    cur.execute("DROP TABLE IF EXISTS News")
    cur.execute('''CREATE TABLE News(
                        NewsId int  NOT NULL AUTO_INCREMENT,
                        Source VARCHAR(70),
                        Title VARCHAR(300),
                        Link VARCHAR(300),
                        Summary VARCHAR(500),
                        TimeStamp VARCHAR(50),
                        PRIMARY KEY (NewsId)
                        )
                    ''')
    print "DATABASE CREATED"



# Function which retrieves the news feeds and stores in database
def returnStories(url_p,cur,database):
    df_title = []
    df_link = []
    df_source = []
    df_summary = []
    df_date = []
    df = feedparser.parse(url_p)

    for i in range(0,15):
        print i
        print url_p
        print '**********\n'
        df_source.append((df.feed.title).replace('"', '\''))
        df_title.append((df.entries[i].title).replace('"', '\''))
        df_link.append(df.entries[i].link)
        df_summary.append((nltk.clean_html(df.entries[i].summary)).replace('"', '\''))
        df_date.append(df.entries[i].updated)
        cur.execute("""INSERT INTO News (Source, Title, Link, Summary, TimeStamp) VALUES("%s", "%s", "%s", "%s", "%s")""" %(df_source[i], df_title[i], df_link[i], df_summary[i], df_date[i]))

    database.commit()

# Main Function
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
    create_database(cur)

# Read URLs, retrieve stories and store it in database
    file = open("URLs.txt")
    url_s = file.readlines()
    for k in url_s:
        k = k.strip('\n').strip('\r').replace('\'','')
        returnStories(k,cur,database)
    file.close()

    database.close()
if __name__ == "__main__":
    main()