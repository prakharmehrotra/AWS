import MySQLdb
import os
import sys


def connect_db(host, user, passwd):
    try:
        return MySQLdb.connect(host, user, passwd)
    except MySQLdb.Error, e:
        sys.stderr.write("[ERROR]%d: %s\n" %(e.args[0], e.args[1]))
        return False

def database_name():

    try:
        db_file = open('database_name.txt')
        db_name = db_file.readline()
        if db_name == 'NewsFeed_2':
            db_copy = 'NewsFeed_3'
        else:
            db_copy = 'NewsFeed_2'
        return db_copy
    except IOError, e:
        db_name = 'NewsFeed_2'
        return db_name


def main():
# MySQL connection variables
    host = 'localhost'
    user = 'root'
    passwd = ''
    database = connect_db(host, user, passwd)
    cur = database.cursor()

    print 'Creating database copy'

    db_copy = database_name()
    cmd = 'CREATE DATABASE IF NOT EXISTS '+ db_copy
    oss = 'mysql -u root ' + db_copy+' < NewsFeed.sql'
# creating a copy of MySQL database
    cur.execute(cmd)
    os.system("rm -r NewsFeed.sql")
    os.system("mysqldump -u root NewsFeed > NewsFeed.sql")
    os.system(oss)
    print 'NewsFeed database updated and copy created at: ', db_copy
    #database.close()

    file = open('database_name.txt','w')
    file.write(db_copy)


if __name__ == "__main__":
    main()