from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

#global list to store all the links
uni_list = []
depth_list = []     #to store respective depths

#trim the url till # occurs in it
def url_before_hash(url):

 
    hash_at = url.find("#")
    url_substr = url[0:hash_at]
    return url_substr


#crawl the url with the passed to it and return all the
#valid links on it
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
           a['href'].find("Main_Page") == -1:
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

#handles the list of urls to be crawled from depth2 onwards        
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
uni_list.append("/wiki/Sustainable_energy") #append depth1 data
prev_length = 1
new_url_list = get_url_list(seed)

#get depth counter value after each crawl
for url in new_url_list:
    url_insert = True
    for uni_url in uni_list:
        if url == uni_url:
            url_insert = False
    if url_insert:
        uni_list.append(url)

depth_list.append(0)

#to crawl urls from depth2 onwards
for i in range(1,4):
    if len(uni_list) >= 1000:
            break
    depth_list.append(prev_length)
    depth_list.append(len(uni_list))
    prev_length = depth_list[2*i]
    depth2_onwards(i)

#write the urls to file
crawler_file = open("1_Unfocused_Url_list.txt","w")


for i in range(0,1000):
    crawler_file.write("https://en.wikipedia.org"+uni_list[i])
    crawler_file.write("\n")

    #webpage download
    urlhandler = urlopen("https://en.wikipedia.org"+uni_list[i])
    html = urlhandler.read()
    webpage_file = open("webpage_"+str(i)+".txt","wb")
    webpage_file.write(html)
    webpage_file.close()

    print("On page: ")
    print(i)
    print("\n")
    
crawler_file.close()



    


    








