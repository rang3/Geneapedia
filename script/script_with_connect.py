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
                    title = re.search('(?<=<title>)(.*)(?=</title>)' , line) 
                if "<id>" in line:
                    PID = re.search('(?<=<id>)(.*)(?=</id>)',line)
                if "{{infobox person" in line:#if there is an infobox person, then this is a person
                    spouse = "N/A"         
                    children = "N/A"
                    birth_date = "N/A"
                    death_date = "N/A"
                    nationality = "N/A"
                    alma_mater = "N/A"
                    #did not implement popularity score yet!
                    #wikipedia urls are not in the dump
                    while "}}" not in line:     #while we are not at the end of the infobox
                        if "spouse" in line:    #if there is a spouse, get the spouse with regex
                            spouse = process_spouse(line)
                        if "children" in line:  #if there are children, get the children with regex
                            children = process_children(line)
                        if "birth_date" in line:
                            birth_date = process_bday(line)
                        if "death_date" in line:
                            death_date = process_dday(line)
                        if "nationality" in line:
                            nationality = process_nat(line)
                        if "alma_mater" in line:
                            alma_mater = process_alma(line)

                        line = filestream.next()
                    #print the info here
                    #this will be where the info gets added to the database
                    #we can include other attributes like
                    #residence, birth place, 
                    print title.group(0)
                    print PID.group(0)
                    print birth_date
                    print death_date
                    print spouse
                    print children
                    print nationality
                    print alma_mater
                    print "\n\n\n"
                    print "INSERT INTO Person(PID, name, birth_date, death_date, nationality, popularity_score) VALUES(%d, \"%s\", \"%s\", \"%s\", \"%s\", %d);" % (int(PID.group(0)), title.group(0), birth_date, death_date, nationality, 0)
                    global cursor
                    cursor.execute("INSERT INTO Person(PID, name, birth_date, death_date, nationality, popularity_score) VALUES(%d, \"%s\", \"%s\", \"%s\", \"%s\", %d);" % (int(PID.group(0)), title.group(0), birth_date, death_date, nationality, 0))  
                    #popularity score set to 0 for now
                    if spouse != 'N/A':
                        for person in spouse:
                            cursor.execute('INSERT INTO Spouse(name1, name2, date) VALUES(\"%s\", \"%s\", \"%s\");' % (title.group(0), person, "N/A"))
                        #date for marriage is set to "N/A" for now
                    if children != 'N/A':
                        for child in children:
                            cursor.execute('INSERT INTO Child(parent_name, child_name) VALUES(\"%s\", \"%s\");' % (title.group(0), child))
                    if alma_mater != 'N/A':
                        for uni in alma_mater:
                            cursor.execute('INSERT INTO Alma_mater(name, university) VALUES(\"%s\", \"%s\");' % (title.group(0), uni))  
                            
                line = filestream.next()

def process_spouse(line):     #todo: implement this to strip strings and return a tuple of all 
    return [line]           # everything in a good format

def process_children(line):
    return [line]

def process_bday(line):
    return line

def process_dday(line):
    return line

def process_nat(line):
    return line

def process_alma(line):
    return [line]

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

