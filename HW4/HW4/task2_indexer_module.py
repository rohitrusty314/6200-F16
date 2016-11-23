from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os.path
import re
import glob
import operator

l=1
one_gram_graph = {}

doc_docid_dict = {}


###############################################################################

#Indexes the token into a dict to write them later
def indexer(tok, graph, curr_tup, curr_tok, l):
    #if token has not been indexed
    if tok not in graph:
        graph.update(curr_tok)
       


    #if token has already been indexed
    else:
        
        
        insert_tup = True
        #for i in range(0,len(graph[tok])):
       
        if str(l) in graph[tok].keys():
            insert_tup = False
            graph[tok][str(l)] = graph[tok][str(l)] + 1
        if insert_tup:
            graph[tok].update(curr_tup)
            

#write the index generated to the given file
def write_indexer_to_file(file_name, graph):
    file_op = open(file_name,"wb")
    for tok in graph:
        file_op.write(tok.encode('utf-8'))
        i = 0
        for doc in graph[tok]:
            if i == 0:
                doc_id = "\t("+doc+","+str(graph[tok][doc])+")"
            else:
                doc_id = " ("+doc+","+str(graph[tok][doc])+")"
            

            if i != len(graph[tok])-1:
                doc_id = doc_id+", "
            file_op.write(doc_id.encode('utf-8'))
            i += 1
        
        file_op.write("\r\n".encode('utf-8'))

    file_op.close()
    
###############################################################################


#process each file in the folder with cleaned text to create the indexer
#the desired folder can be specified to read the cleaned texts
files_at = glob.glob(os.path.join("Cleaned_Text",'*.txt'))

for i in range(0,len(files_at)):
    file_name = files_at[i][files_at[i].find('\\')+1:]
    curr_docid = {l:file_name}

    doc_docid_dict.update(curr_docid)
    
    

    file_handler = open(files_at[i],"rb")
    all_tokens = file_handler.read().decode('utf-8')
    token_list = all_tokens.split()

    
    #make and process 1-grams
    for i in range(0,len(token_list)):
        curr_tup = {str(l):1}
        tok = token_list[i]
        curr_tok = {tok:curr_tup}
        

        indexer(tok,one_gram_graph, curr_tup, curr_tok, l)
    
       
    
    file_handler.close()
    l+=1
    
###############################################################################
#write 1-grams
write_indexer_to_file("1_gram_indices.txt", one_gram_graph)


###############################################################################

file_handler = open("doc_docid_map.txt","wb")
for doc in doc_docid_dict:
    s = str(doc)+"\t"+doc_docid_dict[doc]+"\r\n"
    file_handler.write(s.encode('utf-8'))
file_handler.close()




