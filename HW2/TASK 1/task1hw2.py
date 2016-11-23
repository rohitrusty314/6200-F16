from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path

#trim the url till # occurs in it
def url_before_hash(url):

 
    hash_at = url.find("#")
    url_substr = url[0:hash_at]
    return url_substr


def get_url_list(crawlurl):
    curr_urllist = []
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



def page_title(url):
    url = url.strip('https://en.wikipedia.org/wiki/')
    return url.strip('\n')



def get_inlinks2():
    j = 0
    for url in url_list:
        out_links = get_url_list(url)

        for link in out_links:
            link_docid = link.replace('/wiki/','')
            url_docid = page_title(url)
            if link_docid in inlink_graph and\
               url_docid not in inlink_graph[link_docid] and\
               url_docid != link_docid:
                inlink_graph[link_docid].append(url_docid)
                
        print(j)
        j=j+1
        
        

inlink_graph = {}
url_list = []
url_file = open("1_Unfocused_Url_list.txt","r")
url_list = url_file.readlines()
url_file.close()
i = 0


for url in url_list:    
    #title = page_title(url,i)
    docid = page_title(url)
    inlink_for = {docid:[]}
    inlink_graph.update(inlink_for)    
    i = i + 1

get_inlinks2()

inlink_file = open("task1_G1.txt","w")

print(".................")
print(".................")
i = 1
for url in url_list:
    key = page_title(url)
    inlink_file.write(key+" ")
    for value in inlink_graph[key]:
        inlink_file.write(value+" ")
    inlink_file.write("\n")
    print(i)
    i += 1

inlink_file.close()


    
    
