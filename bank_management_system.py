import random

class Person:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

#_____________________________________________________________________________________

class User(Person):
    users = {}

    def __init__(self, name, email, address, account_type):
        super().__init__(name, email, address)
        self.account_type = account_type
        self.balance = 0
        self.account_number = str(random.randint(100,999)) + name[0:2]
        self.loan_count = 0
        self.loan_amount = 0  # Track total loan amount separately
        self.transaction_history = []
        self.serial = 0
        User.users[self.account_number] = self

    @staticmethod
    def create_account(name, email, address, account_type):
        user = User(name, email, address, account_type)
        print(f"User account is registered with AC Number: {user.account_number}")
        return user

    def deposit(self, amount):
        self.balance += amount
        self.serial += 1
        self.transaction_history.append(f"{self.serial}. Deposited: {amount}")
        print(f"Deposit: {amount}, Current Balance is: {self.balance}")

    def withdraw(self, amount):
        Admin.check_balance_of_bank()
        if Admin.bankruft:
            print("Bank is bankrupt!!")
            return 

        if amount > self.balance:
            print("Sorry, Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.serial += 1
            self.transaction_history.append(f"{self.serial}. Withdrawn: {amount}")
            print(f"Withdrawn {amount}, Current balance is: {self.balance}")

    def check_balance(self):
        print(f"Your Current balance: {self.balance}")

    def check_transaction_history(self):
        print("--------Transaction History---------")
        for transaction in self.transaction_history:
            print(transaction)
        
    def take_loan(self, amount):
        if not Admin.loan_allowed:
            print("Sorry, Loan feature is disabled.")
        elif self.loan_count >= 2:
            print("Sorry, You have reached your loan limit!")
        else:
            self.loan_count += 1
            self.loan_amount += amount  # Track loan amount separately
            self.balance += amount
            self.serial += 1
            self.transaction_history.append(f"{self.serial}. Loan taken: {amount}")
            print(f"Granted Loan: {amount}. Current balance: {self.balance}. Loans remaining: {2 - self.loan_count}")

    def transfer_money(self, amount, recipient_account):
        recipient = User.users.get(recipient_account)
        if amount > self.balance:
            print("Sorry, Insufficient balance")
        elif recipient is None:
            print(f"Account {recipient_account} does not exist")
        else:
            self.balance -= amount
            recipient.balance += amount
            self.serial += 1
            self.transaction_history.append(f"{self.serial}. Transferred {amount} to {recipient.account_number}")
            recipient.serial += 1
            recipient.transaction_history.append(f"{recipient.serial}. Received {amount} from {self.account_number}")
            print(f"Successfully transferred {amount} to {recipient.account_number}. Current balance: {self.balance}")

#______________________________________________________________________________________________

class Admin(Person):
    admins = {}
    loan_allowed = True
    bankruft = False

    def __init__(self, id, password):
        super().__init__(name="Admin", email="admin@gmail.com", address="Bank")
        self.id = id
        self.password = password

    @staticmethod
    def create_account(id, password):
        if id not in Admin.admins:
            admin = Admin(id, password)
            Admin.admins[id] = admin
            print("Admin account is registered")
        else:
            print("Already registered")

    def delete_user_account(self, account_number):
        if account_number in User.users:
            del User.users[account_number]
            print(f"{account_number} is deleted successfully")
        else:
            print(f"AC {account_number} does not exist")
        
    def see_user_list(self):
        if User.users:
            print("Account Number\tName\tBalance")
            for account_number, user in User.users.items():
                print(f"{account_number}\t{user.name}\t{user.balance}")
        else:
            print("No user available")

    @staticmethod
    def check_balance_of_bank():
        total_balance = 0
        for user in User.users.values():
            total_balance += user.balance
        print("Total Bank balance is:", total_balance)
        if total_balance == 0:
            Admin.bankruft = True
        else:
            Admin.bankruft = False

    def check_total_loan(self):
        total_loan_balance = 0
        for user in User.users.values():
            if user.loan_amount > 0:  # Track total loaned amount
                total_loan_balance += user.loan_amount
        print("Total loaned amount from the bank is:", total_loan_balance)

        
    @classmethod
    def dictate_loan_feature(self):
        Admin.loan_allowed = not Admin.loan_allowed
        status = 'enabled' if Admin.loan_allowed else 'disabled'
        print(f'Loan feature is now {status}')
  

#_______________________________________________________________________________________

def user_menu(user):
    while True:
        print('\n-----User Menu-----')
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Check Transaction History")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Logout")

        choice = int(input("Enter your choice: "))
        print("\n")
        if choice == 1:
            amount = int(input("Enter amount to deposit: "))
            user.deposit(amount)
        elif choice == 2:
            amount = int(input("Enter amount to withdraw: "))
            user.withdraw(amount)
        elif choice == 3:
            user.check_balance()
        elif choice == 4:
            user.check_transaction_history()    
        elif choice == 5:
            amount = int(input("Enter loan amount: "))
            user.take_loan(amount)
        elif choice == 6:
            recipient_number = input("Enter recipient AC Number: ")
            amount = int(input("Enter amount to transfer: "))
            user.transfer_money(amount, recipient_number)
        elif choice == 7:
            print('Logged out..')
            break
        else:
            print("Invalid choice")

#________________________________________________________________________________________________________

def admin_menu(admin):
    while True:
        print("\n----Admin Menu-----")
        print('1. Delete User Account')
        print('2. View Users')
        print('3. Check Total Balance')
        print('4. Check Total loan')
        print('5. Dictate loan feature')
        print('6. Logout')

        choice = int(input("Enter your choice: "))
        print("\n")
        if choice == 1:
            account_number = input("Enter account number to delete: ")
            admin.delete_user_account(account_number)
        elif choice == 2 : 
            admin.see_user_list()
        elif choice == 3:
            admin.check_balance_of_bank()
        elif choice == 4:
            admin.check_total_loan()
        elif choice == 5:
            admin.dictate_loan_feature()
        elif choice == 6:
            print('Logged out..')
            break
        else:
            print("Invalid choice")

#________________________________________________________________________________________________________

def main():
    while True:
        print("\n--- Bank Main Menu---")
        print("1. Register User")
        print("2. Register Admin")
        print("3. User Login")
        print("4. Admin Login")
        print("5. Exit")

        choice = int(input("Enter your choice: "))
        print("\n")
        if choice == 1:
            name = input("Enter Your Name: ")
            email = input("Enter Your Email: ")
            address = input("Enter Address: ")
            account_type = input("Enter account type (savings/current): ")
            User.create_account(name, email, address, account_type)
        elif choice == 2:
            id = int(input("Enter id: "))
            password = input("Enter password: ")
            Admin.create_account(id, password)
        elif choice == 3:
            account_number = input("Enter your account number: ")
            user = User.users.get(account_number)
            if user:
                user_menu(user)
            else:
                print(f'{account_number} does not exist')
        elif choice == 4:
            id = int(input("Enter admin's id: "))
            password = input("Enter admin's password: ")
            admin = Admin.admins.get(id)
            if admin and admin.password == password:
                admin_menu(admin)
            else:
                print("Incorrect Info")
        elif choice == 5:
            print('Shutting down main menu')
            break
        else:
            print('Incorrect choice..')

main()
