# Create a BankAccount class with methods for deposit, withdrawal, and balance
# inquiry. Add a child class DepositAccount and SavingsAccount with interest calculation.

# class BankAccount:
#     balance=0
#     def __init__(self,amount):
#         self.balance=float(amount)
#     def deposit(self,amount):
#         self.balance+=float(amount)
#     def withdrawal(self,amount):
#         current=self.balance
#         self.balance-=float(amount)
#         if(self.balance<0):
#             print(f"you cant withdraw {amount}Rs. your account has {current}Rs.")
#             self.balance+=float(amount)
#     def balanceInquiry(self):
#         print(self.balance)
#
# b1=BankAccount(10000)
# b1.deposit(500)
#
# b1.balanceInquiry()
# b1.withdrawal(100000)
# b1.balanceInquiry()
#


import datetime

accounts = []


class BankAccount:
    def __init__(self, aNumber, aHolder, balance=0.0):
        self.account_number = aNumber
        self.account_holder = aHolder
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Enter a valid amount to deposit.")
            return

        self.balance += amount
        print(f"New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Enter a valid amount to withdraw.")
            return

        if amount > self.balance:
            print("Insufficient balance.")
            return

        self.balance -= amount
        print(f"Remaining balance: ₹{self.balance}")

    def get_balance(self):
        return self.balance



class DepositAccount(BankAccount):
    def __init__(self, aNumber, aHolder, balance=0.0, interestRate=5.0):
        super().__init__(aNumber, aHolder, balance)
        self.interestRate = interestRate / 100

    def interest(self, months=1):
        minterestRate = self.interestRate / 12
        i = self.balance * (1 + minterestRate) ** months - self.balance
        self.balance += i
        print(f"New balance: ₹{round(self.balance, 2)}")


class SavingsAccount(BankAccount):
    def __init__(self, aNumber, aHolder, balance=0.0, interestRate=3.5):
        super().__init__(aNumber, aHolder, balance)
        self.interestRate = interestRate/ 100

    def interest(self, months=1):
        minterestRate = self.interestRate / 12
        i = self.balance * (1 + minterestRate) ** months - self.balance
        self.balance += i
        print(f"New balance: ₹{round(self.balance, 2)}")


def create_account():
    acc_num = input("enter account number: ")
    name = input("enter account holder name: ")
    acc_type = input("enter account Type (Savings/Deposit): ").lower()
    initial_balance = float(input("enter Initial Balance: "))

    if acc_type == "savings":
        account = SavingsAccount(acc_num, name, initial_balance)
    else:
        account = DepositAccount(acc_num, name, initial_balance)

    accounts.append(account)
    print("account created successfully!")


def find_account(acc_num):
    for account in accounts:
        if account.account_number == acc_num:
            return account
    return None


status = True
while status:
    print("\n1: Create Account 2: Deposit 3: Withdraw 4: Check Balance 5: Apply Interest 6:Exit")
    choice = int(input("enter your choice: "))

    if choice == 1:
        create_account()
    elif choice in [2, 3, 4, 5]:
        acc_num = input("enter account Number: ")
        account = find_account(acc_num)
        if not account:
            print("account not found!")
            continue

        if choice == 2:
            amount = float(input("enter amount to deposit: "))
            account.deposit(amount)
        elif choice == 3:
            amount = float(input("enter amount to withdraw: "))
            account.withdraw(amount)
        elif choice == 4:
            print(f"current balance: ₹{account.get_balance()}")
        elif choice == 5:
            months = int(input("enter number of months: "))
            account.interest(months)
    elif choice == 6:
            status = False

    else:
        print("enter a valid choice!")
