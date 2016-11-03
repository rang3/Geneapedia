#This script was written to take information from the 
#Wikipedia xml dumps and store it in our mySQL db.

import sys, getopt, getpass
from bs4 import BeautifulSoup
import MySQLdb
from lxml import etree
import re
#regex_search = re.search('regex', string)
#regex_search.group(0)


###############################################################
################ GLOBAL VARIABLES #############################
username = ''
password = ''
wikifile = ''
dbname = ''
db = ''         #db object, don't touch!
cursor = ''     #cursor object for the db object. don't touch!

###############################################################
##################EXPECTED RELATIONAL MODEL TABLES#############
###############################################################
#Person(PID, name, birth_date, death_date, nationality, popularity_score)
#       --- -----
#Spouse(name1, name2, date)
#       ----  ----
#Child(parent_name, child_name)
#      -----------  ----------
#Alma_mater(name, university)

def getPassword():
    password = getpass.getpass('enter password: ')
    return password

def parseFile(wikifile):
    filestream = open(wikifile, 'r')
    for line in filestream:
        if "<page>" in line:
            #print "new page"
            title = "no name"
            PID = "no ID"
            while "</page>" not in line:    #for each page 
                if "<title>" in line:       #find the title
                    title = re.search('(?<=<title>)(.*)(?=</title>)' , line).group(0) 
                if "<id>" in line:
                    PID = re.search('(?<=<id>)(.*)(?=</id>)',line).group(0)
                if "{{infobox person" in line:#if there is an infobox person, then this is a person
                    infobox = re.search('{{infobox person(.*)', line).group(0).rstrip('\n').rstrip('\r');
                    left_bracket = infobox.count('{')
                    right_bracket = infobox.count('}')
                    line = filestream.next().rstrip('\n').rstrip('\r')
                    while left_bracket != right_bracket:
                        infobox += line
                        left_bracket += line.count('{')
                        right_bracket += line.count('}')
                        line = filestream.next().rstrip('\n').rstrip('\r')

                    print title
                    print PID
                    print infobox
                            
                line = filestream.next().rstrip('\n').rstrip('\r')

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hu:pi:", [])
    except getopt.GetoptError:
        print('script.py -u <username> -p -i <input>')
        sys.exit()

    for opt, arg in opts:
        if opts == []:
            print('script.py -u <username> -p -i <input>')
            sys.exit()
        if opt == '-h':
            print('script.py -u <username> -p -i <input>')
            sys.exit()
        if opt == '-u':
            username = arg
        if opt == '-p':
            password = getPassword()
        if opt == '-i':
            wikifile = arg

    global dbname 
    dbname = raw_input("enter db name: ") 
    global db 
    db = MySQLdb.connect("127.0.0.1", username, password, dbname)
    global cursor 
    cursor = db.cursor()

    parseFile(wikifile)

    db.commit()     #commit changes to db
    db.close()      #close the connection

if __name__ == "__main__":
    main(sys.argv[1:])

