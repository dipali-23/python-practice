# From a list of any 1000 numbers, create three new data collections:
# even numbers, numbers multiplier of 17, and numbers greater than a user-specified
# input number


import random
l=[]
listofno=[10,100,1000,10000,100000]
for i in range(1000):
    l.append(int(random.random()*random.choice(listofno)))
print(l)
even_no=set()
no_multiplier_17=set()
no_grater_choice=set()
no=int(input("enter your favourite no: "))
for i in l:
    if(i%2==0):
        even_no.add(i)
    if(i%17==0):
        no_multiplier_17.add(i)
    if(i>no):
        no_grater_choice.add(i)
print("Even no: ",end=' ')
print(even_no)
print("numbers multiplier of 17: ",end=' ')
print(no_multiplier_17)
print("numbers greater than a user-specified input number: ",end=' ')
print(no_grater_choice)


