def process_bday(birth_date):
    processed = re.search("\d{4}\|\d{1,2}\|\d{1,2}", birth_date)
    if(processed == None):
        processed = re.search("[a-zA-Z]{3,9}\s*\d{1,2}, \d{1,4} ?(B.C.)?",birth_date)
    if(processed == None):
        processed = re.search("[a-zA-Z]{3,9} \d{4} ?(B.C.)?", birth_date)
    if(processed == None):
        processed = re.search("\d{4} ?(B.C.)?",birth_date)

    return processed

def process_dday(death_date):
    processed = ''
    if(re.search("death date and age", death_date) != None):
        processed = re.search("\d{1,4}\|\d{1,2}\|\d{1,2}",death_date).group(1)
    elif re.search("[a-zA-Z]{3,9} (\d{1,2},) \d{1,4}",death_date) != None:
        processed = re.search("[a-zA-Z]{3,9} (\d{1,2},) \d{1,4}", death_date).group(0)
    elif re.search("[a-zA-Z]{3,9} \d{1,4}", death_date) != None:
        processed = re.search("[a-zA-Z]{3,9} \d{1,4}",death_date).group(0)
        
