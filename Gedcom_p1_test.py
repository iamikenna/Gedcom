import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
from datetime import datetime
from prettytable import PrettyTable
from collections import defaultdict
from typing import List


class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """

    # Author: McKenzie Christopher
    def test_us01(self):
        """Tests that dates do not occur before current date."""
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()

        present: datetime.date = datetime.date(datetime.now())
        errors: List[str] = ['US01_I11', 'US01_I17', 'US01_F4', 'US01_F8']
        self.assertEqual(test.us01(), errors)

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
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()

        errors = ['I13', 'I14']
        self.assertEqual(test.us02(), errors)

        """Tests the following boundaries:
        1. Missing/incorrectly formatted death date for dead individual
        2. Missing/incorrectly formatted birthday
        3. Missing/incorrectly formatted divorce date
        4. Missing/incorrectly formatted marriage date."""

        # Tests missing death dates for dead people and birthdays
        bounds: GedcomRepo = GedcomRepo("us01_us02_bounds.ged")
        bounds.ged_reader()
        b_errors: List[str] = ['I14']
        self.assertEqual(bounds.us02(), b_errors)

    # Author: Shaffer Wayne
    def test_us03(self):
        """ Tests birth before death """
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()
        error_list = test.us03()
        assert(len(error_list) > 0)

    # Author: Lehmann Margaret
    def test_us04(self):
        """ Tests marriage before divorce """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us04()), 1)

    # Author: Lehmann Margaret
    def test_us05(self):
        """ Tests marriage before death """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us05()), 2)

    # Author: Shaffer Wayne
    def test_us06(self):
        """ Tests divorce before death for each individual """
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertTrue(len(test.us06()) > 0)

    # Author: Ibezim Ikenna
    def test_us07(self):
        """Checking for less than 150 years """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        death, alive, error = [('US07_I1', 200), ('US07_I0886', 198)], [
            ('I6', 170)], ['0r', 'I1', 'I17', 'I15', 'I15']
        my_func = test.us07()
        self.assertEqual(my_func[0],  death)
        self.assertNotEqual(my_func[0],  error)
        self.assertEqual(my_func[1],  alive)

    # Author: Ibezim Ikenna
    def test_us08(self):
        """ Birth before marriage of parents"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        marr_ex = sorted([('I6', 'F2'), ('I15', 'US02_F7'), ('I2', 'US02_F3'),
                          ('I15', 'US02_F7'), ('I1', 'F2'), ('I15', 'US02_F7')])
        div_ex = sorted([('I2', 'US02_F3')])
        error = []
        my_func = test.us08()
        self.assertEqual(my_func[0],  marr_ex)
        self.assertEqual(my_func[1],  div_ex)
        self.assertNotEqual(my_func,  error)

    # Author: Lehmann Margaret
    def test_us09(self):
        """ Tests child born before death of parents """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us09()), 3)

    # Author: Lehmann Margaret
    def test_us10(self):
        """ Tests marriage atleast 14 years old"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us10()), 4)

    # Author: Ibezim Ikenna
    # def test_us11(self):
    #     """Marriage should not occur during marriage to another spouse"""
    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     couples = ['us_11_I13']
    #     error = []
    #     my_func = test.us11()
    #     self.assertEqual(my_func,  couples)
    #     self.assertNotEqual(my_func,  error)

    # Author: Ibezim Ikenna
    # def test_us14(self):
    #     """No more than five siblings should be born at the same time --Ikenna"""
    #     test = GedcomRepo("family.ged")
    #     test.ged_reader()
    #     family = ['us14_F2']
    #     error = []
    #     my_func = test.us14()

    #     self.assertEqual(my_func,  family)
    #     self.assertNotEqual(my_func,  error)

    # Author: Ibezim Ikenna

    def test_us22(self):
        """function to test the id duplicates"""
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()
        ind_id_duplicates, fam_id_duplicates, error = ['I1', 'US01_I17', 'I15', 'I15'], [
            'US01_F8', 'F9'], ['0r', 'US01_I1', 'I17', 'I15', 'I15']
        # Testing duplicates ID for individual table
        my_func = test.us22()
        self.assertEqual(my_func[0],  ind_id_duplicates)
        # Testing duplicates ID for family table
        self.assertEqual(my_func[1],  fam_id_duplicates)
        # Testing for errors
        self.assertNotEqual(my_func[0],  error)

    # Author: Ibezim Ikenna
    def test_us27(self):
        """function to test for individual complete data"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        id_age, error = [('I1', "NA"), ('US07_I1', 200),
                         ('US07_I0886', 198), ('I2', 69),
                         ('I3', 68), ('I4', 40),
                         ('I5', 32), ('I6', 170), ('I7', 32), ('I8', 3),
                         ('I9', 43), ('I10', 18), ('US01_I11', 47), ('I12', 112),
                         ('I13', 67), ('I14', 64), ('I15', 65), ('I16', 0),
                         ('US01_I17', -30), ('I1', 65), ('US01_I17', 71), ('I15', 65),
                         ('I15', 65), ('us14_I9', 2), ('us14_I4', 2), ('us14_I5', 2),
                         ('us14_20', 2), ('us14_I6', 2), ('us14_I8', 2),
                         ('US09_I1', 28), ('US09_I2', 48), ('US09_I3', 27),
                         ('US09_I4', 30), ('US09_I5', 72), ('US09_I6', 42),
                         ('US09_I7', 40), ('US09_I8', 35), ('US09_I9', 70)
                         ], []
        my_func = test.us27()

        self.assertEqual(my_func,  id_age)
        self.assertNotEqual(my_func,  error)

    # Author: Christopher McKenzie
    def test_us29(self):
        """Tests if function lists all dead individuals."""

        set_deat = {'US09_I3', 'I16', 'US09_I4', 'US09_I8', 'US07_I0886', 'US07_I1', 'I12'}
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(test.us29(), set_deat)

        """Below tests the following boundaries:
        1. Missing death date
        2. Future death date
        3. Living individual with death date
        4. Invalid death date."""

        bounds: GedcomRepo = GedcomRepo("us29_us30.ged")
        bounds.ged_reader()
        b_set = {'US29_US30_I11', 'US30_I2', 'I12', 'US30_I4', 'US07_I0886'}
        self.assertEqual(bounds.us29(), b_set)

    # Author: Christopher McKenzie
    def test_us30(self):
        """Tests if function lists all living married people."""

        set_marr = {'I2', 'I15', 'I1', 'I3', 'US09_I2', 'I4', 'I6', 'US09_I6', 'I9', 'US09_I7'}
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(test.us30(), set_marr)

        """Below tests the following boundaries:
        1. Married but one spouse dead
        2. Future death date
        3. Living individual with death date
        4. Missing marriage date
        5. Future marriage date
        6. Invalid death date
        7. Invalid marriage date."""

        bounds: GedcomRepo = GedcomRepo("us29_us30.ged")
        bounds.ged_reader()
        b_set = {'I13', 'I1', 'I15', 'US30_I9', 'I6'} #New version of code
        self.assertEqual(bounds.us30(), b_set)



if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
