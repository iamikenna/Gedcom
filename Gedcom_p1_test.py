import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
import datetime
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

        errors = ['I13', 'I14', 'US33_I21', 'US33_I22', 'US16_I11',
                  'US16_I12', 'US16_I21', 'US16_I22']
        self.assertEqual(test.us02(), errors)

        """Tests the following boundaries:
        1. Missing/incorrectly formatted death date for dead individual
        2. Missing/incorrectly formatted birthday
        3. Missing/incorrectly formatted divorce date
        4. Missing/incorrectly formatted marriage date."""

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
                          ('I15', 'US02_F7'), ('I1', 'F2'), ('I15', 'US02_F7'),
                          ('US32_I45', 'US32_F4'), ('US32_I44', 'US32_F4'),
                          ('US32_I46', 'US32_F4'), ('US32_I47', 'US32_F4'),
                          ('US32_I43', 'US32_F4')])
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
        self.assertEqual(len(test.us09()), 4)

    # Author: Lehmann Margaret
    def test_us10(self):
        """ Tests marriage at least 14 years old"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us10()), 14)

    # Author: Ibezim Ikenna
    def test_us11(self):
        """Marriage should not occur during marriage to another spouse"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        couples = ['us_11_I13']
        error = []
        my_func = test.us11()
        self.assertEqual(my_func,  couples)
        self.assertNotEqual(my_func,  error)

    # Author: Shaffer Wayne
    def test_us12(self):
        """ Tests parents too old """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        failed_families = ["F5", "F9", "F9",
                           "US12_F1", "US12_F3", "US28_F1", "US28_F3"]
        self.assertEqual(test.us12(), failed_families)

    # Author: Ibezim Ikenna
    def test_us14(self):
        """No more than five siblings should be born at the same time --Ikenna"""
        test = GedcomRepo("family.ged")
        test.ged_reader()
        family = ['us14_F2']
        error = []
        my_func = test.us14()

        self.assertEqual(my_func,  family)
        self.assertNotEqual(my_func,  error)

    # Author: Lehmann Margaret
    def test_us15(self):
        """ Tests for families with 15 or more children """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(test.us15()), 1)

    # Author: Shaffer Wayne
    def test_us16(self):
        """Tests that all males in a family have the same last name."""
        test = GedcomRepo("us16_family.ged")
        test.ged_reader()
        failed_IDs = ["US16_I16", "US16_I25", "US16_I26"]
        self.assertEqual(test.us16(), failed_IDs)

        test = GedcomRepo("family.ged")
        test.ged_reader()
        failed_IDs = ["I15", "I15", "us14_I9", "us14_I4", "us14_I5", "us14_20", 
                      "us14_I6", "us14_I8", "US16_I16", "US16_I25", "US16_I26"]
        self.assertEqual(test.us16(), failed_IDs)

    # Author: McKenzie Christopher
    def test_us17(self):
        """Tests if parents are married to children."""
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()

        errors: List[str] = ['US17_F2', 'US17_F3']
        self.assertEqual(test.us17(), errors)

        """Bounds tested include:
        1. Divorced parents
        2. Parent/Child divorce
        3. Parent death
        4. Child death
        5. Death before parent/child marriage
        6. Multiple marriages
        7. Invalid marriage, divorce, and death dates
        """

        bounds: GedcomRepo = GedcomRepo("us17.ged")
        bounds.ged_reader()
        b_errors: List[str] = ['US17_F3', 'US17_F5', 'US17_F6']
        self.assertEqual(bounds.us17(), b_errors)

    # Author: McKenzie Christopher
    def test_us18(self):
        """Tests if siblings are married to each other."""
        test = GedcomRepo("family.ged")
        test.ged_reader()

        errors: List[str] = ['US18_F2', 'US18_F3']
        self.assertEqual(test.us18(), errors)

        """Bounds tested include:
        1. Sibling divorce
        2. Sibling death
        3. Multiple marriages
        4. Death before sibling marriage
        5. Invalid marriage, divorce, and death dates
        """

        bounds: GedcomRepo = GedcomRepo("us18.ged")
        bounds.ged_reader()
        b_errors: List[str] = ['US18_F3', 'US18_F5', 'US18_F6']
        self.assertEqual(bounds.us18(), b_errors)

    # Author: Shaffer Wayne
    def test_us21(self):
        """ Test if husband and wife are correct gender in each family. """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        failed_families = ["I1", "US21_I41", "US21_I42", "US21_I52"]
        self.assertEqual(test.us21(), failed_families)

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
    def test_us23(self):
        """Unique name and birth date"""
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()
        duplicates, error = [('Susan /Sargent/', datetime.date(1989, 5, 5))], []
        # Testing duplicates names and birthdate in individual table
        my_func = test.us23()
        self.assertEqual(my_func, duplicates)
        # Testing for errors
        self.assertNotEqual(my_func, error)

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
                         ('US01_I17', -30), ('US17_I1',
                                             80), ('US17_I2', 75), ('US17_I3', 40),
                         ('US17_I4', 38), ('US18_I1', 100), ('US18_I2',
                                                             100), ('US18_I3', 73), ('US18_I4', 71),
                         ('US18_I5', 69), ('US18_I6', 67), ('I1',
                                                            65), ('US01_I17', 71), ('I15', 65),
                         ('I15', 65), ('us14_I9', 2), ('us14_I4', 2), ('us14_I5', 2),
                         ('us14_20', 2), ('us14_I6', 2), ('us14_I8', 2),
                         ('US09_I1', 28), ('US09_I2', 48), ('US09_I3', 27),
                         ('US09_I4', 30), ('US09_I5', 72), ('US09_I6', 42),
                         ('US09_I7', 40), ('US09_I8', 35), ('US09_I9', 70),
                         ('US12_I11', 105), ('US12_I12', 80), ('US12_I13', 60),
                         ('US12_I14', 58), ('US12_I15', 23), ('US12_I16', 22),
                         ('US12_I31', 68), ('US12_I32', 65), ('US12_I33', 'NA'),
                         ('US12_I34', 'NA'), ('US12_I21', 63), ('US12_I22', 57),
                         ('US12_I23', 40), ('US12_I24', 32), ('US21_I41', 31),
                         ('US21_I42', 31), ('US21_I51',
                                            31), ('US21_I52', 31), ('us23_I1', 31),
                         ('US33_I21', 30), ('US33_I22', 29), ('US33_I23',
                                                              1), ('US33_I24', 2), ('US15_I1', 60),
                         ('US15_I2', 58), ('US15_I3', 30), ('US15_I4', 29),
                         ('US15_I5', 28), ('US15_I6', 27), ('US15_I7', 26),
                         ('US15_I8', 25), ('US15_I9', 24), ('US15_I10', 23),
                         ('US15_I11', 22), ('US15_I12', 21), ('US15_I13', 20),
                         ('US15_I14', 19), ('US15_I15', 18), ('US15_I16', 17),
                         ('US15_I17', 16), ('US15_2_I1', 60), ('US15_2_I2', 58),
                         ('US15_2_I3', 30), ('US15_2_I4', 29),
                         ('US15_2_I5', 28), ('US15_2_I6', 27),
                         ('US15_2_I7', 26), ('US15_2_I8', 25),
                         ('US15_2_I9', 24), ('US15_2_I10', 23),
                         ('US15_2_I11', 22), ('US15_2_I12', 21),
                         ('US15_2_I13', 20), ('US15_2_I14', 19),
                         ('US15_2_I15', 18), ('US15_2_I16', 17),
                         ('US28_I11', 105), ('US28_I12', 80),
                         ('US28_I13', 60), ('US28_I14', 57),
                         ('US28_I15', 57), ('US28_I16', 23),
                         ('US28_I17', 22), ('US28_I31', 65),
                         ('US28_I32', 65), ('US28_I33', 'NA'),
                         ('US28_I34', 'NA'), ('US28_I35', 40),
                         ('US32_I41', 31), ('US32_I42', 34),
                         ('US32_I43', 4), ('US32_I44', 4),
                         ('US32_I45', 4), ('US32_I46', 2),
                         ('US32_I47', 2), ('US35_I1', 0),
                         ('US35_I2', 34), ('US35_I3', 33),
                         ('US35_I4', 61), ('US35_I5', 60),
                         ('US16_I11', 45), ('US16_I12', 50),
                         ('US16_I13', 30), ('US16_I14', 28),
                         ('US16_I15', 23), ('US16_I16', 20),
                         ('US16_I17', 17), ('US16_I21', 47),
                         ('US16_I22', 38), ('US16_I23', 30),
                         ('US16_I24', 28), ('US16_I25', 23),
                         ('US16_I26', 20), ('US16_I27', 17)],  []
        my_func = test.us27()

        self.assertEqual(my_func,  id_age)
        self.assertNotEqual(my_func,  error)

    # Author: Shaffer Wayne
    def test_us28(self):
        """ Tests if children are listed oldest to youngest from each family"""
        test_files = ["us28_us32_family.ged", "familly.ged"]

        for filename in test_files:
            test = GedcomRepo(filename)
            test.ged_reader()

            result = test.us28()

            for age_list in result:
                print(age_list)
                self.assertTrue(age_list == sorted(
                    age_list, key=lambda i: str(i[1]), reverse=True))

    # Author: Christopher McKenzie
    def test_us29(self):
        """Tests if function lists all dead individuals."""

        set_deat = {'US09_I3', 'I16', 'US09_I4', 'US09_I8',
                    'US07_I0886', 'US07_I1', 'I12', 'US33_I21', 'US33_I22', 'US35_I4', 'US35_I3'}
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(test.us29(), set_deat)

        """Below tests the following boundaries:
        1. Missing death date
        2. Future death date
        3. Invalid death date."""

        bounds: GedcomRepo = GedcomRepo("us29_us30.ged")
        bounds.ged_reader()
        b_set = {'US29_US30_I11', 'US30_I2', 'I12', 'US07_I0886'}
        self.assertEqual(bounds.us29(), b_set)

    # Author: Christopher McKenzie
    def test_us30(self):
        """Tests if function lists all living married people."""
        set_marr = {'I4', 'US12_I21', 'US17_I3', 'I3', 'US12_I22', 'US18_I2',
                    'US18_I6', 'I2', 'US12_I12', 'US18_I1', 'US09_I6',
                    'US21_I42', 'US17_I2', 'US18_I5', 'US12_I31', 'US21_I51',
                    'US12_I11', 'I9', 'US09_I2', 'US21_I41', 'US17_I4',
                    'US18_I4', 'US18_I3', 'US21_I52', 'US17_I1', 'US12_I32',
                    'US09_I7', 'US28_I11', 'US28_I12', 'US28_I32',
                    'US28_I31', 'US32_I41', 'US32_I42', 'US35_I2', 'US35_I5',
                    'US16_I21', 'US16_I11', 'US16_I12', 'US16_I22'}
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(test.us30(), set_marr)

        """Below tests the following boundaries:
        1. Married but one spouse dead
        2. Future death date
        3. Missing marriage date
        4. Future marriage date
        5. Invalid death date
        6. Invalid marriage date."""

        bounds: GedcomRepo = GedcomRepo("us29_us30.ged")
        bounds.ged_reader()
        b_set = {'I13', 'US30_I14'}
        self.assertEqual(bounds.us30(), b_set)

    # Author: Lehmann Margaret
    def test_us31(self):
        """ Tests if the function lists all living over 30 people who were never married. """
        set_single = {'US01_I17', 'US12_I23', 'US01_I11', 'I5',
                      'US12_I24', 'US12_I14', 'us23_I1', 'US12_I13', 'US15_I3',
                      'US15_2_I3', 'US28_I14', 'US28_I15', 'US28_I35', 'US28_I13',
                      'US16_I13', 'US16_I23'}

        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(test.us31(), set_single)

    # Author: Shaffer Wayne
    def test_us32(self):
        """ Tests if multiple births are listed. """
        # for sample family file
        sample_test = GedcomRepo("us28_us32_family.ged")
        sample_test.ged_reader()
        expected_result = ["2016-06-06", "2018-04-04"]
        self.assertTrue(sample_test.us32() == expected_result)

        # for full family file
        test = GedcomRepo("family.ged")
        test.ged_reader()
        expected_result = ["1955-08-08",
                           "2018-08-27", "2016-06-06", "2018-04-04"]
        self.assertTrue(test.us32() == expected_result)

    # Author: Ibezim Ikenna
    def test_us33(self):
        """Testing List of orphans"""
        test: GedcomRepo = GedcomRepo("family.ged")
        test.ged_reader()
        kids, error = [('US33_I23', 1), ('US33_I24', 2)], []
        # Testing duplicates names and birthdate in individual table
        my_func = test.us33()
        self.assertEqual(my_func, kids)
        # Testing for errors
        self.assertNotEqual(my_func, sorted(error))

    # Author: Lehmann Margaret
    def test_us35(self):
        """ Tests births in the last 30 days """
        test = GedcomRepo("family.ged", datetime.datetime(
            1989, 2, 20).date())  # static date time
        test.ged_reader()

        people = {'US21_I51', 'US21_I42', 'US21_I41', 'US32_I41'}
        self.assertEqual(test.us35(), people)

    # Author: Lehmann Margaret
    def test_us36(self):
        """ Tests deaths in the last 30 days """
        test = GedcomRepo("family.ged", datetime.datetime(
            2019, 4, 20).date())  # static datetime
        test.ged_reader()

        people = {'US33_I22', 'US33_I21', 'US07_I1'}
        self.assertEqual(test.us36(), people)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
