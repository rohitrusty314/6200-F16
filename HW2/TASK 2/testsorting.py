import operator
x = {'a': 2, 'b': 4, 'c': 0, 'd': 1, 'e': 0}
print(x)
sorted_x = sorted(x.items(), key=operator.itemgetter(1),reverse = True)
print(sorted_x)
