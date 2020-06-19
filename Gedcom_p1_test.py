import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
from datetime import datetime
from prettytable import PrettyTable  # Used to build a table
from collections import defaultdict


class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """

    def setUp(self):
        """ Initial setup code for unit tests """

        self.test = GedcomRepo("family.ged")
        self.test.ged_reader()

    # Author: Christopher McKenzie
    def test_us01(self):
        """Tests that dates do not occur before current date."""

        test = GedcomRepo("test.ged")
        test.ged_reader()
        present: date = datetime.date(datetime.now())
        errors = ['I18', 'I19', 'F11', 'F12']

        self.assertEqual(test.us01(), errors)

    # Author: Christopher McKenzie
    def test_us02(self):
        """Tests that marriage only occurs after birth."""

        test = GedcomRepo("test.ged")
        test.ged_reader()
        errors = ['I23', 'I24', 'I25', 'I26']

        self.assertEqual(test.us02(), errors)

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
        self.assertEqual(len(self.test.us04()), 2)

    # Author: Lehmann Margaret
    def test_us05(self):
        """ Tests marriagne before death """
        test = GedcomRepo("family.ged")
        test.ged_reader()
        self.assertEqual(len(self.test.us05()), 1)

    # Author: Shaffer Wayne
    def test_us06(self):
        """ Tests divorce before death for each individual """
        self.assertTrue(len(self.test.us06()) > 0)

    # Author: Ibezim Ikenna
    def test_us22(self):
        """function to test the id duplicates"""
        ind_id_duplicates, fam_id_duplicates, error = ['I1', 'I17', 'I15', 'I15'], [
            'F8', 'F9'], ['0r', 'I1', 'I17', 'I15', 'I15']
        # Testing duplicates ID for individual table
        self.assertEqual(self.test.us22()[0],  ind_id_duplicates)
        # Testing duplicates ID for family table
        self.assertEqual(self.test.us22()[1],  fam_id_duplicates)
        # Testing for errors
        self.assertNotEqual(self.test.us22()[0],  error)

    # Author: Ibezim Ikenna
    def test_us27(self):
        """function to test for individual complete data"""
        #test = GedcomRepo("family.ged")
        # test.ged_reader()
        id_age, error = [('I1', "NA"), ('I2', 69),
                         ('I3', 68), ('I4', 40),
                         ('I5', 32), ('I6', 170), ('I7', 32), ('I8', 3),
                         ('I9', 43), ('I10', 18), ('I11', 17), ('I12', 112),
                         ('I13', 95), ('I14', 103), ('I15', 65), ('I16', -2),
                         ('I17', 71), ('I1', 65), ('I17', 71), ('I15', 65),
                         ('I15', 65)
                         ], []

        self.assertEqual(self.test.us27(),  id_age)
        self.assertNotEqual(self.test.us27(),  error)

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
