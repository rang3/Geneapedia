import re,string

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
   

################################################################################## 

fp = open('out.txt','r')
# each line of fp represents the single line transformed infobox information

for text in fp:
    info_list = make_a_list(text)
