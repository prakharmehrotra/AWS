#-------------------------------------------------------------------------------
# Name:        Retreiving the news from the database and finding most frequent occuring words
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
import ast


# More stopwords list
stopwords_list2 = ['a','able','about','across','after','all','almost','also','am','among',
             'an','and','any','are','as','at','be','because','been','but','by','can',
             'cannot','could','comes','dear','did','do','does','done','either','else','ever','every',
             'for','from','go','get','goes','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','man','may','me','might','most','must','my','neither','new','no','nor',
             'not','of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','still','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yes','yet','you','your', '(video)',
             'huffpost', 'tastemakers', 'video', '&', 'near', 'seems', 'video', 'first']



# Function to connect to database
def connect_db(host, user, passwd, db):
    try:
        return MySQLdb.connect(host, user, passwd, db)
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR]%d: %s\n" %(e.args[0], e.args[1]))
        return False

def join_titles(cur):
    join = []
    cur.execute('SELECT * FROM News')
    data = cur.fetchall()
    nrows = int(cur.rowcount)
    for i in range(0, nrows):
        join.extend(data[i][2].split())
    from nltk.corpus import stopwords
    join_lower = map(str.lower, join)
    filtered_words = [w for w in join_lower if w not in stopwords.words('english')]
    filtered_words = [w for w in filtered_words if w not in stopwords_list2]
    return filtered_words

def count(words):
    words_u = []
    for i in range(0, len(words)):
        words_u.append(words[i].replace(':','').replace("'",''))

    from collections import Counter
    cnt = Counter(words_u).most_common(50)
    return cnt

# Writing keywords and there frequency in new table called Keywords
def saving_in_db_ug(unigrams,cur, database):
    sum = 0
    for i in range(0, len(unigrams)):
        sum = sum + unigrams[i][1]

    w = 1.0; #weight
    cur.execute('USE NewsFeed')
    cur.execute("DROP TABLE IF EXISTS Unigrams")
    cur.execute('''CREATE TABLE IF NOT EXISTS Unigrams(
                    Id int NOT NULL AUTO_INCREMENT,
                    Word VARCHAR(50),
                    Freq int,
                    Score float(4, 3),
                    PRIMARY KEY(Id)
                    )
                ''')
    for i in range(0, len(unigrams)):
        cur.execute("""INSERT INTO Unigrams (Word, Freq, Score) VALUES("%s", "%s", "%s")""" %(unigrams[i][0], unigrams[i][1], unigrams[i][1]*w/sum))
    database.commit()

def saving_in_db_bg(keywords_bgrams,cur, database):
    sum = 0
    for i in range(0, len(keywords_bgrams)):
        sum = sum + keywords_bgrams[i][1]

    w = 2.0; #weight
    cur.execute('USE NewsFeed')
    cur.execute("DROP TABLE IF EXISTS Bigrams")
    cur.execute('''CREATE TABLE IF NOT EXISTS Bigrams(
                    Id int NOT NULL AUTO_INCREMENT,
                    Word VARCHAR(100),
                    Freq int,
                    Score float(4,3),
                    PRIMARY KEY(Id)
                    )AUTO_INCREMENT = 1000
                ''')
    for i in range(0, len(keywords_bgrams)):
        cur.execute("""INSERT INTO Bigrams (Word, Freq, Score) VALUES("%s", "%s", "%s")""" %(keywords_bgrams[i][0], keywords_bgrams[i][1],keywords_bgrams[i][1]*w/sum))
    database.commit()

def saving_in_db_tg(keywords_trigrams,cur, database):
    sum = 0
    for i in range(0, len(keywords_trigrams)):
        sum = sum + keywords_trigrams[i][1]

    w = 4.0 #weight
    cur.execute('USE NewsFeed')
    cur.execute("DROP TABLE IF EXISTS Trigrams")
    cur.execute('''CREATE TABLE IF NOT EXISTS Trigrams(
                    Id int NOT NULL AUTO_INCREMENT,
                    Word VARCHAR(100),
                    Freq int,
                    Score float(4, 3),
                    PRIMARY KEY(Id)
                    )AUTO_INCREMENT = 10000
                ''')
    for i in range(0, len(keywords_trigrams)):
        cur.execute("""INSERT INTO Trigrams (Word, Freq, Score) VALUES("%s", "%s", "%s")""" %(keywords_trigrams[i][0], keywords_trigrams[i][1],keywords_trigrams[i][1]*w/sum))
    database.commit()

def remove_duplicate(word):
    s = set()
    for i in word:
        if not s.intersection(i):
            yield i
            s.update(i)

def duplicates(list_tobe_corrected):
    temp = []
    for i in range(0, len(list_tobe_corrected)):
        temp.append(list_tobe_corrected[i][0])
    dup = remove_duplicate(temp)
    return list(dup)

def updated_table(cur, database,updated_list_bgrams, updated_list_trigrams, keywords_ugms):
    cur.execute('USE NewsFeed')
    cur.execute('DROP TABLE IF EXISTS FILTERED_GRAMS')
    cur.execute('''CREATE TABLE IF NOT EXISTS FILTERED_GRAMS(
                    Id int NOT NULL AUTO_INCREMENT,
                    Word VARCHAR(100),
                    Freq int,
                    Score float(4, 3),
                    PRIMARY KEY(Id)
                    )

                ''')
    n_feeds = 40
    for i in range(0, n_feeds):
        #print keywords_ugms[i][0]
        cur.execute('''INSERT INTO FILTERED_GRAMS SELECT * FROM Unigrams WHERE Word = ("%s")''' %(str(keywords_ugms[i][0])))
    database.commit()

    for i in range(0, len(updated_list_bgrams)):
        print updated_list_bgrams[i]
        cur.execute('''INSERT INTO FILTERED_GRAMS SELECT * FROM Bigrams WHERE Word = ("%s")''' %(str(updated_list_bgrams[i])))
    database.commit()

    for i in range(0, len(updated_list_trigrams)):
        #print updated_list_trigrams[i]
        cur.execute('''INSERT INTO FILTERED_GRAMS SELECT * FROM Trigrams WHERE Word = ("%s")''' %(str(updated_list_trigrams[i])))
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

    # Counting frequency of unigram and saving them
    filter_words = join_titles(cur)
    keywords_ugms = count(filter_words)
    print 'Keywords in Trending News\n', keywords_ugms
    saving_in_db_ug(keywords_ugms, cur, database)

    # Generating Bigrams, counting and saving them
    from nltk import bigrams
    from collections import Counter
    lists = []
    for i in range(0, len(filter_words)):
        lists.append(filter_words[i].replace(':','').replace("'",'').replace(',',''))
    bgrams = bigrams(lists)
    keywords_bgrams = Counter(bgrams).most_common(50)
    print 'Bigrams Keywords in Trending News\n', keywords_bgrams
    saving_in_db_bg(keywords_bgrams, cur, database)

    # Generating Trigrams, counting and saving them
    from nltk import trigrams
    trigrams = trigrams(lists)
    keywords_trigrams = Counter(trigrams).most_common(50)
    print 'Trigrams Keywords in Trending News\n', keywords_trigrams
    saving_in_db_tg(keywords_trigrams, cur, database)


    # Removing duplicates
    updated_list_bgrams = duplicates(keywords_bgrams)
    updated_list_trigrams = duplicates(keywords_trigrams)

    # creating updated table
    updated_table(cur, database, updated_list_bgrams, updated_list_trigrams, keywords_ugms)
    database.close()

if __name__ == "__main__":
    main()