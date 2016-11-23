from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os.path

#global variables
uni_list = []
depth_list = []

#trim url if there is a hash in it
def url_before_hash(url):
    hash_at = url.find("#")
    url_substr = url[0:hash_at]
    return url_substr


#crawl the given url and return the result list

def get_url_list(crawlurl):
    curr_urllist = []
    time.sleep(1)
    urlhandler = urlopen(crawlurl)
    html = urlhandler.read()

    soup = BeautifulSoup(html)
    i=1
    for a in soup.find_all('a',href=True):
        if a['href'].startswith("/wiki/") and\
           a['href'].find(":") == -1 and\
           a['href'].find("Main_Page") == -1 and\
           ("solar" in a['href'].lower() or "solar" in a.text.lower()):

            if a['href'].find("#") != -1:
                a['href'] =  url_before_hash(a['href'])
                
            insert_url = True
            for url in curr_urllist:
                if a['href'] == url:
                    insert_url = False

            if insert_url:
                curr_urllist.append(a['href'])
                i+=1
    return curr_urllist

#crawl for depth 2 onwards
        
def depth2_onwards(depth):
    for i in range(depth_list[2*depth-1],depth_list[2*depth]):        
        if len(uni_list) >= 1000:
            return
        new_url_list = get_url_list("https://en.wikipedia.org"+uni_list[i])
        for url in new_url_list:
            url_insert = True
            for uni_url in uni_list:
                if url == uni_url:
                    url_insert = False
            if url_insert:
                uni_list.append(url)
        
        
#main
seed = "https://en.wikipedia.org/wiki/Sustainable_energy"
uni_list.append("/wiki/Sustainable_energy")
prev_length = 1
new_url_list = get_url_list(seed)
for url in new_url_list:
    url_insert = True
    for uni_url in uni_list:
        if url == uni_url:
            url_insert = False
    if url_insert:
        uni_list.append(url)

depth_list.append(0)

for i in range(1,4):
    if len(uni_list) >= 1000:
            break
    depth_list.append(prev_length)
    depth_list.append(len(uni_list))
    prev_length = depth_list[2*i]
    depth2_onwards(i)

upper_url_count = 1000

if(len(uni_list) < 1000):
    upper_url_count = len(uni_list)

#write to file
crawler_file = open("2_Focused_Url_list.txt","w")

for i in range(0,upper_url_count):
    crawler_file.write("https://en.wikipedia.org"+uni_list[i])
    crawler_file.write("\n")

    #webpage download
    urlhandler = urlopen("https://en.wikipedia.org"+uni_list[i])
    html = urlhandler.read()

    completeName = os.path.join("2_Focussed_BFS_pages","webpage_"+str(i)+".txt")
    webpage_file = open(completeName,"wb")
    webpage_file.write(html)
    webpage_file.close()

    print("On page: ")
    print(i)
    print("\n")

crawler_file.close()



