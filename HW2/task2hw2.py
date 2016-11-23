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

    
inlink_file = open("test_inlink_file.txt","r")
#inlink_file = open("wt2g_inlinks.txt","r")
inlinks = inlink_file.readlines()
inlink_file.close()
print("File Read: check")
inlink_graph = {}
pr_p_graph = {}
p_lq_graph = {}
links_from2 = []
links_keys = []


for link in inlinks:
    p = link.split()
    inlink_for = {p[0]:[]}
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
print(itr)
while conv < 4:
    sink_pr = 0
    for page in sink_pages:
        sink_pr += pr_p_graph[page]
    cnt = 0
    #for page in pr_p_graph:
    print("links_to",len(links_keys))
    for links in links_keys: 
        new_pr = (1-d)/N
        new_pr += d*sink_pr/N
        #print("Page no:",pageno)
        #print("links_keys: ",links_keys[pageno])
        mp = links_to_page(links)
        #print("length of mp:", len(mp))
        #for q in mp:
        for q in mp:
            #print(q," ",len(mp))
            pr_q = pr_p_graph[q]
            lq = p_lq_graph[q]
            new_pr += d*pr_q/lq
            #print(q,"lq: ",lq)

        pr_p_graph[link] = new_pr
        
    prplx2 = perplexity()
    change = prplx1-prplx2
    print("prplx1: ", prplx1)
    print("prplx2: ", prplx2)
    print("change: ",change)
    print("abs change: ",abs(change))
    prplx1 = prplx2
    if abs(change) < 1:
        conv += 1
    else:
        conv = 0
    print("Itr: ",itr)
   
    itr += 1
    #print(pr_p_graph)

print(sorted(pr_p_graph.values()))
for p in pr_p_graph:
    
    print (p," ",pr_p_graph[p])













            















    
    


