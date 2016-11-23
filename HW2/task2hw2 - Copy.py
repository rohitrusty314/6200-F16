import math

def initial_PR():
    for key in inlink_graph:
        value = {key:1/N}
        pr_p_graph.update(value)
    print("initial page rank:",1/N)


def perplexity():
    H = 0
    
    for key in pr_p_graph:
        H += pr_p_graph[key] * math.log(pr_p_graph[key],2)
        
    H = -1 * H
    perplexity = math.pow(2,H)
    return perplexity


def links_to_page(p):
    mp = inlink_graph[p]
    return mp


        
def get_sink_pages():
    
    links_from = []
    
    sink_pages = []
    pageno = 0

    links_from = list(inlink_graph.values())
    for k in range(0,len(links_from)):
            for u in links_from[k]:
                links_from2.append(u)
                
    links_to = list(inlink_graph.keys())
    print(len(links_to))
    print(len(set(links_from2)))
        

    sink_pages = list(set(links_to)-set(links_from2))
    print("Sink page count: ",len(sink_pages))
    return sink_pages

    
#inlink_file = open("test_inlink_file.txt","r")
inlink_file = open("wt2g_inlinks.txt","r")
inlinks = inlink_file.readlines()
inlink_file.close()
print("File Read: check")
inlink_graph = {}
pr_p_graph = {}
p_lq_graph = {}
links_from2 = []
links_keys = []
new_pr = {}


for link in inlinks:
    p = link.split()
    inlink_for = {p[0]:[]}
    curr_new = {p[0]:[0.0]}
    new_pr.update(curr_new)
    
    for i in range (1,len(p)):
        inlink_for[p[0]].append(p[i])
        if p[i] in p_lq_graph:
           p_lq_graph[p[i]] += 1
        else:
            curr = {p[i]:1}
            p_lq_graph.update(curr)
        
        
    inlink_graph.update(inlink_for)


print("p_lq_graph len: ",len(p_lq_graph))
print("inlink_graph: check")
N = len(inlink_graph)
print(N)
initial_PR()


sink_pages = get_sink_pages()
print("Count of sink pages:",len(sink_pages))
links_keys = list(inlink_graph.keys())

conv = 0
d = 0.85
prplx1 = perplexity()
prplx2 = 0
change = prplx1-prplx2

print("Getting out links count:")


itr = 0
#print(itr)
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

    sum_pr = 0
    for links in links_keys:
        sum_pr += new_pr[links]
        pr_p_graph[links] = new_pr[links]

    file_handler = open("pr_p_graph.txt","w")
    for p in pr_p_graph:
        file_handler.write(str(p)+" "+str(pr_p_graph[p])+"\n")

    file_handler.close()
    break

    #print("sink_pr: ",sink_pr)
    prplx2 = perplexity()
    change = abs(prplx1-prplx2)
    print("SUM PR: ",sum_pr)
    #print("prplx1: ", prplx1)
    #print("prplx2: ", prplx2)
    print("abs change: ",change)
    prplx1 = prplx2
    if change < 1:
        conv += 1
    else:
        conv = 0
    print("Itr: ",itr)
   
    itr += 1
    #print(pr_p_graph)

#print(sorted(pr_p_graph.values()))

file_handler = open("p_lq.txt","w")
for p in p_lq_graph:
    file_handler.write(str(p)+" "+str(p_lq_graph[p])+"\n")

file_handler.close()
#for p in pr_p_graph:
 #   print (p," ",pr_p_graph[p])

#print(p_lq_graph)

#file_handler = open("pr_p_graph.txt","w")
#for p in pr_p_graph:
 #   file_handler.write(str(p)+" "+str(pr_p_graph[p])+"\n")

#file_handler.close()













            















    
    


