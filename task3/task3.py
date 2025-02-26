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
                youngest_group.update({key:int(value)})
            elif(int(value)>=36 and int(value)<=50):
                second_group.update({key:int(value)})
            elif(int(value)>=51 and int(value)<=65):
                third_group.update({key:int(value)})
            elif(int(value)>66 and int(value)<=90):
                oldest_group.update({key:int(value)})
        l1=youngest_group.values()
        if(len(l1)>0):
            min_first=min(l1)
            max_first=max(l1)
            print(f"in group 18-35 youngest is: {list(youngest_group.keys())[list(youngest_group.values()).index(min_first)]} with age: {min_first}")
            print(f"in group 18-35 oldest is: {list(youngest_group.keys())[list(youngest_group.values()).index(max_first)]} with age: {max_first}")
        l2=second_group.values()
        if(len(l2)>0):
            min_second=min(l2)
            max_second=max(l2)
            print(min_second)
            print(f"in group 36-50 youngest is: {list(second_group.keys())[list(second_group.values()).index(min_second)]} with age: {min_second}")
            print(f"in group 36-50 youngest is: {list(second_group.keys())[list(second_group.values()).index(max_second)]} with age: {max_second}")
        l3 = third_group.values()
        if(len(l3)>0):
            min_third = min(l3)
            max_third = max(l3)

            print(f"in group 51-65 youngest is: {list(third_group.keys())[list(third_group.values()).index(min_third)]} with age: {min_third}")
            print(f"in group 51-65 youngest is: {list(third_group.keys())[list(third_group.values()).index(max_third)]} with age: {max_third}")
        l4 = oldest_group.values()
        if(len(l4)>0):
            min_fourth = min(l4)
            max_fourth = max(l4)
            print(f"in group 66-90 youngest is: {list(oldest_group.keys())[list(oldest_group.values()).index(min_fourth)]} with age: {min_fourth}")
            print(f"in group 66-90 youngest is: {list(oldest_group.keys())[list(oldest_group.values()).index(max_fourth)]} with age: {max_fourth}")


    if(choice=="1"):
        input_fn()
    elif(choice=="2"):
        display()
    elif(choice=="3"):
        status=False
    else:
        print("enter valid no")
        exit()

