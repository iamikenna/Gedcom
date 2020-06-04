"""
Author: Ibezim Ikenna
User function to read files for my homework
"""
# export-Forest.ged
# proj02test.ged
#sample-1.ged
def ged_reader():
    """This function reads a gedcom file and displays output"""
    user_input = input("Enter the file name \n") #taking input from the user
    dict_storage = {
            '0':['HEAD','NOTE','TRLR'], 
            '1':['BIRT','CHIL','DIV','HUSB','WIFE','MARR','NAME','SEX','DEAT','FAMC','FAMS'], 
            '2':['DATE'],
            '5':['INDI', 'FAM']
        } #storing the level element as key and tag elements as values
    try: #Catching an exception
        open_file = open(user_input, "r")
    except FileNotFoundError as e:
        print(e)
    else:
        with open_file: # This closes the file after using the file
            for line in open_file:
                line = line.strip()
                print(f"-->{line}")
                line_list = line.split(" ")
                len_line = len(line_list)
                #Checking the lines for a specific format
                if len_line == 3 and line_list[2] in dict_storage['5'] and line_list[0] == '0':
                    level,arg, tag = line_list
                    valid = 'Y'
                elif len_line >= 2:
                    level, tag, arg = line_list[0], line_list[1], " ".join(line_list[2:])
                    if level in dict_storage and tag in dict_storage[level]:
                        valid = 'Y'
                    else:
                        valid = 'N'
                else: #Back up Plan
                    valid = 'N'
                    level, tag, arg = line_list
                print(f"<--{level}|{tag}|{valid}|{arg}")
             
ged_reader()
