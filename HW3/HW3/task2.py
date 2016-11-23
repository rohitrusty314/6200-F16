from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os.path
import re
import glob
import operator

l=1
one_gram_graph = {}
two_gram_graph = {}
three_gram_graph = {}
one_gram_tf = {}
two_gram_tf = {}
three_gram_tf = {}
doc_docid_dict = {}


###############################################################################

#Indexes the token into a dict to write them later
def indexer(tok, graph, curr_tup, curr_tok, l, curr_tf, n_gram_tf):
    #if token has not been indexed
    if tok not in graph:
        graph.update(curr_tok)
        n_gram_tf.update(curr_tf)


    #if token has already been indexed
    else:
        
        n_gram_tf[tok] += 1
        insert_tup = True
        for i in range(0,len(graph[tok])):
            
            if int(l) == int(graph[tok][i][0]):
                insert_tup = False
                graph[tok][i] = (graph[tok][i][0], graph[tok][i][1] + 1)
                break
        if insert_tup:
            graph[tok].append(curr_tup)
            

#write the index generated to the given file
def write_indexer_to_file(file_name, graph):
    file_op = open(file_name,"wb")
    for tok in graph:
        file_op.write(tok.encode('utf-8'))
        for i in range(0,len(graph[tok])):
            if i == 0:
                doc_id = "\t("+graph[tok][i][0]+","+str(graph[tok][i][1])+")"
            else:
                doc_id = " ("+graph[tok][i][0]+","+str(graph[tok][i][1])+")"
            

            if i != len(graph[tok])-1:
                doc_id = doc_id+", "
            file_op.write(doc_id.encode('utf-8'))
        
        file_op.write("\r\n".encode('utf-8'))

    file_op.close()
    
###############################################################################


#process each file in the folder with cleaned text to create the indexer
#the desired folder can be specified to read the cleaned texts
for file_with_path in glob.glob(os.path.join("Cleaned_Text",'*.txt')):
    file_name = file_with_path[file_with_path.find('\\')+1:]
    curr_docid = {l:file_name}

    doc_docid_dict.update(curr_docid)
    
    

    file_handler = open(file_with_path,"rb")
    all_tokens = file_handler.read().decode('utf-8')
    token_list = all_tokens.split()

    
    #make and process 1-grams
    for i in range(0,len(token_list)):
        curr_tup = (str(l),1)
        tok = token_list[i]
        curr_tok = {tok:[curr_tup]}
        curr_tf = {tok:1}

        indexer(tok,one_gram_graph, curr_tup, curr_tok, l, curr_tf, one_gram_tf)
    
       
    #make and process 2-grams
    for i in range(0,len(token_list)-1):
        curr_tup = (str(l),1)
        tok = token_list[i]+" "+token_list[i+1]
        curr_tok = {tok:[curr_tup]}
        curr_tf = {tok:1}

        indexer(tok, two_gram_graph, curr_tup, curr_tok, l, curr_tf, two_gram_tf)

    #make and process 3-grams
    for i in range(0,len(token_list)-2):
        curr_tup = (str(l),1)
        tok = token_list[i]+" "+token_list[i+1]+" "+token_list[i+2]
        
        curr_tok = {tok:[curr_tup]}
        curr_tf = {tok:1}

        indexer(tok, three_gram_graph, curr_tup, curr_tok, l, curr_tf, three_gram_tf)
    
    file_handler.close()
    l+=1
    print(l)
    
###############################################################################
#write 1-grams
write_indexer_to_file("1_gram_indices.txt", one_gram_graph)

#write 2-grams
write_indexer_to_file("2_gram_indices.txt", two_gram_graph)

#write 3-grams
write_indexer_to_file("3_gram_indices.txt", three_gram_graph)



###############################################################################

def write_term_frequency(file_name, n_gram_tf):
    file_op = open(file_name,"wb")
    sorted_x = sorted(n_gram_tf.items(), key=operator.itemgetter(1),reverse = True)
    for tok in sorted_x:
        token = tok[0] + "\t\t"
        file_op.write(token.encode('utf-8'))
        file_op.write(str(tok[1]).encode('utf-8'))
        file_op.write("\r\n".encode('utf-8'))

    file_op.close()


def write_doc_frequency(file_name, n_gram_graph):
    file_op = open(file_name,"wb")
    sorted_n_gram_graph = sorted(n_gram_graph.keys())
    
    for tok in sorted_n_gram_graph:
        
        token = str(tok) + "\t\t"
        file_op.write(token.encode('utf-8'))
        
        doc_tuple_list = n_gram_graph[tok]
        df = len(doc_tuple_list)
        for i in range(0, df):
            if i != df - 1:
                doc_id  = doc_tuple_list[i][0] + ","
            else:
                doc_id = doc_tuple_list[i][0]
            file_op.write(doc_id.encode('utf-8'))
        formatted_df = "\t\t" + str(df) + "\r\n"
        file_op.write(formatted_df.encode('utf-8'))
    file_op.close()
    
# Write term frequency to file
write_term_frequency("1_gram_frequency.txt", one_gram_tf)
write_term_frequency("2_gram_frequency.txt", two_gram_tf)
write_term_frequency("3_gram_frequency.txt", three_gram_tf)


#write document frequency to file
write_doc_frequency("1_gram_df.txt", one_gram_graph)
write_doc_frequency("2_gram_df.txt", two_gram_graph)
write_doc_frequency("3_gram_df.txt", three_gram_graph) 

###############################################################################

file_handler = open("doc_docid_map.txt","wb")
for doc in doc_docid_dict:
    s = str(doc)+"\t"+doc_docid_dict[doc]+"\r\n"
    file_handler.write(s.encode('utf-8'))
file_handler.close()



