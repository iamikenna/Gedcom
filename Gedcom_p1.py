"""
Author: Ibezim Ikenna
User function to read files for my homework and display in a pretty table
"""
from datetime import datetime #Date calculation
from prettytable import PrettyTable #Used to build a table
from collections import defaultdict
indi_storage, fam_storage, gen_storage = {}, {}, {} #Storage for both Individuals, Families and altogether

def ged_reader():
    """This function reads a gedcom file and displays output"""
    user_input = input("Enter the file name \n") #taking input from the user
    # user_input = "" #proj02test.ged  #export-Forest.ged #sample-2.ged #p_gedcomData.ged #pro_gedcom.ged #general.ged #family.ged #original_fam.ged
    #Storing the level element as key and tag elements as values
    dict_storage, user_id, fam_id, death_c, child_c, spouse_c, death, marr_cnt, div_cnt, fam_, birth_cnt = {
            '0':['HEAD','NOTE','TRLR'],
            '1':['BIRT','CHIL','DIV','HUSB','WIFE','MARR','NAME','SEX','DEAT','FAMC','FAMS'],
            '2':['DATE'],
            '5':['INDI', 'FAM']
        }, 0, 0, 0, 0, 0, "NA", 0, 0, "", 0
    tag_curr = ""
   
    try: #Catching an exception
        open_file = open(user_input,"r")
    except FileNotFoundError as e:
        print(e)
    else:
        with open_file: # This closes the file after using the file
            for line in open_file:
                line = line.strip()
                print(f"-->{line}")
                line_list = line.split(" ")
                len_line = len(line_list)
                #Checking the lines for a specific format
                if len_line == 3 and line_list[2] in dict_storage['5'] and line_list[0] == '0':
                    level,arg, tag = line_list
                    valid = 'Y'
                elif len_line >= 2:
                    level, tag, arg = line_list[0], line_list[1], " ".join(line_list[2:])
                    if level in dict_storage and tag in dict_storage[level]:
                        valid = 'Y'
                    else:
                        valid = 'N'
                print(f"<--{level}|{tag}|{valid}|{arg}\n\n")
    
                if level == "0" and tag == "INDI": #This is fetching all users and families in the file
                    user_id += 1
                    indi_storage[user_id] = {"ID": arg.strip("@")}
                    indi_storage[user_id]["Name"] = "NA"
                    indi_storage[user_id]["Gender"] = "NA"
                    indi_storage[user_id]["Birthday"] = "NA"
                    indi_storage[user_id]["Age"] = "NA"
                    indi_storage[user_id]["Alive"] = "NA"
                    indi_storage[user_id]["Death"] = "NA"
                    indi_storage[user_id]["Child"] = "NA"
                    indi_storage[user_id]["Spouse"] = "NA" 
                elif level == "1" and tag == "NAME" and user_id in indi_storage.keys() and indi_storage[user_id]["Name"] == "NA":
                    indi_storage[user_id]["Name"] = arg
                elif level == "1" and tag == "SEX" and user_id in indi_storage.keys() and indi_storage[user_id]["Gender"] == "NA":
                    indi_storage[user_id]["Gender"] = arg
                elif level == "1" and tag == "BIRT" and user_id in indi_storage.keys():
                    tag_curr = tag
                elif level == "2" and tag == "DATE" and user_id in indi_storage.keys() and indi_storage[user_id]["Birthday"] == "NA"  and indi_storage[user_id]["Age"] == "NA" and indi_storage[user_id]["Alive"] == "NA" and indi_storage[user_id]["Death"] == "NA" and tag_curr == "BIRT":
                    try:
                        indi_storage[user_id]["Birthday"] = date_convert(arg.split(" "))
                    except AttributeError:
                        print(f"Invalid date: {arg}")
                    else:
                        indi_storage[user_id]["Alive"] = "True"
                        indi_storage[user_id]["Death"] = "NA"
                    try:
                        alive_age = datetime.today().year - date_convert(arg.split(" ")).year
                    except AttributeError:
                        print(f"Invalid date: {arg}")
                    else:
                        indi_storage[user_id]["Age"] = alive_age
                elif level == "1" and tag == "DEAT" and user_id in indi_storage.keys():
                    tag_curr = tag
                elif level == "2" and tag == "DATE" and user_id in indi_storage.keys() and indi_storage[user_id]["Death"] == "NA" and tag_curr == "DEAT":
                    try:
                        indi_storage[user_id]["Death"] = date_convert(arg.split(" "))
                    except AttributeError:
                        print(f"Invalid date: {arg}")
                    else:
                        if indi_storage[user_id]['Death'] != "NA":
                            indi_storage[user_id]['Alive']= "False"
                            try:
                                death_age = date_convert(arg.split(" ")).year - indi_storage[user_id]["Birthday"].year
                            except AttributeError:
                                print(f"Invalid date: {arg}")
                            else:
                                indi_storage[user_id]["Age"] = death_age
                elif level == "1" and tag == "FAMS" and user_id in indi_storage.keys() and indi_storage[user_id]["Spouse"] == "NA":
                    spouse_c += 1
                    if indi_storage[user_id]["Spouse"] == "NA" and spouse_c == 1:
                        indi_storage[user_id]['Spouse'] = set()
                        indi_storage[user_id]["Spouse"].add(arg.strip("@"))
                        spouse_c -= 1
                    else:
                        indi_storage[user_id]["Spouse"].add(arg.strip("@"))
                        spouse_c -= 1
                elif level == "1" and tag == "FAMC" and user_id in indi_storage.keys() and indi_storage[user_id]["Child"] == "NA":
                    child_c += 1
                    if indi_storage[user_id]["Child"] == "NA" and child_c == 1:
                        indi_storage[user_id]['Child'] = set() 
                        indi_storage[user_id]["Child"].add(arg.strip("@"))
                        child_c -= 1
                    else:
                        indi_storage[user_id]["Child"].add(arg.strip("@"))
                        child_c -= 1
                elif level == "0" and tag == "FAM":
                    fam_id += 1
                    fam_storage[fam_id] = {"ID": arg.strip("@")}
                    fam_ += arg.strip("@")
                    fam_storage[fam_id]["Children"] = set()
                    fam_storage[fam_id]["Married"] = "NA"
                    fam_storage[fam_id]["Divorced"] = "NA"
                    fam_storage[fam_id]["Husband ID"] = "NA"
                    fam_storage[fam_id]["Husband Name"] = "NA"
                    fam_storage[fam_id]["Wife ID"] = "NA"
                    fam_storage[fam_id]["Wife Name"] = "NA"
                elif level == "1" and tag == "CHIL" and fam_id in fam_storage.keys():
                    try:
                        fam_storage[fam_id]["Children"].add(arg.strip("@"))
                    except KeyError as e:
                        print(f"{e}:")
                elif level == "1" and tag == "MARR"  and fam_id in fam_storage.keys():
                    tag_curr = "MARR"
                elif level == "2" and tag == "DATE" and fam_id in fam_storage.keys() and fam_storage[fam_id]["Married"]=="NA" and tag_curr == "MARR":
                    try:
                        fam_storage[fam_id]["Married"] = date_convert(arg.split(" "))   
                    except AttributeError:
                        print(f"Invalid date: {arg}")
                elif level == "1" and tag == "DIV" and fam_id in fam_storage.keys():
                    tag_curr = "DIV"
                elif level == "2" and tag == "DATE" and fam_id in fam_storage.keys()  and fam_storage[fam_id]["Divorced"] == "NA" and tag_curr == "DIV":
                    try:
                        fam_storage[fam_id]["Divorced"] = date_convert(arg.split(" "))
                    except AttributeError:
                        print(f"Invalid date: {arg}")
                elif level == "1" and tag == "HUSB" and fam_id in fam_storage.keys() and fam_storage[fam_id]["Husband ID"] == "NA" and fam_storage[fam_id]["Husband Name"] == "NA":
                    fam_storage[fam_id]["Husband ID"] = arg.strip("@")
                    for i,j in indi_storage.items():
                        if arg.strip("@") in j.values():
                            name = j["Name"]
                        else:
                            continue
                    else:
                        fam_storage[fam_id]["Husband Name"] = name
                elif level == "1" and tag == "WIFE" and fam_id in fam_storage.keys() and fam_storage[fam_id]["Wife ID"] == "NA" and fam_storage[fam_id]["Wife Name"] == "NA":
                    fam_storage[fam_id]["Wife ID"] = arg.strip("@")
                    for i,j in indi_storage.items():
                        if arg.strip("@") in j.values():
                            name = j["Name"]
                        else:
                            continue
                    else:
                        fam_storage[fam_id]["Wife Name"] = name
                else:
                    tag_curr = ""
                    continue

def date_convert(g_date): 
    """Converting '15 MAY 2020' into '2020-5-15' and g_date takes a date in a list:[] form """
    g_date = " ".join(g_date)
    try:
        g_object = datetime.strptime(g_date, "%d %b %Y")
    except (ValueError, AttributeError):
        return(f"Invalid Date: {g_date}")
    else:
        return(g_object.date())

def pretty_table_indiv():
    """This function is used to print out the data of Individuals in a table format"""
    pretty_table3 = PrettyTable(field_names=['NO','ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])
    for i,j in indi_storage.items():
        for k,m in j.items():
            no_ = i
            if k == 'ID':
                id_ = m
            elif k == 'Name':
                na_ = m
            elif k == 'Gender':
                ge_ = m
            elif k == 'Birthday':
                bi_ = m
            elif k == 'Age':
                ag_ = m
            elif k == 'Alive':
                al_ = m
            elif k == 'Death':
                de_ = m
            elif k == 'Child':
                ch_ = m
            elif k == 'Spouse':
                sp_ = m
            else:
                continue
        try:
            pretty_table3.add_row([no_, id_, na_, ge_, bi_, ag_, al_, de_, ch_, sp_])
        except UnboundLocalError as e:
            print(e)
    print(pretty_table3)
    
def pretty_table_fam():
    """This function is used to print out the data of Family in a table format"""
    pretty_table4 = PrettyTable(field_names=['NO','ID', 'Married' , 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
    for i in range(1, (len(fam_storage) + 1)):
        no = i
        for n, m in fam_storage[i].items():
            if n == 'ID':
                id_ = m
            elif n == 'Married':
                na_ = m
            elif n == 'Divorced':
                ge_ = m
            elif n == 'Husband ID':
                bi_ = m
            elif n == 'Husband Name':
                ag_ = m
            elif n == 'Wife ID':
                al_ = m
            elif n == 'Wife Name':
                de_ = m
            elif n == 'Children':
                ch_ = m
            else:
                continue
        try:
            pretty_table4.add_row([no, id_, na_, ge_, bi_, ag_, al_, de_, ch_])
        except UnboundLocalError as e:
            print (e) 
    print(pretty_table4)
    
"""This would be used for our user stories"""
def us27():
    """Include person's current age when listing individuals --Ikenna"""
    print("This is user story 27 --Ikenna")
    return pretty_table_indiv() #This prints out a list of indiviuals and their ages included
def us22():
    """All individual IDs should be unique and all family IDs should be unique --Ikenna"""
    print("This is user story 22 --Ikenna")
    d_i = defaultdict(int)
    d_f = defaultdict(int)
    for i,j in indi_storage.items():
        for n,m  in j.items():
            if n == "ID":
                d_i[m] += 1
        for d,f in d_i.items():
            if f > 1 and d in j.values():
                name = j["Name"]
                print(f"ERROR: ID: {d} is not unique and has another INDIVIDUAL: {name}")
            
    for i,j in fam_storage.items():
        for n,m  in j.items():
            if n == "ID":
                d_f[m] += 1
        for d,f in d_f.items():
            if f > 1 and d in j.values():
                h_name = j["Husband Name"]
                w_name = j["Wife Name"]
                print(f"ERROR: ID: {d} is not unique and has another FAMILY: {h_name}, {w_name}")
                
def main():
    """
    Testing
    """
    ged_reader() #Calling the gedcom file reader
    us27() #Calling the user story 27 function
    us22() #Calling the user story 22 function
       
    # pretty_table_indiv()   
    # pretty_table_fam()  
   
    print("This is the Individuals data in a dictionary format\n\n\n")
    print(indi_storage) 
    print("\n\n\n")
    
    print("This is the Family data in a dictionary format\n\n\n")
    print(fam_storage)       
    
    # gen_storage["individual"]= indi_storage
    # gen_storage["family"]= fam_storage
    # print("\n\n\n")
    
    # print("This is the general dictionary for both individuals and family\n\n\n")
    # print(gen_storage) 
    # print("\n\n\n")     
        
    # print("test anything you want here!!!!!!\n\n\n")
    # print(gen_storage["individual"][1]["Birthday"]) # testing datetime                                                                                                                                                                                                                                                                                                     
if __name__ == "__main__":
    main()
