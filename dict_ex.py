
dict = {'a':[1,2,3],'b':[4,5,6],'c':[7,8,9]}

print(dict['a'])
print(dict['b'])
print(dict['c'])

dict['a'].append(10)
print(dict['a'])
print('a' in dict)

for key in dict:
    print(key,": ",dict[key])


