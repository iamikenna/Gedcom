import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
from datetime import datetime
from prettytable import PrettyTable  # Used to build a table
from collections import defaultdict


class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """
    
    # Author: Christopher McKenzie
    # def test_us01(self):
        
    #     """Tests that dates do not occur before current date."""

    #     test: GedcomRepo = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     present: date = datetime.date(datetime.now())
        
    #     #exp_bday = 
    #     #exp_deat = 
    #     #exp_marr =
    #     exp_div = {f'ERROR: FAMILY: US01: F3: Divorce 1945-07-10 occurs in the future.'}
        
    #     prd_bday = {f'ERROR: INDIVIDUAL: US01: {person.id}: {person.name}: Birthday {person.birthday} occurs in the future.'\
    #         for person in test.indi_storage.values() if type(person.birthday) != str\
    #         and person.birthday > present}
            
    #     prd_deat = {f'ERROR: INDIVIDUAL: US01: {person.id}: {person.name}: Death {person.death} occurs in the future.'\
    #         for person in test.indi_storage.values() if type(person.death) != str\
    #         and person.death !='NA'\
    #         and person.death > present}

    #     prd_marr = {f'ERROR: FAMILY: US01: {family.id}: Marriage {family.married} occurs in the future.'\
    #         for family in test.fam_storage.values() if type(family.married) != str\
    #         and family.married !='NA'\
    #         and family.married > present}

    #     prd_div = {f'ERROR: FAMILY: US01: {family.id}: Divorce {family.divorced} occurs in the future.'\
    #         for family in test.fam_storage.values() if type(family.divorced) != str\
    #         and family.divorced !='NA'\
    #         and family.divorced < present}
        
    #     #self.assertEqual(exp_bday, prd_bday)
    #     #self.assertEqual(exp_deat, prd_deat)
    #     #self.assertEqual(exp_marr, prd_marr)
    #     #self.assertEqual(exp_div, prd_div)
            
    # Author: Christopher McKenzie
    # def test_us02(self):
        
    #     """Tests that marriage only occurs after birth."""
        
    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     errors = ['I2', 'I3', 'I12', 'I13', 'I13', 'I14', 'I4', 'I9', 'I14', 'I16']

    #     self.assertEqual(test.us02(), errors)


    # Author: Lehmann Margaret
    def test_us04(self):
        """ Tests marriage before divorce """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us04()), 3)

    # Author: Lehmann Margaret
    def test_us05(self):
        """ Tests marriagne before death """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us05()), 1)

    # Author: Ibezim Ikenna
    def test_us22(self):
        """function to test the id duplicates"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        ind_id_duplicates, fam_id_duplicates, error = ['I1', 'I17', 'I15', 'I15'], [
            'F8', 'F9'], ['0r', 'I1', 'I17', 'I15', 'I15']
        # Testing duplicates ID for individual table
        self.assertEqual(test.us22()[0],  ind_id_duplicates)
        # Testing duplicates ID for family table
        self.assertEqual(test.us22()[1],  fam_id_duplicates)
        #Testing for errors
        self.assertNotEqual(test.us22()[0],  error)

    # Author: Ibezim Ikenna
    def test_us27(self):
        """function to test for individual complete data"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        id_age, error = [('I1', "NA"), ('I2', 69),
                         ('I3', 68), ('I4', 40),
                         ('I5', 32), ('I6', 170), ('I7', 32), ('I8', 3),
                         ('I9', 43), ('I10', 18), ('I11', 17), ('I12', 112),
                         ('I13', 95), ('I14', 103), ('I15', 65), ('I16', 23),
                         ('I17', 71), ('I1', 65), ('I17', 71), ('I15', 65),
                         ('I15', 65)
                         ], []
       
        self.assertEqual(test.us27(),  id_age)
        self.assertNotEqual(test.us27(),  error)
    
    
    

    # Author: Ibezim Ikenna
    # def test_us07(self):

    #     """Checking for less than 150 years """

    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
        # death, alive, error = [('I12', 153)],
        #                     [('I6', 170)],
        #                     ['0r','I1', 'I17', 'I15', 'I15']
    #     self.assertEqual(test.us07()[0],  death)
    #     self.assertNotEqual(test.us07()[0],  error)
    #     self.assertEqual(test.us07()[1],  alive)

    # Author: Ibezim Ikenna
    # def test_us08(self):

    #     """ Birth before marriage of parents"""

    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     marr_ex = sorted([('I6', 'F2'), ('I1', 'F2'), ('I2', 'F3'), ('I15', 'F7'), ('I15', 'F7'), ('I15', 'F7')])
    #     div_ex = sorted([('I2', 'F3')])
    #     error = []
    #     self.assertEqual(test.us08()[0],  marr_ex)
    #     self.assertEqual(test.us08()[1],  div_ex)
    #     self.assertNotEqual(test.us08(),  error)


    # #Author: Christopher McKenzie
    # def test_us29(self):

    #     set_deat = {'I16', 'I12'}
    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     self.assertEqual(test.us29(), set_deat)

    # #Author: Christopher McKenzie
    # def test_us30(self):

    #     set_marr = {'I13', 'I9', 'I2', 'I6', 'I15', 'I1', 'I4', 'I14', 'I3'}
    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     self.assertEqual(test.us30(), set_marr)



if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
