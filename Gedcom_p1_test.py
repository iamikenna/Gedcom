import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo
from datetime import datetime

class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """
  
    #Author: Ibezim Ikenna
    def test_us22(self):
        
        """function to test the id duplicates""" 
        test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged")
        test.ged_reader()
        ind_id_duplicates, fam_id_duplicates, error = ['I1', 'I17', 'I15', 'I15'], ['F8', 'F9'], ['0r','I1', 'I17', 'I15', 'I15']
        self.assertEqual(test.us22()[0],  ind_id_duplicates) #Testing duplicates ID for individual table
        self.assertNotEqual(test.us22()[0],  error)
        self.assertEqual(test.us22()[1],  fam_id_duplicates) #Testing duplicates ID for family table
        
    #Author: Ibezim Ikenna
    def test_us27(self):
        
        """function to test for individual complete data""" 
        test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged")
        test.ged_reader()
        id_age, error = [('I1', "NA"), ('I2', 69),
                          ('I3', 68), ('I4', 40),
                            ('I5', 32), ('I6', 170), ('I7', 32), ('I8', 3),
                            ('I9', 43), ('I10', 18), ('I11', 17), ('I12', 153), 
                            ('I13', 95), ('I14', 103), ('I15', 65), ('I16', 23), 
                            ('I17', 71), ('I1', 65), ('I17', 71), ('I15', 65), 
                            ('I15', 65)
                    ], []
        self.assertEqual(test.us27(),  id_age) #Testing duplicates ID for individual table
        self.assertNotEqual(test.us27(),  error)
        
    #Author: Ibezim Ikenna
    # def test_us07(self):
        
    #     """Checking for less than 150 years """ 
       
    #     test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged")
    #     test.ged_reader()
        # death, alive, error = [('I12', 153)], 
        #                     [('I6', 170)], 
        #                     ['0r','I1', 'I17', 'I15', 'I15']
    #     self.assertEqual(test.us07()[0],  death) 
    #     self.assertNotEqual(test.us07()[0],  error)
    #     self.assertEqual(test.us07()[1],  alive) 
        
    #Author: Ibezim Ikenna
    # def test_us08(self):
        
    #     """ Birth before marriage of parents""" 
        
    #     test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged")
    #     test.ged_reader()
    #     marr_ex = sorted([('I6', 'F2'), ('I1', 'F2'), ('I2', 'F3'), ('I15', 'F7'), ('I15', 'F7'), ('I15', 'F7')])
    #     div_ex = sorted([('I2', 'F3')])
    #     error = []
    #     self.assertEqual(test.us08()[0],  marr_ex) 
    #     self.assertEqual(test.us08()[1],  div_ex) 
    #     self.assertNotEqual(test.us08(),  error)
        
            
if __name__ == "__main__":
    unittest.main(exit = False, verbosity = 2)  