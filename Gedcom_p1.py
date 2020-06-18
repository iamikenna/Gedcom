"""
Author: Ibezim Ikenna
User function to read files for my homework and display in a pretty table
"""

import string
from typing import IO, Dict, Tuple, List
from datetime import datetime  # Date calculation
from dateutil.relativedelta import relativedelta  # Using this for us08
from prettytable import PrettyTable  # Used to build a table
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
    # we have this already
    3. Individual and family dictionary E.g self.indi_storage, self.fam_storage, gen_storage = {}, {}
    4. date function , to calculate date in datetime   #we have this already
    # we have this already
    5. parse function to read the file and input into the dictionaries

    Anything else!!!

    """

    def __init__(self, path) -> None:
        """Initialize printing pretty tables here
        refer to Individual and family here"""
        self.path = path
        # indi_storage[indiv_id] = Individual()
        self.indi_storage: Dict[int, Individual] = dict()
        # fam_storage[fam_counter] = Family()
        self.fam_storage: Dict[int, Family] = dict()

    def ged_reader(self):
        """This function reads a gedcom file and displays output"""
        user_input = self.path  # for test cases
        # user_input = input("Enter the file name \n") #taking input from the user
        # user_input = "" #proj02test.ged  #export-Forest.ged #sample-2.ged #p_gedcomData.ged #pro_gedcom.ged #general.ged #family.ged #original_fam.ged
        # Storing the level element as key and tag elements as values

        dict_storage, indi_counter, fam_counter, death_c, child_c, spouse_c, death, marr_cnt, div_cnt, fam_, birth_cnt = {
            '0': ['HEAD', 'NOTE', 'TRLR'],
            '1': ['BIRT', 'CHIL', 'DIV', 'HUSB', 'WIFE', 'MARR', 'NAME', 'SEX', 'DEAT', 'FAMC', 'FAMS'],
            '2': ['DATE'],
            '5': ['INDI', 'FAM']
        }, 0, 0, 0, 0, 0, "NA", 0, 0, "", 0
        tag_curr = ""

        try:  # Catching an exception
            open_file: IO = open(user_input, "r")
        except FileNotFoundError as e:
            print(e)
        else:
            with open_file:  # This closes the file after using the file
                for line in open_file:
                    line: str = line.strip()
                    line_list: List[str] = line.split(" ")
                    len_line: int = len(line_list)

                    if len_line == 3 and line_list[2] in dict_storage['5'] \
                            and line_list[0] == '0':
                        level, arg, tag = line_list
                        valid = 'Y'
                    elif len_line >= 2:
                        level, tag, arg = line_list[0], line_list[1], " ".join(
                            line_list[2:])
                        if level in dict_storage and tag in dict_storage[level]:
                            valid: str = 'Y'
                        else:
                            valid: str = 'N'

                    # INDIVIUDAL STUFF

                    if level == "0" and tag == "INDI":  # This is fetching all users and families in the file
                        indi_counter += 1  # This serves as a counter for individuals
                        indi: Individual = Individual(
                            arg.strip("@"), indi_counter)
                        self.indi_storage[indi_counter] = indi

                    # Assigning values to  Individual characteristics
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
                        tag_curr = tag

                    # Setting up birthday
                    elif level == "2" and tag == "DATE" and \
                            indi_counter in self.indi_storage.keys() and \
                            self.indi_storage[indi_counter].birthday == "NA" and \
                            self.indi_storage[indi_counter].age == "NA" and \
                            self.indi_storage[indi_counter].alive == True and \
                            self.indi_storage[indi_counter].death == "NA" and \
                            tag_curr == "BIRT":

                        try:
                            self.indi_storage[indi_counter].birthday = self.date_convert(
                                arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[indi_counter].alive = True
                            self.indi_storage[indi_counter].death = "NA"

                        # Setting up age
                        try:
                            alive_age = datetime.today().year \
                                - self.date_convert(arg.split(" ")).year
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            self.indi_storage[indi_counter].age = alive_age

                    # Setting up date of death
                    elif level == "1" and tag == "DEAT" and \
                            indi_counter in self.indi_storage.keys():
                        tag_curr = tag
                    elif level == "2" and tag == "DATE" and \
                            indi_counter in self.indi_storage.keys() and \
                            self.indi_storage[indi_counter].death == "NA" and \
                            tag_curr == "DEAT":
                        try:
                            self.indi_storage[indi_counter].death = self.date_convert(
                                arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            if self.indi_storage[indi_counter].death != "NA":
                                self.indi_storage[indi_counter].alive = False

                                # Setting up age of death
                                try:
                                    death_age = self.date_convert(arg.split(" ")).year \
                                        - self.indi_storage[indi_counter].birthday.year
                                except AttributeError:
                                    print(f"Invalid date: {arg}")
                                else:
                                    self.indi_storage[indi_counter].age = death_age

                    elif level == "1" and tag == "FAMS" and \
                            indi_counter in self.indi_storage.keys():

                        self.indi_storage[indi_counter].spouse.add(
                            arg.strip("@"))

                    elif level == "1" and tag == "FAMC" and \
                            indi_counter in self.indi_storage.keys():
                        self.indi_storage[indi_counter].child.add(
                            arg.strip("@"))

                    # FAMILY LEVEL STUFF

                    elif level == "0" and tag == "FAM":
                        fam_counter += 1
                        fam = Family(arg.strip("@"), fam_counter)
                        self.fam_storage[fam_counter] = fam

                    elif level == "1" and tag == "CHIL" and \
                            fam_counter in self.fam_storage.keys():
                        try:
                            self.fam_storage[fam_counter].children.add(
                                arg.strip("@"))
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
                            self.fam_storage[fam_counter].married = self.date_convert(
                                arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")

                    # Setting up divorce date
                    elif level == "1" and tag == "DIV" and \
                            fam_counter in self.fam_storage.keys():
                        tag_curr = "DIV"

                    elif level == "2" and tag == "DATE" and \
                            fam_counter in self.fam_storage.keys() and \
                            self.fam_storage[fam_counter].divorced == "NA" and \
                            tag_curr == "DIV":
                        try:
                            self.fam_storage[fam_counter].divorced = self.date_convert(
                                arg.split(" "))
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
                    # testing with a testcase
                    return(self.indi_storage, self.fam_storage)

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
                                                 'Gender', 'Birthday', 'Age',
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
                print(e)
        print(pretty_table4)

    """This would be used for our user stories"""

    # Author: Christopher McKenzie
    def us01(self):
        """Dates should not be after the current date."""

        present = datetime.date(datetime.now())
        errors: List[str] = []
        for person in self.indi_storage.values():
            if type(person.birthday) != str and person.birthday > present:
                print(
                    f'ERROR: INDIVIDUAL: US01: {person.id}: Birthday {person.birthday} occurs in the future.')
                errors.append(person.id)
            # We say != str to avoid both NA and Invalid Date
            elif type(person.death) != str and person.death > present:
                print(
                    f'ERROR: INDIVIDUAL: US01: {person.id}: Death {person.death} occurs in the future.')
                errors.append(person.id)

        for family in self.fam_storage.values():
            if type(family.married) != str and family.married > present:
                print(
                    f'ERROR: FAMILY: US01: {family.id}: Marriage {family.married} occurs in the future.')
                errors.append(family.id)
            elif type(family.divorced) != str and family.divorced > present:
                print(
                    f'ERROR: FAMILY: US01: {family.id}: Divorce {family.divorced} occurs in the future.')
                errors.append(family.id)

        return errors

    # Author: Christopher McKenzie
    def us02(self):
        """Birth should occur before marriage of an individual."""
        errors = []
        for family in self.fam_storage.values():
            if family.married != 'NA':
                for person in self.indi_storage.values():

                    try:
                        if person.name == family.husbandName and person.id == family.husbandId and person.birthday > family.married:
                            print(
                                f"ERROR: FAMILY: US02: {family.id}: Husband's birthday {person.birthday} occurs after marriage {family.married}.")
                            errors.append(person.id)

                        elif person.name == family.wifeName and person.id == family.wifeId and person.birthday > family.married:
                            print(
                                f"ERROR: FAMILY: US02: {family.id}: Wife's birthday {person.birthday} occurs after marriage {family.married}.")
                            errors.append(person.id)

                    except TypeError as e:
                        print(e)
        return errors

    # Author: Lehmann Margaret
    def us04(self):
        """ Marriage should occur before divorce of spouses, and divorce can only occur after marriage """
        errors: List[str] = []
        for fam in self.fam_storage.values():
            if fam.divorced != "NA":
                if fam.divorced < fam.married:
                    error = f"ERROR: FAMILY: US04: {fam.id}: Divorced {fam.divorced} before married {fam.married}."
                    print(error)
                    errors.append(error)

            for fam_compare in self.fam_storage.values():
                if fam_compare.married != "NA" and fam.married != "NA":
                    if fam_compare.wifeId == fam.wifeId and \
                            fam_compare.married < fam.married and \
                            (fam_compare.divorced == "NA" or
                             fam_compare.divorced > fam.married):
                        error = f"ERROR: FAMILY: US04: {fam.id}: Wife {fam.wifeId} previous marriage {fam_compare.id} divorced {fam_compare.divorced} after remarried {fam.married}."
                        print(error)
                        errors.append(error)

                    elif fam_compare.husbandId == fam.husbandId and \
                            fam_compare.married < fam.married and \
                            (fam_compare.divorced == "NA" or
                             fam_compare.divorced > fam.married):
                        error = f"ERROR: FAMILY: US04: {fam.id}: Husband {fam.husbandId} previous marriage {fam_compare.id} divorced {fam_compare.divorced} after remarried {fam.married}."
                        print(error)
                        errors.append(error)
        return errors

    # Author: Lehmann Margaret
    def us05(self):
        """ Marriage should occur before death of either spouse """
        errors = []
        for fam in self.fam_storage.values():
            if fam.married != 'NA':
                for indi in self.indi_storage.values():
                    if (indi.id == fam.husbandId or indi.id == fam.wifeId) and indi.death != 'NA' and fam.married >= indi.death:
                        error = f"ERROR: FAMILY: us05: {fam.id}: Marriage date {fam.married} did not occur before death of individual {indi.id} on {indi.death}."
                        print(error)
                        errors.append(error)
        return errors

    # Author: Ibezim Ikenna

    def us22(self):
        """All individual IDs should be unique and all family IDs should be unique --Ikenna"""
        print("This is user story 22")
        d_i = defaultdict(int)
        d_f = defaultdict(int)
        l_i, l_f = [], []
        for offset_1, vals_1 in self.indi_storage.items():

            d_i[vals_1.id] += 1
            for offset_2, vals_2 in d_i.items():
                if vals_2 > 1 and offset_2 == vals_1.id:
                    name = vals_1.name
                    l_i.append(offset_2)
                    print(
                        f"ERROR: US22: ID: {offset_2} is not unique and has another INDIVIDUAL: {name}")

        for offset_1, vals_1 in self.fam_storage.items():
            d_f[vals_1.id] += 1
            for offset_2, vals_2 in d_f.items():
                if vals_2 > 1 and offset_2 == vals_1.id:
                    h_name = vals_1.husbandName
                    w_name = vals_1.wifeName
                    l_f.append(offset_2)
                    print(
                        f"ERROR: US22: ID: {offset_2} is not unique and has another FAMILY: {h_name}, {w_name}")
        return l_i, l_f

    # Author: Ibezim Ikenna
    def us27(self):
        """Include person's current age when listing individuals """
        print("This is user story 27 --Ikenna")
        id_age = []
        for i in self.indi_storage.values():
            id_age.append((i.id, i.age))
        # This prints out a list of indiviuals and their ages included
        print(self.pretty_table_indiv())
        return id_age

    # Author: Ibezim Ikenna
    # def us07(self):

    #     """ Less then 150 years old"""

    #     print("This is user story 07 --Ikenna")
        # alive, death = [], []
        # for val in self.indi_storage.values():
        #     if val.death != "NA" and val.birthday != "NA": # Making sure dead people are less than 150 years old
        #         try:
        #             d_age = val.death.year - val.birthday.year
        #         except AttributeError:
        #             print(f"{val.birthday}")
        #         else:
        #             if d_age >= 150:
        #                 death.append((val.id, d_age))
        #                 print(f"Error US07: Death after birth of {val.name} ({val.id}) was {d_age} years which occurs after 150 years")
        #     elif val.death == "NA" and val.birthday != "NA":
        #         try:
        #             b_age = datetime.today().year - val.birthday.year
        #         except AttributeError:
        #             print(f"{val.birthday}")
        #         else:
        #             if b_age >= 150:
        #                 alive.append((val.id,b_age))
        #                 print(f"Error US07: Current date after birth of {val.name} ({val.id}) was {b_age} years which occurs after 150 years")
        # return death, alive

    # Author: Ibezim Ikenna
    # def us08(self):

    #     """Birth before marriage of parents and within 9 months after divorce"""
    # print("This is user story 08 --Ikenna")
    #     marr_err, div_err = [], []
    #     for val in self.fam_storage.values():
    #         if val.married != "NA":
    #             for val2 in val.children:
    #                 for val3 in self.indi_storage.values():
    #                     if val3.id == val2:
    #                         try:
    #                             if val.married >= val3.birthday: #keeping track of marriage error
    #                                 marr_err.append((val3.id, val.id))
    #                                 print(f"Anomaly US09: Birth date of {val3.name} ({val3.id}) occurs before the marriage date of his parents in Family {val.id}")
    #                         except TypeError:
    #                             continue

    #                         try:
    #                             if val3.birthday > (val.divorced + relativedelta(months=+9)): #keeping track of divorce error
    #                                 div_err.append((val3.id, val.id))
    #                                 print(f"Anomaly US09: Birth date of {val3.name} ({val3.id}) occurs after 9 months of the divorce date of his parents in Family {val.id}")
    #                         except TypeError:
    #                             continue
    #     return (sorted(marr_err), sorted(div_err))

    # def us29(self):

    #     """List all deceased individuals in a GEDCOM file."""

    #     set_deat = set()
    #     for person in self.indi_storage.values():
    #         if person.alive == False:
    #             set_deat.add(person.id)

    #     return set_deat

    # def us30(self):

    #     """List all living married people in a GEDCOM file."""

    #     set_marr = set()
    #     for person in self.indi_storage.values():
    #         if person.alive == True:
    #             alive_id = person.id
    #             for family in self.fam_storage.values():
    #                 if family.husbandId == alive_id or family.wifeId == alive_id and family.married != 'NA':
    #                     set_marr.add(alive_id)
    #     return set_marr


def main():
    """
    Testing
    """
    path = input("Enter file name: ")
    test = GedcomRepo(path)
    test.ged_reader()  # Calling the gedcom file reader

    test.pretty_table_fam()
    test.pretty_table_indiv()

    test.us01()
    test.us02()
    test.us04()
    test.us05()
    test.us27()  # Calling the user story 27 function
    test.us22()  # Calling the user story 22 function
    # test.us07()
    # test.us08()
    # test.us29()
    # test.us30()

    # print('\n\n\n')
    # print("This is the Individuals data in a dictionary format\n\n\n")
    # print(self.indi_storage)
    # print("\n\n\n")

    # print("This is the Family data in a dictionary format\n\n\n")
    # print(self.fam_storage)

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
