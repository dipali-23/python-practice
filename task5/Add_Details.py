


def addDetails():
    id=input("enter your id: ")
    name = input("enter your name: ")
    luckyNo = input("enter your lucky no: ")
    hobbies = []
    ho_no = input("how many hobbies do you have: ")
    print("enter your hobbies: ", end=" ")
    for i in range(int(ho_no)):
        hobbies.append(input())

    print("enter book you read with author: ", end=" ")
    book = []
    book.append(input())
    book.append(input())
    d = {"id": id, "name": name, "lucky_no": luckyNo, "hobbies": hobbies, "book": book}
    return d