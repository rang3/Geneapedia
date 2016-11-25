#This script was written to take information from the 
#Wikipedia xml dumps and store it in our mySQL db.

import sys, getopt, getpass
from bs4 import BeautifulSoup
import MySQLdb
from lxml import etree
import re
import string
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
#Person(PID, name, birth_date, death_date, popularity_score)
#       --- -----
#Spouse(name1, name2, date)
#       ----  ----
#Child(parent_name, child_name)
#      -----------  ----------
#Alma_mater(name, university)


###############################################################
#make infodic function
def makeinfodic(x):
    a = re.split('\|[ \t\n\r\f\v]*?([a-z\_]*?)[ \t\n\r\f\v]*?=',x)
    info_dic = {}
    target = ['children','spouse','alma_mater','birth_date','death_date','nationality']
    for i in target:info_dic.setdefault(i,'')
    cnt = 0
    for i in a:
        if cnt == len(a)-1:break
        if i in target:
            info_dic[i]=a[cnt+1]
        cnt +=1
    return info_dic

def spouse_children_alma(search_text,x):
    text = re.findall(search_text,x)
    for i in range(len(text)):
        text[i] = text[i].strip()
    temp_text = list(text)
    A = list(string.ascii_uppercase)
    Aa = list(string.ascii_letters)
    num = list(string.digits)
    for i in temp_text:
        flag = 0
        special_character = re.findall('[^ \t\n\r\f\va-zA-Z0-9_\-\.\,\']',i)
        if len(special_character) >=1:
            flag = 1
        elif len(i) <=8:
            flag = 1
        elif (i[0] not in A):
            flag = 1
        elif (i.startswith('Nonspecific')):
            flag = 1
        elif (i[-1] not in Aa) and (i[-1] not in num):
            flag = 1
        elif len(i.split()) >4:
            flag = 1
        if flag ==1:
            text.remove(i)
    if len(text) == 0:
        text = ['N/A']
        return text
    return text

def process_bday(birth_date):
    processed = re.search("\d{4}\|\d{1,2}\|\d{1,2}", birth_date)
    if(processed == None):
        processed = re.search("[a-zA-Z]{3,9}\s*\d{1,2}, \d{1,4} ?(B.C.)?",birth_date)
    if(processed == None):
        processed = re.search("[a-zA-Z]{3,9} \d{4} ?(B.C.)?", birth_date)
    if(processed == None):
        processed = re.search("\d{4} ?(B.C.)?",birth_date)
    if processed:
        return processed.string[processed.start():processed.end()]
        #return processed.group(1) 
    return None

def process_dday(death_date):
    processed = ''
    if(re.search("death date and age", death_date) != None):
        processed = re.search("\d{1,4}\|\d{1,2}\|\d{1,2}",death_date)
    elif re.search("[a-zA-Z]{3,9} (\d{1,2},) \d{1,4}",death_date) != None:
        processed = re.search("[a-zA-Z]{3,9} (\d{1,2},) \d{1,4}", death_date)
    elif re.search("[a-zA-Z]{3,9} \d{1,4}", death_date) != None:
        processed = re.search("[a-zA-Z]{3,9} \d{1,4}",death_date)
    if processed:
        return processed.string[processed.start():processed.end()]
    return None

def process_input_type(x,input_type):
    if input_type == 'children' or input_type == 'spouse' or input_type == 'alma_mater':
        if input_type == 'alma_mater':
            search_text = '([ \t\n\r\f\va-zA-Z0-9_\-\.\,\']*)'
        else:
            search_text = '([ \t\n\r\f\va-zA-Z0-9_\-\.\']*)'
        text = spouse_children_alma(search_text,x[input_type])
        return text
    else:
        if input_type == 'birth_date':
            bday = process_bday(x[input_type])
            return bday
        elif input_type == 'death_date':
            dday = process_dday(x[input_type])
            return dday

def make_a_list(x):
    info_dic = makeinfodic(x)
    spouse_list = process_input_type(info_dic,'spouse')
    children_list = process_input_type(info_dic,'children')
    alma_mater_list = process_input_type(info_dic,'alma_mater')
    bday = process_input_type(info_dic,'birth_date')
    dday = process_input_type(info_dic,'death_date')
    #print [spouse_list,children_list,alma_mater_list,bday,dday]
    return [spouse_list,children_list,alma_mater_list,bday,dday]
#end of process   
###################################################################

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

                    #print title
                    #print PID
                    #print infobox
                    #[['Mary Mannering', 'Beatrice Mary Beckley'], ['N/A'], ['N/A'], 'September 6, 1869', 'November 8, 1926']
#Person(PID, name, birth_date, death_date, popularity_score)
#       --- -----
#Spouse(name1, name2, date)
#       ----  ----
#Child(parent_name, child_name)
#      -----------  ----------
#Alma_mater(name, university)
                    infolist = make_a_list(infobox)
                    spouse_list = infolist[0]
                    child_list = infolist[1]
                    alma_list = infolist[2]
                    birth_date = infolist[3]
                    death_date = infolist[4]
                    global cursor
                    cursor.execute("INSERT INTO Person(PID, name, birth_date, death_date, popularity_score) VALUES(%d, \"%s\", \"%s\", \"%s\", %d);" % (int(PID), title, birth_date, death_date, 0))  
                    #popularity score set to 0 for now
                    if spouse_list != ['N/A']:
                        for person in spouse_list:
                            cursor.execute('INSERT INTO Spouse(name1, name2, date) VALUES(\"%s\", \"%s\", \"%s\");' % (title, person, "N/A"))
                        #date for marriage is set to "N/A" for now
                    if child_list != ['N/A']:
                        for child in child_list:
                            cursor.execute('INSERT INTO Child(parent_name, child_name) VALUES(\"%s\", \"%s\");' % (title, child))
                    if alma_list != ['N/A']:
                        for uni in alma_list:
                            cursor.execute('INSERT INTO Alma_mater(name, university) VALUES(\"%s\", \"%s\");' % (title, uni))  
    
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

