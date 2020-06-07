"""
Author: Ibezim Ikenna
User function to read files for my homework and display in a pretty table
"""


from typing import IO, Dict, Tuple, List
import string

from datetime import datetime #Date calculation
from prettytable import PrettyTable #Used to build a table
from collections import defaultdict




#Refractoring in progress --ikenna
class Individual:

    """Class individual"""
    
     
    def __init__(self, arg, userId):
        # lets think of attributes that we want private __attribute
        self.userId = userId
        self.id = arg
        self.name = 'NA'
        self.gender = 'NA'
        self.birthday = 'NA'
        self.age = 'NA'
        self.alive = True
        self.death = 'NA'
        self.child = set()
        self.spouse = set()
        
    #other functions, potentially scrap add functions?
    #potentially keep for bounce checking
    #def addName(self, name):
    #    self.name = name
    #def addGender(self, gender):
    #    self.gender = gender
    #def addBirthday(self, birthday):
    #    self.birthday = birthday
    #def addAge(self, age):
    ##    self.age = age
    #def addAlive(self, alive):
    #    self.alive = alive
    #def addDeath(self, death):
    #    self.death = death
    #def addChild(self, child):
    #    self.child.add(child)
    #def addSpouse(self, spouse):
    #    self.spouse.add(spouse)

    def info(self) -> List[str]:

        return [self.userId, self.id, self.name, self.gender, self.birthday, self.age, self.alive, self.death, self.child, self.spouse]
        
class Family:
    
    """Class Family"""
    
    def __init__(self, arg, famId):
        # lets think of attributes that we want private __attribute
        self.famId = famId
        self.id = arg
        self.married = "NA"
        self.divorced = "NA"
        self.husbandId = "NA"
        self.husbandName = "NA"
        self.wifeId = "NA"
        self.wifeName = "NA"
        self.children = set()
        
    #other functions
    #def addMarried(self, date):
    #    self.married = date
    #def addDivorced(self, divorced):
    #    self.divorced = divorced
    #def addHusband(self, id_, husbandName):
    #    self.husbandId = id_
    #    self.husbandName = husbandName
    # def addWife(self, id_, wifeName):
    #     self.wifeId = id_
    #     self.wifeName = wifeName
    # def addChildren(self, children):
    #     self.children.add(children)

    def info(self) -> List[str]:
        return [self.famId, self.id, self.married, self.divorced, self.husbandId, self.husbandName, self.wifeId, self.wifeName, self.children]

class GedcomRepo:
    """Class Gedcom, keeps track of everything and main storage"""
    """
    Things we might need in this class
    
    1. Functions to find people, if neccessary
    2. Pretty table function to test output of data  #need to make a new function
    3. Individual and family dictionary E.g self.indi_storage, self.fam_storage, gen_storage = {}, {}  #we have this already
    4. date function , to calculate date in datetime   #we have this already
    5. parse function to read the file and input into the dictionaries      #we have this already
    
    Anything else!!!
    
    """
    
    def __init__(self) -> None:
        
        """Initialize printing pretty tables here
        refer to Individual and family here"""

        self.indi_storage: Dict[int, Individual] = dict() #indiv[indiv_id] = Individual()
        self.fam_storage: Dict[int, Family] = dict() #fam[fam_id] = Family()
    


    def ged_reader(self):
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
            open_file: IO = open(user_input,"r")
        except FileNotFoundError as e:
            print(e)
        else:
            with open_file: # This closes the file after using the file
                for line in open_file:
                    line: str = line.strip()
                    #print(f"-->{line}")
                    line_list: List[str] = line.split(" ")
                    len_line: int = len(line_list)

                    #Checking the lines for a specific format
                    if len_line == 3 and line_list[2] in dict_storage['5'] and line_list[0] == '0':
                        level,arg, tag = line_list #This assigns line_list[0] to level, line_list[1] to arg, line_list[2] to tag for that special format
                        valid = 'Y'
                    elif len_line >= 2:
                        level, tag, arg = line_list[0], line_list[1], " ".join(line_list[2:])
                        if level in dict_storage and tag in dict_storage[level]:
                            valid: str = 'Y'
                        else:
                            valid: str = 'N'
                    #print(f"<--{level}|{tag}|{valid}|{arg}\n\n")

                    #Afterwards is the extra functionality outside of Project02

                    #INDIVIUDAL STUFF
        
                    if level == "0" and tag == "INDI": #This is fetching all users and families in the file
                        user_id += 1
                        indi = Individual(arg.strip("@"), user_id)
                        self.indi_storage[user_id] = indi


                    elif level == "1" and tag == "NAME" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].name == "NA":
                        self.indi_storage[user_id].name = arg
                        #print(self.indi_storage[user_id].name)
                    elif level == "1" and tag == "SEX" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].gender == "NA":
                        self.indi_storage[user_id].gender = arg
                        #print(self.indi_storage[user_id].gender)
                    elif level == "1" and tag == "BIRT" and user_id in self.indi_storage.keys():
                        tag_curr = tag 
                        
                    elif level == "2" and tag == "DATE" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].birthday == "NA"  \
                        and self.indi_storage[user_id].age == "NA" and self.indi_storage[user_id].alive == True and self.indi_storage[user_id].death == "NA" and tag_curr == "BIRT":
                        
                        try:
                            self.indi_storage[user_id].birthday = self.date_convert(arg.split(" "))
                            #print(self.indi_storage[user_id].birthday)
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[user_id].alive = True
                            self.indi_storage[user_id].death = "NA"
                        try:
                            alive_age = datetime.today().year - self.date_convert(arg.split(" ")).year #Is this only finding the difference between the years?
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[user_id].age = alive_age
                    elif level == "1" and tag == "DEAT" and user_id in self.indi_storage.keys():
                        tag_curr = tag
                    elif level == "2" and tag == "DATE" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].death == "NA" and tag_curr == "DEAT":
                        try:
                            self.indi_storage[user_id].death = self.date_convert(arg.split(" "))
                            #print(self.indi_storage[user_id].death)
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            if self.indi_storage[user_id].death != "NA":
                                self.indi_storage[user_id].alive= False
                                try:
                                    death_age = self.date_convert(arg.split(" ")).year - self.indi_storage[user_id].birthday.year
                                except AttributeError:
                                    print(f"Invalid date: {arg}")
                                else:
                                    self.indi_storage[user_id].age = death_age
                    elif level == "1" and tag == "FAMS" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].spouse == set():
                        spouse_c += 1
                        if self.indi_storage[user_id].spouse == set() and spouse_c == 1:
                            self.indi_storage[user_id].spouse.add(arg.strip("@"))
                            #print(self.indi_storage[user_id].spouse)
                            spouse_c -= 1
                        else:
                            self.indi_storage[user_id].spouse.add(arg.strip("@"))
                            spouse_c -= 1
                    elif level == "1" and tag == "FAMC" and user_id in self.indi_storage.keys() and self.indi_storage[user_id].child == set():
                        child_c += 1
                        if self.indi_storage[user_id].child == set() and child_c == 1:
                            self.indi_storage[user_id].child.add(arg.strip("@"))
                            child_c -= 1
                        else:
                            self.indi_storage[user_id].child.add(arg.strip("@"))
                            child_c -= 1

                    #FAMILY LEVEL STUFF

                    elif level == "0" and tag == "FAM":
                        fam_id += 1
                        fam = Family(arg.strip("@"), fam_id)
                        self.fam_storage[fam_id] = fam

                    elif level == "1" and tag == "CHIL" and fam_id in self.fam_storage.keys():
                        try:
                            self.fam_storage[fam_id].children.add(arg.strip("@"))
                            #print(self.fam_storage[fam_id].children)
                        except KeyError as e:
                            print(f"{e}:")
                    elif level == "1" and tag == "MARR"  and fam_id in self.fam_storage.keys():
                        tag_curr = "MARR"
                    elif level == "2" and tag == "DATE" and fam_id in self.fam_storage.keys() and self.fam_storage[fam_id].married=="NA" and tag_curr == "MARR":
                        try:
                            self.fam_storage[fam_id].married = self.date_convert(arg.split(" "))   
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                    elif level == "1" and tag == "DIV" and fam_id in self.fam_storage.keys():
                        tag_curr = "DIV"
                    elif level == "2" and tag == "DATE" and fam_id in self.fam_storage.keys()  and self.fam_storage[fam_id].divorced == "NA" and tag_curr == "DIV":
                        try:
                            self.fam_storage[fam_id].divorced = self.date_convert(arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                    elif level == "1" and tag == "HUSB" and fam_id in self.fam_storage.keys() and self.fam_storage[fam_id].husbandId == "NA" and self.fam_storage[fam_id].husbandName == "NA":
                        self.fam_storage[fam_id].husbandId = arg.strip("@")
                        for i,j in self.indi_storage.items():
                            #i is the ID Number, j is the whole set/dictionary/thing
                            #print(i)
                            #print(j)
                            if arg.strip("@") == j.id:
                                name = j.name
                                #print(name)
                            else:
                                continue
                        else:
                            self.fam_storage[fam_id].husbandName = name
                    elif level == "1" and tag == "WIFE" and fam_id in self.fam_storage.keys() and self.fam_storage[fam_id].wifeId == "NA" and self.fam_storage[fam_id].wifeName == "NA":
                        self.fam_storage[fam_id].wifeId = arg.strip("@")
                        for i,j in self.indi_storage.items():
                            if arg.strip("@") == j.id:
                                name = j.name
                            else:
                                continue
                        else:
                            self.fam_storage[fam_id].wifeName = name
                    else:
                        tag_curr = ""
                        continue

                    #No children names?  #We only need the ID of the child and family id where they belong -- ikenna

    def date_convert(self, g_date): 
        """Converting '15 MAY 2020' into '2020-5-15' and g_date takes a date in a list:[] form """
        g_date = " ".join(g_date)
        try:
            g_object = datetime.strptime(g_date, "%d %b %Y")
        except (ValueError, AttributeError):
            return(f"Invalid Date: {g_date}")
        else:
            return(g_object.date())

    def pretty_table_indiv(self):
        """This function is used to print out the data of Individuals in a table format"""
        pretty_table3 = PrettyTable(field_names=['NO','ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'])
        for i,j in self.indi_storage.items():
            try:
                pretty_table3.add_row(j.info())
            except UnboundLocalError as e:
                print(e)
        print(pretty_table3)
        
    def pretty_table_fam(self):
        """This function is used to print out the data of Family in a table format"""
        pretty_table4 = PrettyTable(field_names=['NO','ID', 'Married' , 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
        for i,j in self.fam_storage.items():
            try:
                pretty_table4.add_row(j.info())
            except UnboundLocalError as e:
                print (e) 
        print(pretty_table4)
        
        
        
    """This would be used for our user stories"""

    def us27(self):
        """Include person's current age when listing individuals --Ikenna"""
        print("This is user story 27 --Ikenna")
        return self.pretty_table_indiv() #This prints out a list of indiviuals and their ages included
    def us22(self):
        """All individual IDs should be unique and all family IDs should be unique --Ikenna"""
        print("This is user story 22 --Ikenna")
        d_i = defaultdict(int)
        d_f = defaultdict(int)
        for i,j in self.indi_storage.items():
            d_i[j.id] += 1
            for d,f in d_i.items():
                if f > 1 and d == j.id:
                    name = j.name
                    print(f"ERROR: ID: {d} is not unique and has another INDIVIDUAL: {name}")
                
        for i,j in self.fam_storage.items():
            d_f[j.id] += 1
            for d,f in d_f.items():
                if f > 1 and d == j.id:
                    h_name = j.husbandName
                    w_name = j.wifeName
                    print(f"ERROR: ID: {d} is not unique and has another FAMILY: {h_name}, {w_name}")
                
def main():
    """
    Testing
    """
    test = GedcomRepo()
    test.ged_reader() #Calling the gedcom file reader
    test.us27() #Calling the user story 27 function
    test.us22() #Calling the user story 22 function
    test.pretty_table_fam()  

    
    #print('\n\n\n')
    #print("This is the Individuals data in a dictionary format\n\n\n")
    #print(self.indi_storage) 
    #print("\n\n\n")
    
    #print("This is the Family data in a dictionary format\n\n\n")
    #print(self.fam_storage)       
    
    # gen_storage["individual"]= self.indi_storage
    # gen_storage["family"]= self.fam_storage
    # print("\n\n\n")
    
    # print("This is the general dictionary for both individuals and family\n\n\n")
    # print(gen_storage) 
    # print("\n\n\n")     
        
    # print("test anything you want here!!!!!!\n\n\n")
    # print(gen_storage["individual"][1].birthday) # testing datetime                                                                                                                                                                                                                                                                                                     
if __name__ == "__main__":
    main()
