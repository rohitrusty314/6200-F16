import matplotlib.pyplot as plt
import math
'''
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()'''

file_handler = open("2_gram_frequency.txt","rb")
lines = file_handler.readlines()
l = 1
total = 0
rank_list = []
freq_list = []

for line in lines:
   # print(line)
    a = line.split()
    #print(a)
    rank_log = math.log10(l)
    rank_list.append(rank_log)

    freq = int(a[2].decode('utf-8'))
    total += int(a[2].decode('utf-8'))
    freq_list.append(freq)
    l += 1

    
    


file_handler.close()


p_log = []
for freq in freq_list:
    p = math.log10(freq/total)
    p_log.append(p)
    

plt.plot(rank_list,p_log,marker='+',color='black')
plt.ylabel('log10(Probability)')
plt.xlabel('log10(Rank)')
plt.show()
