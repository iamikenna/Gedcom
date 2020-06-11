"""
Author: Ibezim Ikenna
User function to read files for my homework and display in a pretty table
"""

from typing import IO, Dict, Tuple, List
import string

from datetime import datetime #Date calculation
from prettytable import PrettyTable #Used to build a table
from collections import defaultdict

class Individual:

    """Class individual"""
    
     
    def __init__(self, arg, i_counter):
    
        """Individual characteristics"""

        # lets think of attributes that we want private __attribute
        self.i_counter = i_counter
        self.id = arg
        self.name: str = 'NA'
        self.gender: str = 'NA'
        self.birthday = 'NA'
        self.age = 'NA'
        self.alive: bool = True
        self.death = 'NA'
        self.child = set()
        self.spouse = set()
        
    def info(self) -> List[str]:

        """Returns list of info to be used in individual pretty table."""

        return [self.i_counter, self.id, self.name, self.gender, self.birthday,
                self.age, self.alive, self.death, self.child, self.spouse
                ]
        
class Family:

    """Class Family"""
    

    def __init__(self, arg, f_counter):

        """Family characteristics."""

        # lets think of attributes that we want private __attribute
        self.f_counter = f_counter
        self.id = arg
        self.married = "NA"
        self.divorced = "NA"
        self.husbandId = "NA"
        self.husbandName = "NA"
        self.wifeId = "NA"
        self.wifeName = "NA"
        self.children = set()

    def info(self) -> List[str]:

        """Returns list of info to be used in family pretty table."""

        return [self.f_counter, self.id, self.married, self.divorced, self.husbandId,
                self.husbandName, self.wifeId, self.wifeName, self.children
                ]

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
    

    def __init__(self, path) -> None:
        
        
        """Initialize printing pretty tables here
        refer to Individual and family here"""
        self.path = path
        self.indi_storage: Dict[int, Individual] = dict() #indi_storage[indiv_id] = Individual()
        self.fam_storage: Dict[int, Family] = dict() #fam_storage[fam_counter] = Family()
    

    def ged_reader(self):
        """This function reads a gedcom file and displays output"""
        user_input = self.path #for test cases
        # user_input = input("Enter the file name \n") #taking input from the user
        # user_input = "" #proj02test.ged  #export-Forest.ged #sample-2.ged #p_gedcomData.ged #pro_gedcom.ged #general.ged #family.ged #original_fam.ged
        #Storing the level element as key and tag elements as values
        
        #Are these placeholders?
        #Separate lines for each variable?
        #Maybe take out 'fam_'
        dict_storage, indi_counter, fam_counter, death_c, child_c, spouse_c, death, marr_cnt, div_cnt, fam_, birth_cnt = {
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
                    line_list: List[str] = line.split(" ")
                    len_line: int = len(line_list)

                    #Checking the lines for that special case
                    #Should we just set it to level = blank, arg = blank 2, tag = blank 3?
                    if len_line == 3 and line_list[2] in dict_storage['5'] \
                                and line_list[0] == '0':
                        level, arg, tag = line_list #This assigns line_list[0] to level, line_list[1] to arg, line_list[2] to tag for that special format
                        valid = 'Y'
                    elif len_line >= 2:
                        level, tag, arg = line_list[0], line_list[1], " ".join(line_list[2:]) #Separate lines for each variable?
                        if level in dict_storage and tag in dict_storage[level]:
                            valid: str = 'Y'
                        else:
                            valid: str = 'N'

                    #INDIVIUDAL STUFF
        
                    if level == "0" and tag == "INDI": #This is fetching all users and families in the file
                        indi_counter += 1 #This serves as a counter for individuals
                        indi: Individual = Individual(arg.strip("@"), indi_counter)
                        self.indi_storage[indi_counter] = indi #Ask about this line. Whats going on here?

                    #Assigning values to  Individual characteristics
                    elif level == "1" and tag == "NAME" \
                                and indi_counter in self.indi_storage.keys() \
                                and self.indi_storage[indi_counter].name == "NA":
                        self.indi_storage[indi_counter].name = arg

                    elif level == "1" and tag == "SEX" and \
                            indi_counter in self.indi_storage.keys() and \
                            self.indi_storage[indi_counter].gender == "NA":
                        self.indi_storage[indi_counter].gender = arg

                    elif level == "1" and tag == "BIRT" and \
                            indi_counter in self.indi_storage.keys():
                        tag_curr = tag #Used keeping track of dates and tags

                    #Setting up birthday    
                    elif level == "2" and tag == "DATE" and \
                        indi_counter in self.indi_storage.keys() and \
                        self.indi_storage[indi_counter].birthday == "NA" and \
                        self.indi_storage[indi_counter].age == "NA" and \
                        self.indi_storage[indi_counter].alive == True and \
                        self.indi_storage[indi_counter].death == "NA" and \
                        tag_curr == "BIRT":
                        
                        try:
                            self.indi_storage[indi_counter].birthday = self.date_convert(arg.split(" ")) # Maybe we should move our date_convert function to before our ged_reader?
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[indi_counter].alive = True
                            self.indi_storage[indi_counter].death = "NA"

                        #Setting up age
                        try:
                            alive_age = datetime.today().year \
                            - self.date_convert(arg.split(" ")).year #Is this only finding the difference between the years?
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[indi_counter].age = alive_age

                    #Setting up date of death
                    elif level == "1" and tag == "DEAT" and \
                            indi_counter in self.indi_storage.keys():
                        tag_curr = tag
                    elif level == "2" and tag == "DATE" and \
                        indi_counter in self.indi_storage.keys() and \
                        self.indi_storage[indi_counter].death == "NA" and \
                        tag_curr == "DEAT":
                        try:
                            self.indi_storage[indi_counter].death = self.date_convert(arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            if self.indi_storage[indi_counter].death != "NA":
                                self.indi_storage[indi_counter].alive= False
                                
                                #Setting up age of death
                                try:
                                    death_age = self.date_convert(arg.split(" ")).year \
                                    - self.indi_storage[indi_counter].birthday.year
                                except AttributeError:
                                    print(f"Invalid date: {arg}")
                                else:
                                    self.indi_storage[indi_counter].age = death_age
                    

                    #Why the plus/minus for spouse_c and child_c?
                    #Setting up IDs(F1, F2, F3) for children and spouses? 
                    elif level == "1" and tag == "FAMS" and \
                            indi_counter in self.indi_storage.keys() and \
                            self.indi_storage[indi_counter].spouse == set():
                        #spouse_c += 1
                        self.indi_storage[indi_counter].spouse.add(arg.strip("@"))
                        #spouse_c -= 1
                        #if self.indi_storage[indi_counter].spouse == set() and \
                        #        spouse_c == 1:
                        #    self.indi_storage[indi_counter].spouse.add(arg.strip("@"))
                        #    spouse_c -= 1
                        #else:
                        #    self.indi_storage[indi_counter].spouse.add(arg.strip("@"))
                        #    spouse_c -= 1


                    #Repeat for child if above works

                    elif level == "1" and tag == "FAMC" and \
                            indi_counter in self.indi_storage.keys() and \
                            self.indi_storage[indi_counter].child == set():
                        child_c += 1
                        self.indi_storage[indi_counter].child.add(arg.strip("@"))
                        child_c -= 1
                        # if self.indi_storage[indi_counter].child == set() and \
                        #         child_c == 1:
                        #     self.indi_storage[indi_counter].child.add(arg.strip("@"))
                        #     child_c -= 1
                        # else:
                        #     self.indi_storage[indi_counter].child.add(arg.strip("@"))
                        #     child_c -= 1

                    #FAMILY LEVEL STUFF

                    elif level == "0" and tag == "FAM":
                        fam_counter += 1
                        fam = Family(arg.strip("@"), fam_counter)
                        self.fam_storage[fam_counter] = fam

                    elif level == "1" and tag == "CHIL" and \
                            fam_counter in self.fam_storage.keys():
                        try:
                            self.fam_storage[fam_counter].children.add(arg.strip("@"))
                        except KeyError as e:
                            print(f"{e}:")

                    elif level == "1" and tag == "MARR" and \
                            fam_counter in self.fam_storage.keys():
                        tag_curr = "MARR"

                    elif level == "2" and tag == "DATE" and \
                            fam_counter in self.fam_storage.keys() and \
                            self.fam_storage[fam_counter].married == "NA" and \
                            tag_curr == "MARR":
                        try:
                            self.fam_storage[fam_counter].married = self.date_convert(arg.split(" ")) 
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                    
                    #Setting up divorce date in next elif
                    elif level == "1" and tag == "DIV" and \
                            fam_counter in self.fam_storage.keys():
                        tag_curr = "DIV"

                    elif level == "2" and tag == "DATE" and \
                            fam_counter in self.fam_storage.keys() and \
                            self.fam_storage[fam_counter].divorced == "NA" and \
                            tag_curr == "DIV":
                        try:
                            self.fam_storage[fam_counter].divorced = self.date_convert(arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")

                    elif level == "1" and tag == "HUSB" and \
                            fam_counter in self.fam_storage.keys() and \
                            self.fam_storage[fam_counter].husbandId == "NA" and \
                            self.fam_storage[fam_counter].husbandName == "NA":
                        self.fam_storage[fam_counter].husbandId = arg.strip("@")
                        for offset, vals in self.indi_storage.items():
                            if arg.strip("@") == vals.id:
                                name = vals.name
                            else:
                                continue
                        else:
                            self.fam_storage[fam_counter].husbandName = name

                    elif level == "1" and tag == "WIFE" and \
                            fam_counter in self.fam_storage.keys() and \
                            self.fam_storage[fam_counter].wifeId == "NA" and \
                            self.fam_storage[fam_counter].wifeName == "NA":
                        self.fam_storage[fam_counter].wifeId = arg.strip("@")
                        for offset, vals in self.indi_storage.items():
                            if arg.strip("@") == vals.id:
                                name = vals.name
                            else:
                                continue
                        else:
                            self.fam_storage[fam_counter].wifeName = name

                    else:
                        tag_curr = ""
                        continue
                else:
                    return(self.indi_storage, self.fam_storage) #testing with a testcase

                  

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

        pretty_table3 = PrettyTable(field_names=['NO', 'ID', 'Name',
                                                'Gender','Birthday', 'Age',
                                                'Alive', 'Death', 'Child',
                                                'Spouse'
                                                ])
        for offset, vals in self.indi_storage.items():
            try:
                pretty_table3.add_row(vals.info())
            except UnboundLocalError as e:
                print(e)
        print(pretty_table3)
        
    def pretty_table_fam(self):

        """This function is used to print out the data of Family in a table format"""

        pretty_table4 = PrettyTable(field_names=['NO', 'ID', 'Married',
                                                'Divorced', 'Husband ID',
                                                'Husband Name', 'Wife ID',
                                                'Wife Name', 'Children'
                                                ])
        for offset, vals in self.fam_storage.items():
            try:
                pretty_table4.add_row(vals.info())
            except UnboundLocalError as e:
                print (e) 
        print(pretty_table4)
        
        
    """This would be used for our user stories"""

    def us27(self):

        """Include person's current age when listing individuals --Ikenna"""
       
        print("This is user story 27 --Ikenna")
        id_age = []
       
        for i in self.indi_storage.values():
            id_age.append((i.id, i.age))
        print(self.pretty_table_indiv())#This prints out a list of indiviuals and their ages included
        return id_age

    def us22(self):

        """All individual IDs should be unique and all family IDs should be unique --Ikenna"""
        
        print("This is user story 22 --Ikenna")
        d_i = defaultdict(int)
        d_f = defaultdict(int)
        l_i, l_f = [],[]
        #Give variable names to d, f?
        for offset_1, vals_1 in self.indi_storage.items():
            
            d_i[vals_1.id] += 1
            for offset_2, vals_2 in d_i.items():
                if vals_2 > 1 and offset_2 == vals_1.id:
                    name = vals_1.name
                    l_i.append(offset_2)
                    print(f"ERROR: ID: {offset_2} is not unique and has another INDIVIDUAL: {name}")
           
        for offset_1, vals_1 in self.fam_storage.items():
            d_f[vals_1.id] += 1
            for offset_2, vals_2 in d_f.items():
                if vals_2 > 1 and offset_2 == vals_1.id:
                    h_name = vals_1.husbandName
                    w_name = vals_1.wifeName
                    l_f.append(offset_2)
                    print(f"ERROR: ID: {offset_2} is not unique and has another FAMILY: {h_name}, {w_name}")
        return l_i,l_f
    
    
    """This would be used for our user stories"""

    def us07(self):

        """ --Ikenna"""
       
        print("This is user story 07 --Ikenna")
        pass

    def us08(self):

        """  --Ikenna"""
        
        print("This is user story 08 --Ikenna")
        pass
        
                
def main():
    """
    Testing
    """
    # test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged") #--Ikenna
    test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged") #Please change to your current path
    test.ged_reader() #Calling the gedcom file reader
    # test.us27() #Calling the user story 27 function
    # test.us22() #Calling the user story 22 function
    # test.pretty_table_fam()  
    # test.indi_storage

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
