import math
import operator

#Calculate initial page rank for all the pages in a graph
def initial_PR():
    for key in inlink_graph:
        value = {key:1/N}
        pr_p_graph.update(value)


#Perplexity calculation
def perplexity():
    H = 0
    for key in pr_p_graph:
        H += pr_p_graph[key] * math.log(pr_p_graph[key],2)
    H = -1 * H
    perplexity = math.pow(2,H)
    return perplexity


#Get list of in-links for a page
def links_to_page(p):
    mp = inlink_graph[p]
    return mp


#Get sink pages(i.e pages with no out-links)        
def get_sink_pages():
    links_from = []
    sink_pages = []
    pageno = 0
    
    links_from = list(inlink_graph.values())
    for k in range(0,len(links_from)):
            for u in links_from[k]:
                links_from2.append(u)
                
    links_to = list(inlink_graph.keys())        
    sink_pages = list(set(links_to)-set(links_from2))
    return sink_pages


####List of files that can be run the appropriate filename file can be
####uncommented to when needed to run

#Comment/Uncomment for G2:
inlink_file = open("wt2g_inlinks.txt","r")


####Comment/Uncomment for small sample file given in the question:
####Change the file name if needed.

#inlink_file = open("test_inlink_file.txt","r")



####Comment/Uncomment for G1(change the file name if needed):

#inlink_file = open("G1_inlinks.txt","r")

#Read from Graph file
inlinks = inlink_file.readlines()
inlink_file.close()


#Initializations
inlink_graph = {}
pr_p_graph = {}
p_lq_graph = {}
links_from2 = []
links_keys = []
new_pr = {}


#Map data read to a dict
for link in inlinks:
    p = link.split()
    if p[0] not in inlink_graph:
        inlink_for = {p[0]:[]}
        curr_new = {p[0]:[0.0]}
        new_pr.update(curr_new)
        
        for i in range (1,len(p)):
            if p[i] not in inlink_for[p[0]]:
                inlink_for[p[0]].append(p[i])
                if p[i] in p_lq_graph:
                    p_lq_graph[p[i]] += 1
                else:
                    curr = {p[i]:1}
                    p_lq_graph.update(curr)
        inlink_graph.update(inlink_for)





#Length total number of links
N = len(inlink_graph)

#Assign initial Page Rank to all the links
initial_PR()

#Find out the sink pages i.e. pages with no out-links
sink_pages = get_sink_pages()
links_keys = list(inlink_graph.keys())


#Convergence counter
conv = 0

#dampening factor
d = 0.85

#initial perplexity
prplx1 = perplexity()
prplx2 = 0
change = prplx1-prplx2

perplexity_file = open("6.perplexity_G2.txt","w")
#perplexity_file = open("5.perplexity_G1.txt","w")

#Counter for iteration
itr = 0

#######################################################################################################
#Page Rank Implementation

while conv < 4:
    sink_pr = 0
    for page in sink_pages:
        sink_pr += pr_p_graph[page]
    cnt = 0
    for links in links_keys: 

        new_pr_curr = (1-d)/N
        new_pr_curr += d*sink_pr/N

        mp = links_to_page(links)
        
        for q in mp:
            
            pr_q = pr_p_graph[q]
            lq = p_lq_graph[q]

            new_pr_curr += d*pr_q/lq
        new_pr[links] = new_pr_curr

    for links in links_keys: 
        pr_p_graph[links] = new_pr[links]

    
    prplx2 = perplexity()
   
    change = abs(prplx1-prplx2)
    perplexity_file.write("Iteration: "+str(itr+1)+\
                          " Perplexity: "+str(prplx2)+"\n")
   
    prplx1 = prplx2
    if change < 1:
        conv += 1
    else:
        conv = 0
    print("Itr: ",itr)
   
    itr += 1


#Page Rank Implementation ends
#######################################################################################################

    
perplexity_file.close()

#Sort on the basis of Page Rank
inverse_pr_graph = sorted(pr_p_graph.items(), key=operator.itemgetter(1), reverse = True)


#Write the top 50 Ranked pages to the file
file_handler = open("8.PageRank_G2.txt","w")
#file_handler = open("7.PageRank_G1.txt","w")

for i in range(0,50):
    file_handler.write(inverse_pr_graph[i][0]+"\t"+str(inverse_pr_graph[i][1])+"\n")

file_handler.close()


###########################################################################################################
#Rank by inlink count G1

'''
inlink_page_rank = {}

for link in inlink_graph:
    curr = {link: len(inlink_graph[link])}
    inlink_page_rank.update(curr)

sorted_inlink_rank = sorted(inlink_page_rank.items(), key=operator.itemgetter(1), reverse = True)

file_handler = open("page_rank_on_inlinks_G1.txt","w")

for i in range(0,5):
    file_handler.write(sorted_inlink_rank[i][0]+"\t"+str(sorted_inlink_rank[i][1])+"\n")

file_handler.close()'''

###########################################################################################################
#Rank by inlink count G2

'''
inlink_page_rank = {}

for link in inlink_graph:
    curr = {link: len(inlink_graph[link])}
    inlink_page_rank.update(curr)

sorted_inlink_rank = sorted(inlink_page_rank.items(), key=operator.itemgetter(1), reverse = True)

file_handler = open("page_rank_on_inlinks_G2.txt","w")

for i in range(0,5):
    file_handler.write(sorted_inlink_rank[i][0]+"\t"+str(sorted_inlink_rank[i][1])+"\n")

file_handler.close()'''
    











            















    
    


