#Task 2: OOP

class BankAccount:
    def __init__(self, acc_num, acc_holder, bal_val):
        self.account_number = acc_num
        self.account_holder = acc_holder
        self.balance = bal_val

    def get_balance(self):
        return self.balance

    def get_account_number(self):
        return self.account_number

    def get_account_holder(self):
        return self.account_holder

    def withdraw(self, wv):
        if (wv <= self.balance):
            self.balance = self.balance - wv
            print(f"The amount of Rs.{wv} withdrawn successfully.")

        else:
            print(f"Not enough balance to withdraw Rs.{wv}")

    def deposit(self, dv):
        self.balance = self.balance + dv
        print(f"The amount of Rs.{dv} deposited successfully.")

    def print_acc_info(self):
        b = self.get_balance()
        print(f"Balance : " + str(b))
        an = self.get_account_number()
        print(f"Account Number: " + an)
        ah = self.get_account_holder()
        print(f"Account Holder: " + ah)


my_acc = BankAccount("E465g56", "Atharva Puranik", 10000)

while True:
    print("Press 1 to deposit.")
    print("Press 2 to withdraw.")
    print("Press 3 to print account info.")
    print("Press 4 to exit.")
    ip = int(input("Enter your input:"))

    if ip == 1:
        amount = int(input("Enter the amount to be deposited:"))
        my_acc.deposit(amount)
    elif ip == 2:
        amount = int(input("Enter the amount to be withdrawn:"))
        my_acc.withdraw(amount)
    elif ip == 3:
        my_acc.print_acc_info()
    elif ip == 4:
        print("Exiting.")
        break
    else:
        print("Invalid Input")