import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
from datetime import datetime
from prettytable import PrettyTable
from collections import defaultdict
from typing import List


class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """

    def setUp(self):
        """ Initial setup code for unit tests """

        self.test: GedcomRepo = GedcomRepo("family.ged")
        self.test.ged_reader()

    # Author: McKenzie Christopher
    def test_us01(self):
        """Tests that dates do not occur before current date."""

        present: datetime.date = datetime.date(datetime.now())
        errors: List[str] = ['US01_I11', 'US01_I17', 'US01_F4', 'US01_F8']
        self.assertEqual(self.test.us01(), errors)

        """Tests the following boundaries:
        1. Missing/incorrectly formatted death date for dead individual
        2. Missing/incorrectly formatted birthday
        3. Missing/incorrectly formatted divorce date
        4. Missing/incorrectly formatted marriage date."""

        bounds: GedcomRepo = GedcomRepo("us01_us02_bounds.ged")
        bounds.ged_reader()
        b_errors: List[str] = ['US01_I17', 'US01_F8']
        self.assertEqual(bounds.us01(), b_errors)

    # Author: McKenzie Christopher
    def test_us02(self):
        """Tests that marriage only occurs after birth."""

        errors = ['I13', 'I14']
        self.assertEqual(self.test.us02(), errors)

        """Tests the following boundaries:
        1. Missing/incorrectly formatted death date for dead individual
        2. Missing/incorrectly formatted birthday
        3. Missing/incorrectly formatted divorce date
        4. Missing/incorrectly formatted marriage date."""

        bounds: GedcomRepo = GedcomRepo("us01_us02_bounds.ged") #Tests missing death dates for dead people and birthdays
        bounds.ged_reader()
        b_errors: List[str] = ['I14']
        self.assertEqual(bounds.us02(), b_errors)

    # Author: Shaffer Wayne
    def test_us03(self):
        """ Tests birth before death """
        error_list = self.test.us03()
        assert(len(error_list) > 0)

    # Author: Lehmann Margaret

    def test_us04(self):
        """ Tests marriage before divorce """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(self.test.us04()), 1)

    # Author: Lehmann Margaret
    def test_us05(self):
        """ Tests marriagne before death """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(self.test.us05()), 2)

    # Author: Shaffer Wayne
    def test_us06(self):
        """ Tests divorce before death for each individual """
        self.assertTrue(len(self.test.us06()) > 0)

    # Author: Ibezim Ikenna
    def test_us22(self):
        """function to test the id duplicates"""
        ind_id_duplicates, fam_id_duplicates, error = ['I1', 'US01_I17', 'I15', 'I15'], [
            'US01_F8', 'F9'], ['0r', 'US01_I1', 'I17', 'I15', 'I15']
        # Testing duplicates ID for individual table
        my_func = self.test.us22()
        self.assertEqual(my_func[0],  ind_id_duplicates)
        # Testing duplicates ID for family table
        self.assertEqual(my_func[1],  fam_id_duplicates)
        # Testing for errors
        self.assertNotEqual(my_func[0],  error)

    # Author: Ibezim Ikenna
    def test_us27(self):
        """function to test for individual complete data"""
        #test = GedcomRepo("family.ged")
        # test.ged_reader()
        id_age, error = [('I1', "NA"), ('I2', 69),
                         ('I3', 68), ('I4', 40),
                         ('I5', 32), ('I6', 170), ('I7', 32), ('I8', 3),
                         ('I9', 43), ('I10', 18), ('US01_I11', 47), ('I12', 112),
                         ('I13', 67), ('I14', 64), ('I15', 65), ('I16', 0),
                         ('US01_I17', -30), ('I1', 65), ('US01_I17', 71), ('I15', 65),
                         ('I15', 65)
                         ], []
        my_func = self.test.us27()

        self.assertEqual(my_func,  id_age)
        self.assertNotEqual(my_func,  error)

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
    main()
