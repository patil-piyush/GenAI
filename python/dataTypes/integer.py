import sys

a=5
b=10

c=a+b
print(c)
print(id(a))
a=12
print(a)
print(id(a))


# integer is immutable 
# reason - because when you change the value of a variable, the variable itself is not changing but the address at which the variable is pointing is changed

# same for all inbuild datatypes



chai = 100
patti = 200

print(f"chai and patti is equal to chai*patti that is {chai*patti}")