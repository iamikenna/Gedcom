import unittest
from Gedcom_p1 import Individual, Family, GedcomRepo

user = input("Please enter a file name")

class UserStoryTest(unittest.TestCase):
    """ Class test for all user stories """
  
        
    def test_us22(self):
        
        """function to test the major tables""" 
        test = GedcomRepo("/Applications/XAMPP/xamppfiles/htdocs/Gedcom/Gedcom/family.ged")
        test.ged_reader()
        ind_id_duplicates, fam_id_duplicates = ['I1', 'I17', 'I15', 'I15'], ['F8', 'F9']
        self.assertEqual(test.us22()[0],  ind_id_duplicates) #Testing duplicates ID for individual table
        self.assertEqual(test.us22()[1],  fam_id_duplicates) #Testing duplicates ID for family table
        
            
if __name__ == "__main__":
    unittest.main(exit = False, verbosity = 2)  