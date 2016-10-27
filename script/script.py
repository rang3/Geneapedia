#This script was written to take information from the 
#Wikipedia xml dumps and store it in our mySQL db.

import sys, getopt, getpass
from bs4 import BeautifulSoup
import MySQLdb as mdb
from lxml import etree
import re
#regex_search = re.search('regex', string)
#regex_search.group(0)


#harris's comment
def getPassword():
    password = getpass.getpass('enter password: ')
    return password

def parseFile(username, wikifile):
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
                            
                line = filestream.next()

def process_spouse(line):     #todo: implement this to strip strings and return a tuple of all 
    return line           # everything in a good format

def process_children(line):
    return line

def process_bday(line):
    return line

def process_dday(line):
    return line

def process_nat(line):
    return line

def process_alma(line):
    return line

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hu:pi:", [])
    except getopt.GetoptError:
        print('script.py -u <username> -p -i <input>')
        sys.exit()

    username = ''
    password = ''
    wikifile = ''
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
            
    parseFile(username, wikifile)    #taglist is a wikisoup
if __name__ == "__main__":
    main(sys.argv[1:])

