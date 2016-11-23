from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os.path

#global vars
uni_list = []

#trim Url if there is # in it
def url_before_hash(url):
    hash_at = url.find("#")
    url_substr = url[0:hash_at]
    return url_substr


#crawl url, and keep a counter of depth
def depth_crawl(url,depth):
    if len(uni_list) >= 1000:
        return
    
    if depth <=4:
        time.sleep(1)
        urlhandler = urlopen(url)
        html = urlhandler.read()
        soup = BeautifulSoup(html)

        for a in soup.find_all('a',href=True):
            if a['href'].startswith("/wiki/") and\
               a['href'].find(":") == -1 and\
               a['href'].find("Main_Page") == -1 and\
               ("solar" in a['href'].lower() or "solar" in a.text.lower()) and\
               ("https://en.wikipedia.org"+a['href']) not in uni_list:
                
                   if a['href'].find("#") != -1:
                       
                       a['href'] =  url_before_hash(a['href'])
                      
                   if ("https://en.wikipedia.org"+a['href']) not in uni_list:
                       
                       uni_list.append("https://en.wikipedia.org"+a['href'])
                       depth_crawl("https://en.wikipedia.org"+a['href'],depth+1)
    else:    #if the deoth is 5 return
        return
        
#remove duplicates, if any from the final list
def remove_duplicates():
    unique_list = []
    for i in uni_list:
        insert = True
        for j in unique_list:
                if i == j:
                    insert = False
                    
        if insert:
            unique_list.append(i)
    return unique_list
              
              
              
#main
uni_list.append("https://en.wikipedia.org/wiki/Sustainable_energy")
seed = "https://en.wikipedia.org/wiki/Sustainable_energy"
depth_crawl(seed,1)
final_list = remove_duplicates()

#write to file
crawler_file = open("3_Focused_DFS_Url_list.txt","w")

i=0
for url in final_list:
    
    crawler_file.write(url)
    crawler_file.write("\n")

    #webpage download
    urlhandler = urlopen(url)
    html = urlhandler.read()

    completeName = os.path.join("3_Focussed_DFS_pages","webpage_"+str(i)+".txt")
    webpage_file = open(completeName,"wb")
    webpage_file.write(html)
    webpage_file.close()

    print("On page: ")
    print(i)
    print("\n")
    i = i + 1

crawler_file.close()    


        

        
        
        

    
        
