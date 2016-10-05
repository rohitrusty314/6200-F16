from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

uni_list = []


def url_before_hash(url):
    hash_at = url.find("#")
    url_substr = url[0:hash_at]
    return url_substr


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
                       print("node at ",depth+1)
                       print(a['href'],"\n")
                       uni_list.append("https://en.wikipedia.org"+a['href'])
                       depth_crawl("https://en.wikipedia.org"+a['href'],depth+1)
    else:
        return
        

def remove_duplicates():
    unique_list = []
    for i in uni_list:
        insert = True
        for j in unique_list:
                if i == j:
                    insert = False
                    
        if insert:
            unique_list.append(i)
    print(len(unique_list))
    return unique_list
              
              
              

uni_list.append("https://en.wikipedia.org/wiki/Sustainable_energy")
seed = "https://en.wikipedia.org/wiki/Sustainable_energy"
depth_crawl(seed,1)
final_list = remove_duplicates()

crawler_file = open("3_Focused_DFS_Url_list.txt","w")

for url in final_list:
    print(url,"\n")
    crawler_file.write(url)
    crawler_file.write("\n")

crawler_file.close()    
print(len(final_list))

        

        
        
        

    
        
