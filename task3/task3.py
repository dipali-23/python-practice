# Create a program that asks users for key-value pairs (name:age format)
# and builds a dictionary. Then display the oldest and youngest person group
# by age group as 18-35, 36-50, 51-65, and 66-90


print("(1 for add your details , 2 for see the details,3 for exit )")
status=True
dist = {}

while status:
    choice=input("Enter your Choice: ")
    name=""
    age=""

    def input_fn():
        name=input("enter your name: ")
        age=input("enter your age: ")
        dist.update({name:int(age)})
    def display():
        youngest_group={}
        second_group={}
        third_group={}
        oldest_group={}
        for key,value in dist.items():
            if(int(value)>=18 and int(value)<=35):
                youngest_group.update({key:value})
            elif(int(value)>=36 and int(value)<=50):
                second_group.update({key:value})
            elif(int(value)>=51 and int(value)<=65):
                third_group.update({key:value})
            elif(int(value)>66 and int(value)<=90):
                oldest_group.update({key:value})
        print("people of youngest group is: ")
        print(youngest_group)
        print("people of oldest group is: ")
        print(oldest_group)

    if(choice=="1"):
        input_fn()
    elif(choice=="2"):
        display()
    elif(choice=="3"):
        status=False
    else:
        print("enter valid no")
        exit()

