"""
Author: Ibezim Ikenna
User function to read files for my homework and display in a pretty table
"""

import string
from collections import Counter
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

    def __init__(self, path, date=datetime.date(datetime.now())) -> None:
        """Initialize printing pretty tables here
        refer to Individual and family here"""
        self.path = path
        self.date = date
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
                            present = datetime.date(datetime.now())
                            # if type(present) == type(self.date_convert(arg.split(" "))) and present < self.date_convert(arg.split(" ")):
                            #     self.indi_storage[indi_counter].alive = True
                            # else:
                            self.indi_storage[indi_counter].death = self.date_convert(
                                arg.split(" "))
                        except AttributeError:
                            print(f"Invalid date: {arg}")
                        else:
                            if self.indi_storage[indi_counter].death != "NA":
                                #print("Death status: ",self.indi_storage[indi_counter].death)
                                self.indi_storage[indi_counter].alive = False
                                if type(present) == type(self.date_convert(arg.split(" "))) and present < self.date_convert(arg.split(" ")):
                                    self.indi_storage[indi_counter].alive = True
                                elif type(self.indi_storage[indi_counter].death) == str:
                                    self.indi_storage[indi_counter].alive = True
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
        present = datetime.date(datetime.now())
        g_date = " ".join(g_date)
        try:
            g_object = datetime.strptime(g_date, "%d %b %Y")
        except (ValueError, AttributeError):
            return(f"Invalid Date: {g_date}")
        if g_object.date() > present:
            print(f"Future Date: {g_date}")
            return(g_object.date())
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

    # Author: McKenzie Christopher
    def us01(self):
        """Dates should not be after the current date."""
        present = datetime.date(datetime.now())
        errors: List[str] = []
        for person in self.indi_storage.values():
            # We say != str to avoid both NA and Invalid Date
            if type(person.birthday) != str and person.birthday > present:
                print(
                    f'ERROR: INDIVIDUAL: US01: {person.id}: Birthday {person.birthday} occurs in the future.')
                errors.append(person.id)

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

    # Author: McKenzie Christopher
    def us02(self):
        """Birth should occur before marriage of an individual."""
        errors: List[str] = []
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

    # Author: Shaffer Wayne
    def us03(self):
        """ Birth must come before death """
        print("This is user story 03 -- Wayne")

        errors = []

        for individual in self.indi_storage.values():
            try:
                if individual.death != "NA" and individual.birthday >= individual.death:
                    error = f"ERROR: Individual: US03: {individual.id}: {individual.name}'s death, {individual.death} occurs before birth, {individual.birthday}"
                    errors.append(error)
                    print(error)
            except TypeError as e:
                print(f'Future; {e}')
        return errors

    # Author: Lehmann Margaret
    def us04(self):
        """ Marriage should occur before divorce of spouses, and divorce can only occur after marriage """
        errors: List[str] = []
        for fam in self.fam_storage.values():
            try:
                if fam.divorced != "NA":
                    if fam.divorced < fam.married:
                        error = f"ERROR: FAMILY: US04: {fam.id}: Divorced {fam.divorced} before married {fam.married}."
                        print(error)
                        errors.append(error)
            except TypeError as e:
                print(f'Future; {e}')
        return errors

    # Author: Lehmann Margaret
    def us05(self):
        """ Marriage should occur before death of either spouse """
        errors = []
        for fam in self.fam_storage.values():
            if fam.married != 'NA':
                for indi in self.indi_storage.values():
                    if (indi.id == fam.husbandId or indi.id == fam.wifeId) and indi.death != 'NA' and fam.married >= indi.death:
                        error = f"ERROR: FAMILY: US05: {fam.id}: Marriage date {fam.married} did not occur before death of individual {indi.id} on {indi.death}."
                        print(error)
                        errors.append(error)
        return errors

    # Author Shaffer Wayne
    def us06(self):
        """ Divorce must be before death for each individual """
        print("This is user story 06")
        errors = []

        # for all dead people
        for individual in [individual for individual in self.indi_storage.values() if individual.death != "NA"]:
            # for all divorced families
            for family in [family for family in self.fam_storage.values() if family.divorced != "NA"]:
                if individual.id == family.husbandId or \
                        individual.id == family.wifeId:
                    if family.divorced >= individual.death:
                        error = f"ERROR: US06: FAMILY: {individual.name}'s divorce, {family.divorced}, is not before deathdate, {individual.death}"
                        errors.append(error)
                        print(error)
        return errors

    # Author: Ibezim Ikenna
    def us07(self):
        """ Less then 150 years old"""
        print("This is user story 07 --Ikenna")
        alive, death = [], []

        for val in self.indi_storage.values():
            if val.death != "NA" and val.birthday != "NA":  # Making sure dead people are less than 150 years old
                try:
                    d_age = val.death.year - val.birthday.year
                except AttributeError:
                    print(f"{val.birthday}")
                else:
                    if d_age >= 150:
                        death.append((val.id, d_age))
                        print(
                            f"Error US07: Death after birth of {val.name} ({val.id}) was {d_age} years which occurs after 150 years")
            elif val.death == "NA" and val.birthday != "NA":
                try:
                    b_age = datetime.today().year - val.birthday.year
                except AttributeError:
                    print(f"{val.birthday}")
                else:
                    if b_age >= 150:
                        alive.append((val.id, b_age))
                        print(
                            f"Error US07: Current date after birth of {val.name} ({val.id}) was {b_age} years which occurs after 150 years")
        return death, alive

    # Author: Ibezim Ikenna
    def us08(self):
        """Birth before marriage of parents and within 9 months after divorce"""
        print("This is user story 08 --Ikenna")
        marr_err, div_err = [], []

        for val in self.fam_storage.values():
            if val.married != "NA":
                for val2 in val.children:
                    for val3 in self.indi_storage.values():
                        if val3.id == val2:
                            try:
                                if val.married >= val3.birthday:  # keeping track of marriage error
                                    marr_err.append((val3.id, val.id))
                                    print(
                                        f"Anomaly US08: Birth date of {val3.name} ({val3.id}) occurs before the marriage date of his parents in Family {val.id}")
                            except TypeError:
                                continue

                            try:
                                # keeping track of divorce error
                                if val3.birthday > (val.divorced + relativedelta(months=+9)):
                                    div_err.append((val3.id, val.id))
                                    print(
                                        f"Anomaly US08: Birth date of {val3.name} ({val3.id}) occurs after 9 months of the divorce date of his parents in Family {val.id}")
                            except TypeError:
                                continue
        return (sorted(marr_err), sorted(div_err))

    # Author: Lehmann Margaret
    def us09(self):
        """ Child should be born before death of mother and before 9 months after death of father """
        errors = []
        for family in self.fam_storage.values():
            for child_id in family.children:
                child = "NA"
                mother = "NA"
                father = "NA"
                for indi in self.indi_storage.values():
                    if indi.id == child_id:
                        child = indi
                    elif indi.id == family.wifeId:
                        mother = indi
                    elif indi.id == family.husbandId:
                        father = indi

                if child != "NA" and child.birthday != "NA":
                    if mother != "NA" and mother.death != "NA" and mother.death < child.birthday:
                        error = f"ERROR: US09: FAMILY: {family.id}: Mother died {mother.death}, before the birth of child {child.id} on {child.birthday}."
                        print(error)
                        errors.append(error)
                    if father != "NA" and father.death != "NA" and (father.death + relativedelta(months=9)) < child.birthday:
                        error = f"ERROR: US09: FAMILY: {family.id}: Father died {father.death}, over 9 months before the birth of child {child.id} on {child.birthday}."
                        print(error)
                        errors.append(error)

        return errors

    # Author: Lehmann Margaret
    def us10(self):
        """ Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old) """
        errors = []
        for family in self.fam_storage.values():
            wife = "NA"
            husband = "NA"
            for individual in self.indi_storage.values():
                if family.wifeId == individual.id:
                    wife = individual
                elif family.husbandId == individual.id:
                    husband = individual

            if family.married != "NA":
                if wife != "NA" and wife.birthday != "NA" and family.married < wife.birthday + relativedelta(years=14):
                    error = f"ERROR: US10: FAMILY: {family.id}: Wife was born {wife.birthday}, less than 14 years before she was married {family.married}."
                    print(error)
                    errors.append(error)
                if husband != "NA" and husband.birthday != "NA" and family.married < husband.birthday + relativedelta(years=14):
                    error = f"ERROR: US10: FAMILY: {family.id}: Husband was born {husband.birthday}, less than 14 years before he was married {family.married}."
                    print(error)
                    errors.append(error)

        return errors

    # Author: Ibezim Ikenna
    def us11(self):
        """Marriage should not occur during marriage to another spouse"""
        print("This is user story 11 --Ikenna")
        marr_storage = defaultdict(int)
        error = []
        for indiv in self.fam_storage.values():
            if type(indiv.married) != str and indiv.divorced == 'NA':
                marr_storage[indiv.husbandId] += 1
                marr_storage[indiv.wifeId] += 1

        for offset, value in marr_storage.items():
            if value > 1:
                error.append(offset)
                print(
                    f"Error US11: INDIVIDUAL: ID: {offset} is married to another family while still in another :MARRIAGE")
        return error

    # Author: Shaffer Wayne
    def us12(self):
        """ Compares ages of parents to ages of their children.
            - Mother must not be more than 60 years older than her children.
            - Father must not be more than 80 years older than his children.
        """
        print("This is user story US12 - Wayne")

        error_families = []

        fams_with_children = [family for family in self.fam_storage.values()
                              if len(family.children) > 0]

        for family in fams_with_children:
            for individual in self.indi_storage.values():
                if individual.id == family.husbandId:
                    husband = individual
                if individual.id == family.wifeId:
                    wife = individual

            children = [child for child in self.indi_storage.values()
                        if child.id in family.children]

            # find youngest child
            youngest_child = None
            sorted_children = sorted(
                children, key=lambda i: str(i.age), reverse=True)
            for child in sorted_children:
                if child.age != "NA":
                    youngest_child = child

            if youngest_child == None:
                error = f"""ERROR: US12: FAMILY: {family.id}:
                            This family has no listed ages for any of its {len(children)} children.
                            Comparison not possible."""
                print(error)
                error_families.append(family.id)

            else:
                # now compare husband/wife ages
                try:
                    if wife.age - youngest_child.age >= 60:  # Used an exception to handle comparisons
                        error = f"""ERROR: US12: FAMILY: {family.id}:
                                    Wife {wife.name} was born {wife.birthday}, more than 60 years
                                    before her youngest child {youngest_child.name},
                                    who was born on {youngest_child.birthday}."""
                        print(error)
                        error_families.append(family.id)
                except TypeError:
                    continue

                if husband.age - youngest_child.age >= 80:
                    error = f"""ERROR: US12: FAMILY: {family.id}:
                                Husband {husband.name} was born {husband.birthday}, more than 80 years
                                before his youngest child {youngest_child.name},
                                who was born on {youngest_child.birthday}."""
                    print(error)
                    error_families.append(family.id)

        return error_families

    # Author: Ibezim Ikenna
    def us14(self):
        """No more than five siblings should be born at the same time"""
        print("This is user story 14 --Ikenna")
        error = []
        for i in self.fam_storage.values():
            if len(i.children) > 5:  # making sure a family have more than 5 kids
                date_storage = defaultdict(int)
                for j in i.children:
                    for k in self.indi_storage.values():
                        if k.id == j:
                            date_storage[k.birthday] += 1
                        else:
                            continue
                    else:
                        for offset3, value in date_storage.items():
                            if value > 5:
                                error.append(i.id)
                                print(
                                    f"Anomaly US14: FAMILY: ID: {i.id} has more than 5 sibling born at the same time")
            else:
                continue
        else:
            return error

    # Author: Lehmann Margaret
    def us15(self):
        """ There should be fewer than 15 siblings in a family """
        errors = []
        for fam in self.fam_storage.values():
            if len(fam.children) >= 15:
                error = f"ERROR: FAMILY: US15: {fam.id}: Family has {len(fam.children)} which is greater thn 14 children."
                print(error)
                errors.append(error)
        return errors

    # Author Shaffer Wayne
    def us16(self):
        """All males in a family must have the same last name."""

        print("This is user story 16 -- Wayne")

        wrong_names = []

        for family in self.fam_storage.values():
            #find the husband to find the family name
            for person in self.indi_storage.values():
                if person.id == family.husbandId:
                    family_name = person.name.split(" ")[1].strip("/")
                    
            #make sure male children have same last name
            children = [individual for individual in self.indi_storage.values()
                        if individual.id in family.children]
            for child in children:
                if child.gender == "M":
                    last_name = child.name.split(" ")[1].strip("/") 
                    if last_name != family_name:
                        error = f"""ERROR: US16: FAMILY: {family.id}: {family_name} family:
                            {child.name} has the wrong last name: {last_name}"""
                        print(error)
                        wrong_names.append(child.id)

        return wrong_names

    # Author: McKenzie Christopher
    def us17(self):
        """Parents should not marry any of their children."""

        couple = defaultdict()  # Tracks children for every individual
        deaths = dict()  # Death counter to check if death occurs before marriage
        errors: List[str] = []

        # Stores death dates
        for individual in self.indi_storage.values():
            deaths[individual.id] = individual.death

        # Need to two for loops to track children for both mother and father in defaultdict
        for family in self.fam_storage.values():
            if family.husbandId not in couple.keys():
                couple[family.husbandId] = family.children
            couple[family.husbandId].union(family.children)

        for family in self.fam_storage.values():
            if family.wifeId not in couple.keys():
                couple[family.wifeId] = family.children
            couple[family.wifeId].union(family.children)

            # Checks married couples with valid marriage dates.
            # Uses two separate if statements to specify who is the parent and child
            if family.husbandId in couple[family.wifeId] and type(family.married) != str:

                # If statement does not print error if death of spouse occurs before marriage
                if (type(deaths[family.husbandId]) != str and deaths[family.husbandId] < family.married) or \
                        (type(deaths[family.wifeId]) != str and deaths[family.wifeId] < family.married):
                    continue

                else:
                    print(
                        f"ERROR: FAMILY: US17: {family.id}: Mother {family.wifeId} married son {family.husbandId}.")
                errors.append(family.id)

            elif family.wifeId in couple[family.husbandId] and type(family.married) != str:

                # If statement does not print error if death of spouse occurs before marriage
                if (type(deaths[family.husbandId]) != str and deaths[family.husbandId] < family.married) or \
                        (type(deaths[family.wifeId]) != str and deaths[family.wifeId] < family.married):
                    continue

                else:
                    print(
                        f"ERROR: FAMILY: US17: {family.id}: Father {family.husbandId} married daughter {family.wifeId}.")
                    errors.append(family.id)

        return errors

    # Author: McKenzie Christopher
    def us18(self):
        """Siblings should not marry one another."""

        sibling = defaultdict()
        deaths = dict()  # Death counter to check if death occurs before marriage
        errors: List[str] = []

        # Stores both children and death dates
        for indi in self.indi_storage.values():

            if indi.id not in sibling.keys():
                sibling[indi.id] = (indi.child)
            sibling[indi.id].union(indi.child)
            deaths[indi.id] = indi.death

        for fam in self.fam_storage.values():

            # If statement checks if family has valid marriage date and if husband/wife ID in indi storage
            if type(fam.married) != str and fam.husbandId in sibling and fam.wifeId in sibling:

                # If statement does not print error if death occurs before marriage
                if (type(deaths[fam.husbandId]) != str and deaths[fam.husbandId] < fam.married) or \
                        (type(deaths[fam.wifeId]) != str and deaths[fam.wifeId] < fam.married):
                    continue

                # Checks if husband and wife are children of the same family
                elif fam.husbandId in sibling and fam.wifeId in sibling:
                    if sibling[fam.husbandId] == sibling[fam.wifeId] and \
                            sibling[fam.husbandId] != set() and \
                            type(fam.married) != str:
                        print(
                            f"ERROR: FAMILY: US18: {fam.id}: Brother {fam.husbandId} married sister {fam.wifeId}.")
                        errors.append(fam.id)

        return errors

    # Author: Shaffer Wayne

    def us21(self):
        """ In all families, father should be male, and mother should be female. """

        error_families = []

        print("This is user story 21 -- Wayne")

        for family in self.fam_storage.values():
            # identify husband and wife
            for individual in self.indi_storage.values():
                if individual.id == family.husbandId:
                    husband = individual
                if individual.id == family.wifeId:
                    wife = individual

            if husband.gender != "M":
                error = f"""ERROR: US21: FAMILY: {family.id}:
                            {husband.name} is the wrong gender!"""
                print(error)
                error_families.append(husband.id)

            if wife.gender != "F":
                error = f"""ERROR: US21: FAMILY: {family.id}:
                            {wife.name} is the wrong gender!"""
                print(error)
                error_families.append(wife.id)

        return error_families

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
    def us23(self):
        """Unique name and birth date"""
        print("This is user story 23 --Ikenna")
        indi_storage1, error = [], []
        indi_storage2 = defaultdict(int)
        for i in self.indi_storage.values():
            indi_storage1.append((i.name, i.birthday))
        for j in indi_storage1:
            indi_storage2[j] += 1
        for k1, v1 in indi_storage2.items():
            if int(v1) > 1:
                error.append(k1)
                print(
                    f"Error: US23: The Individual {k1[0]} with birthday {k1[1]} is not unique and has been repeated {v1} times in the Gedcom file")
        return error

    # Author: Shaffer Wayne
    def us25(self):
        """No more than one child in a family should have the same name and birthdate."""
        fail_list = [] #list of kids that fail the story

        print("This is user story 25 -- Wayne")

        fams_with_children = [family for family in self.fam_storage.values()
                              if len(family.children) > 0]

        for family in fams_with_children:
            children = [person for person in self.indi_storage.values()
                        if person.id in family.children]
            
            for child in children[:]:
                # compare this child to the rest of the children
                for other_child in children[1:]:
                    if child.birthday != "NA" and other_child.birthday != "NA":
                        if child.name == other_child.name and \
                                child.birthday == other_child.birthday:
                            error = f"""ERROR: FAMILY: {family.id}:
                                        Two or more children exist named {child.name}
                                        with birthdate {child.birthday}
                                    """
                            print(error)
                            fail_list.append(child.id)

                children.remove(child)

        return fail_list

    # Author: Ibezim Ikenna
    def us27(self):
        """Include person's current age when listing individuals """
        print("This is user story 27 --Ikenna")
        id_age = []

        for i in self.indi_storage.values():
            id_age.append((i.id, i.age))
        # This prints out a list of indiviuals and their ages included
        else:
            print(self.pretty_table_indiv())
        return id_age

    # Author: Shaffer Wayne
    def us28(self):
        """ List children from each family by age, oldest first. """

        print("This is user story US28 - Wayne")

        full_list = []

        fams_with_children = [family for family in self.fam_storage.values()
                              if len(family.children) > 0]

        for family in fams_with_children:
            children = [child for child in self.indi_storage.values()
                        if child.id in family.children]

            # Sort children, oldest first
            sorted_children = sorted(
                children, key=lambda i: str(i.age), reverse=True)

            print(f"Family: {family.id}")

            # Print sorted list of children
            for child in sorted_children:
                print(f"{child.name} :- {child.age} yrs old.")

            full_list.append([(child.name, child.age)
                              for child in sorted_children])

        return full_list

    # Author: McKenzie Christopher
    def us29(self):
        """List all deceased individuals in a GEDCOM file."""

        present = datetime.date(datetime.now())
        set_deat = set()
        for person in self.indi_storage.values():
            if person.alive == False:
                set_deat.add(person.id)

        print(f'US29: List of all deceased individuals people: {set_deat}')
        return set_deat

    # Author: McKenzie Christopher
    def us30(self):
        """List all living married people in a GEDCOM file."""

        present = datetime.date(datetime.now())
        set_marr = set()
        for person in self.indi_storage.values():
            if person.alive == True:
                alive_id = person.id
                for family in self.fam_storage.values():
                    if type(family.married) != str:  # Does not include Invalid Dates and NA

                        if family.husbandId == alive_id or family.wifeId == alive_id:
                            set_marr.add(alive_id)

                            if family.married > present:  # Does not include future marriage dates
                                set_marr.remove(alive_id)

                            elif type(family.divorced) == type(present) and family.divorced < present:
                                set_marr.remove(alive_id)

        print(f'US30: List of all living married people: {set_marr}')
        return set_marr

    # Author: Lehmann Margaret
    def us31(self):
        """ List all living people over 30 who have never been married in a GEDCOM file """
        set_single = set()
        for indi in self.indi_storage.values():
            if indi.alive and indi.age != 'NA' and indi.age >= 30:
                indi_single = True
                for fam in self.fam_storage.values():
                    if indi.id == fam.wifeId or indi.id == fam.husbandId:
                        indi_single = False
                if indi_single:
                    set_single.add(indi.id)
        print(
            f'US31: List of all living people over 30 who were never married: {set_single}')

        return set_single

    # Author: Shaffer Wayne
    def us32(self):
        """ List multiple births from each family. """

        print("This is user story US32 - Wayne")

        multi_births = []

        fams_with_children = [family for family in self.fam_storage.values()
                              if len(family.children) > 0]

        for family in fams_with_children:
            bdates = []
            children = [child for child in self.indi_storage.values()
                        if child.id in family.children]

            for child in children:
                if child.birthday == "NA" or child.birthday == "":
                    error = f"ERROR: US32: FAMILY: {family.id}: {child.id} doesn't have a birthdate!"
                    print(error)
                else:
                    bdates.append(child.birthday)

            c = Counter(bdates)
            for date in c:
                if c[date] > 1:
                    print(
                        f"Multiple births found in family {family.id} on {date}")
                    multi_births.append(str(date))

        return multi_births

    # Author: Ibezim Ikenna
    def us33(self):
        """List orphans"""
        print("This is user story 33 --Ikenna")
        error = []
        child = dict()
        for i in self.indi_storage.values():
            for f in self.fam_storage.values():
                if i.id == f.husbandId:
                    father = f.husbandId
                    father_alive = i.alive
                elif i.id == f.wifeId:
                    wife = f.wifeId
                    wife_alive = i.alive
                else:
                    continue
                if father_alive == False and wife_alive == False:
                    children = f.children
                    for c in children:
                        for j in self.indi_storage.values():
                            if j.id == c:
                                child[c] = j.age
        else:
            for offset, val in child.items():
                if val < 18:
                    print(
                        f"ANOMALITY: CHILD: {offset} is {val} years old and an orphan from the FAMILY: {f.id}")
                    error.append((offset, val))
            return sorted(error)

    # Author: Lehmann Margaret
    def us35(self):
        """ List all people in a GEDCOM file who were born in the last 30 days """
        people = set()
        for person in self.indi_storage.values():
            if type(person.birthday) != str and person.birthday <= self.date and person.birthday > self.date - relativedelta(days=30):
                people.add(person.id)
        print(f'US35: List of people born in the last 30 days: {people}')
        return people

    # Author: Lehmann Margaret
    def us36(self):
        """ List all people in a GEDCOM file who died in the last 30 days """
        people = set()
        for person in self.indi_storage.values():
            if type(person.death) != str and person.death <= self.date and person.death > self.date - relativedelta(days=30):
                people.add(person.id)
        print(f'US35: List of people who died in the last 30 days: {people}')
        return people

    # Author: McKenzie Christopher
    def us38(self):
        """List all living people in a GEDCOM file whose birthdays
        occur in the next 30 days."""

        present = datetime.now()
        set_bday = set()

        for person in self.indi_storage.values():
            if person.alive == True and type(person.birthday) != str \
                and (person.birthday).year < present.year: # Last 'and' statement avoids future birthdays
                # Convert birthday year to present year to compare by days
                bday = datetime(
                    present.year, (person.birthday).month, (person.birthday).day).date()

                if bday >= self.date and bday < self.date + relativedelta(days=30):
                    set_bday.add(person.id)

        print(f'US38: List of individuals with upcoming birthdays: {set_bday}')
        return set_bday

    def us39(self):
        """List all living couples in a GEDCOM file whose marriage
        anniversaries occur in the next 30 days."""

        present = datetime.now()
        set_anni = set()

        for family in self.fam_storage.values():
            # Includes it if either NA or invalid date (also means not divorced)
            # Also includes families with future divorce dates (invalid divorce date)
            if type(family.divorced) == str or (family.divorced) > present.date():
                # Avoids invalid and future marriages
                if type(family.married) != str and (family.married).year < present.year:
                    for person in self.indi_storage.values():
                        if person.alive == True:

                            # Convert birthday year to present's year to compare by days
                            anni = datetime(
                                present.year, (family.married).month, (family.married).day).date()

                            if anni >= self.date and anni < self.date + relativedelta(days=30):
                                set_anni.add(family.id)

                        elif person.alive == False and family.id in set_anni:
                            # Removes from set if either husband or spouse is dead
                            set_anni.remove(family.id)
        

        print(
            f'US39: List of families with upcoming anniversaries : {set_anni}')
        return set_anni


def main():
    """
    Testing
    """
    path = input("Enter file name: ")

    test = GedcomRepo(path)
    test.ged_reader()  # Calling the gedcom file reader
    print('\n\n\n')
    test.pretty_table_indiv()
    test.pretty_table_fam()
    print("\n\n\n")

    print("Our user stories begin here!!!!!")
    print("\n\n\n")

    test.us01()
    test.us02()
    test.us03()
    test.us04()
    test.us05()
    test.us06()
    test.us07()
    test.us08()
    test.us09()
    test.us10()
    test.us11()
    test.us12()
    test.us14()
    test.us15()
    test.us16()
    test.us17()
    test.us18()
    test.us21()
    test.us22()
    test.us23()
    test.us25()
    test.us27()
    test.us28()
    test.us29()
    test.us30()
    test.us31()
    test.us32()
    test.us33()
    test.us35()
    test.us36()
    test.us38()
    test.us39()

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
