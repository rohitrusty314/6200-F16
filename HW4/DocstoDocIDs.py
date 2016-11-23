doc_to_docID = {}

with open('doc_docid_map.txt') as f:
   
    for line in f:
        docs = line.split()
        docs[1] = docs[1].replace('.txt','')
        doc_to_docID[docs[1]] = docs[0]

        

for query_ID in range(1,5):
    with open('query'+ str(query_ID)+'cosinescoresLUCENE.txt') as f:
        f2 = open('query'+ str(query_ID)+'LUCENEcosinewithdocid.txt','w')
        for line in f:
            elements = line.split()
            print(elements)
            f2.write(elements[0]+' '+elements[1]+' '+doc_to_docID[elements[2]]+' '+elements[3]\
            +' '+elements[4]+' '+elements[5]+'\n')
        f2.close()
