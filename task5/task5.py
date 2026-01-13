# Build a collection of users in a way that they can add,d
# search and delete their details. Users shall be able to add their
# memberId, name, luckyNumberPreference, hobbies, and booksTheyRead(name as well as author).


l1=[]
import Add_Details
status=True
print("1:add Details,2:search,3:delete,4:exit")
while status:
    choice = int((input("enter your Choice: ")))

    if(choice==1):
        l1.append(Add_Details.addDetails())
    elif(choice==2):
        name=input("enter your name: ")
        for i in range(len(l1)):
            if(l1[i].get("name")==name):
                print(l1[i])
    elif(choice==3):
        name=input("enter your name: ")
        index=0
        for i in range(len(l1)):
            if(l1[i].get("name")==name):
                index=i
                print(index)
        l1.pop(index)

        print("list after deleting: ",end=" ")
        print(l1)
    elif(choice==4):
        status=False
    else:
        print("enter valid no: ")
        exit()

