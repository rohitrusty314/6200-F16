from urllib.request import urlopen
import math
import re
import operator


inverted_index = {}
summation_df = {}


# create summation of term frequencies for each document
def all_tokens_in_doc(doc,tok_count):
    
    if doc in summation_df:
        summation_df[doc] = float(summation_df[doc]) + tok_count
        
    else:
        curr_doc_term_count = {doc:tok_count}
        summation_df.update(curr_doc_term_count)


       
#load inverted indexer
indexer_file = open("1_gram_indices.txt","r")

j=0
for index in indexer_file.readlines():
    
    split_of_index = index.split()
    
    i = 1
    value_dict = {}
    while (i < len(split_of_index)):
        clean_value = split_of_index[i].replace('(',' ').replace(')',' ').replace(',',' ')
        clean_value_list = clean_value.split()
        
        curr_value_dict = {clean_value_list[0]:clean_value_list[1]}
        value_dict.update(curr_value_dict)
        
        #Add to the total term frequency count of the doc
        log_tok_count = math.log(float(clean_value_list[1])) + 1
        
        idf = math.log(1000/len(split_of_index))
        
        denominator = math.pow((log_tok_count*idf),2)
        
        all_tokens_in_doc(clean_value_list[0],denominator)
        

        #skip 1 element as it is frequency of the term in the doc
        i += 1
        
    
            
    curr_index = {split_of_index[0]:value_dict}

    #add to the inverted_index dict
    inverted_index.update(curr_index)
    j += 1
    '''print(split_of_index[0])
    if j == 6:
        break'''

#print(summation_df)

#query
query = "global warming potential"
query_list = query.split()

document_vector = {}
query_vector = {}

for term in query_list:
    #print(len(inverted_index[term]))
    for doc in inverted_index[term]:
        idf = math.log(1000/len(inverted_index[term]))
        dij_num = (math.log(float(inverted_index[term][doc])) + 1)*idf
        dij_denum = math.sqrt(summation_df[doc])
        
        dij = dij_num/dij_denum

        dict_value = {term:dij}
        if doc not in document_vector:
            dict_entry = {doc:dict_value}
            #print(dict_entry)
            document_vector.update(dict_entry)
        else:
            document_vector[doc].update(dict_value)

term_count_dict = {} 
#query term frequency
for term in query_list:
    
    if term not in term_count_dict:
        curr = {term:query_list.count(term)}
        term_count_dict.update(curr)

#query vector
for term in term_count_dict:
    
    idf = math.log(1000/len(inverted_index[term]))

    #numerator
    term_numer = (math.log(term_count_dict[term])+1)*idf

    #calculate denominator
    sqr_denum_sum = 0
    for query_term in term_count_dict:
        sqr_denum_sum += math.pow(((math.log(term_count_dict[query_term]) + 1) * idf),2)
    term_denum = math.sqrt(sqr_denum_sum)
    
    qij = term_numer/term_denum

    #update to the query vector
    curr_query_score = {term:qij}
    query_vector.update(curr_query_score)

print(query_vector)

document_score = {}


for doc in document_vector:
    dot_prod_numer = 0
    query_denum_part = 0
    for query_term in query_vector:
        if query_term in document_vector[doc]:
            dot = query_vector[query_term] * document_vector[doc][query_term]
            dot_prod_numer += dot

        query_denum_part += math.pow(query_vector[query_term],2)

    doc_denum_part = 0
    for doc_term in document_vector[doc]:
        doc_denum_part += math.pow(document_vector[doc][doc_term],2)

    dot_prod_denum = math.sqrt(query_denum_part*doc_denum_part)

    score = dot_prod_numer/dot_prod_denum

    curr_doc_score = {doc: score}
    document_score.update(curr_doc_score)


print(len(document_score))
sorted_docs = sorted(document_score.items(), key=operator.itemgetter(1),reverse = True)

x = 1
for doc_score_tuple in sorted_docs:
    print(str(x)+"\t"+doc_score_tuple[0]+"\t"+str(doc_score_tuple[1]))
    x=x+1


    
    


    











