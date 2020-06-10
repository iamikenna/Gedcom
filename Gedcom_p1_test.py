import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo

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
        id_age, error = [('I1', 45), ('I2', 69),
                          ('I3', 68), ('I4', 40),
                            ('I5', 32), ('I6', 41), ('I7', 32), ('I8', 3),
                            ('I9', 43), ('I10', 18), ('I11', 17), ('I12', 103), 
                            ('I13', 95), ('I14', 103), ('I15', 65), ('I16', 23), 
                            ('I17', 71), ('I1', 65), ('I17', 71), ('I15', 65), 
                            ('I15', 65)
                    ], []
        self.assertEqual(test.us27(),  id_age) #Testing duplicates ID for individual table
        self.assertNotEqual(test.us27(),  error)
        
            
if __name__ == "__main__":
    unittest.main(exit = False, verbosity = 2)  