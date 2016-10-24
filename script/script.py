#This script was written to take information from the 
#Wikipedia xml dumps and store it in our mySQL db.

import sys, getopt, getpass
from bs4 import BeautifulSoup
import MySQLdb as mdb
from lxml import etree
import re

def getPassword():
    password = getpass.getpass('enter password: ')
    return password

def parseFile(username, wikifile):
    filestream = open(wikifile, 'r')
    for line in filestream:
        if "<page>" in line:
            print "new page"
            title = ""
            while "</page>" not in line:
                if "<title>" in line:
                    title = re.search('(?<=<title>)(.*)(?=</title>)' , line)
                if "{{infobox person" in line:
                    spouse = ""
                    children = ""
                    while "}}" not in line:
                        if "spouse" in line:
                            spouse = re.search('?<=spouse(\s*)=(s*)(\[{2})?(\w+)',line)
                        if "children" in line:
                            children = re.search('',line)
                        filestream.next()
                    print spouse.group(0)
                            
                line = filestream.next()
            print title.group(0)


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

