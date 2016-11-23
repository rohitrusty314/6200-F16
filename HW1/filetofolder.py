import os.path

#save_path = "C:\Users\Rohit\Documents\GitHub\6200-F16\HW1\1_Unfocussed_pages"

#name_of_file = raw_input("What is the name of the file: ")

completeName = os.path.join("1_Unfocussed_pages", "webpage.txt")         

file1 = open(completeName, "w")

toFile = "fkkdsajfhksdhfjashkfjhsakhfkjdshafkhsakjfh"

file1.write(toFile)

file1.close()
