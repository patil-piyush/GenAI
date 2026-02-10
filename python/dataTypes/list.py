listA = [1,2,3,4,5]
listB = [6,7,8,9,10]
print(listA)
print(listB)

listc = listA + listB
listA.extend(listB)
print(listA)
print(listc)

var = listA.pop()
print(var)
print(max(listA))
print(min(listA))
print(max(listB))
print(min(listB))