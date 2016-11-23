from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os.path
import re
import glob


#Trim the page title to create appropriate filename
def make_title(title):
    
    title = title.replace(" ","")
    title = title.replace("-","")
    title = title.replace("_","")
    title = title.replace("/","")
    title = title.replace("\\","")
    return title


l=0
# All raw html files are in the folder 1_Unfocussed_pages
# This can be changed accordingly

for file_with_path in glob.glob(os.path.join("1_Unfocussed_pages",'*.txt')):
   
    file_handler = open(file_with_path,"rb")


    file_name = make_title(file_with_path[file_with_path.find('\\')+1:])
   
    #Parse tbe html content
    soup = BeautifulSoup(file_handler,'html.parser')
    file_handler.close()

    
    # Make a filename for that title to store the cleaned text in it
    # They are put in a folder Cleaned_Text folder

    if not os.path.exists("Cleaned_Text"):
        os.makedirs("Cleaned_Text")

    clean_file_path = os.path.join("Cleaned_Text",file_name)
    output_file = open(clean_file_path,"wb")
    

    # Find all p tags for content
    complete_content_string = soup.title.string + " "
    for a in soup.find_all('p'):
    
        complete_content_string += a.getText() + " "
      
    complete_string = ""
    

    # Find all <ul> tags for un ordered list that are part of the content
    for ul in soup.find_all('ul'):
        if ul.parent.get('id') == 'mw-content-text':
            for li in ul.find_all('li'):
                complete_string = complete_string + li.getText() + " "
                

    new_string = complete_content_string+" "+complete_string
    all_tokens = new_string.split(" ")


    # Clean each token
    
    for s in all_tokens:
        if not (s.startswith("doi:")):
            
            s = re.sub(r'\[[0-9]+\]+',"",s)
            s = re.sub(r'[^a-zA-Z0-9]*$',"",s)
            s = re.sub(r'^[^a-zA-Z0-9]*',"",s)
            s = s.replace("'","")
            s = s.replace("\"","")
            s = s.replace("&","")
            s = s.replace("#","")
            s = s.replace("*","")
            s = s.replace("$","")
            if re.search(r'[0-9]+\.[0-9]+',s):
                s
            else:
                s = s.replace(".","")

            if s != " " and not(s.startswith("http://")):
                output_file.write(s.lower().encode('utf-8')+" ".encode('utf-8'))

    #close output file handler
    output_file.close()
    print(l)
    l+=1

    


    

    
    


