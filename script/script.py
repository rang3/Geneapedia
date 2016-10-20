#This script was written to take information from the 
#Wikipedia xml dumps and store it in our mySQL db.

import sys, getopt, getpass
#import MySQLdb as mdb

def getPassword():
    password = getpass.getpass('enter password: ')
    return password

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
        if opt == '-h':
            print('script.py -u <username> -p -i <input>')
        if opt == '-u':
            username = arg
        if opt == '-p':
            password = getPassword()
        if opt == '-i':
            wikifile = arg
            
    print(username)
    print(password)
    print(wikifile)
        
    file_stream = open(wikifile, 'r')
    for line in file_stream.readlines():
        print line
if __name__ == "__main__":
    main(sys.argv[1:])
