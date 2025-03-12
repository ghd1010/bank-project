# Writing data to CSV file, from: https://www.geeksforgeeks.org/reading-and-writing-csv-files-in-python/
# menu format, from: https://pypi.org/project/simple-term-menu/
# terminal colors format, from: https://pypi.org/project/termcolor/
import csv 
import os
import sys
from termcolor import colored, cprint 
from simple_term_menu import TerminalMenu
# name of csv file  
my_csv_file = "bank.csv"

if not os.path.exists(my_csv_file):
    # field names  
    fields = ['account_id', 'first_name', 'last_name', 'password', 'balance_checking', 'balance_savings','num_of_overdrafts', 'is_active']  
    
    # data rows of csv file  
    rows = [[10001, 'suresh', 'sigera', 'juagw362', 1000, 10000, 0, True],  
            [10002, 'james', 'taylor', 'idh36%@#FGd', 10000, 10000, 0, True],  
            [10003, 'melvin', 'gordon', 'uYWE732g4ga1', 2000, 20000, 0, True],  
            [10004, 'stacey', 'abrams', 'DEU8_qw3y72$', 2000, 20000, 0, True],  
            [10005, 'jake', 'paul', 'd^dg23g)@', 100000, 100000, 0, True]]  

    # writing to csv file  
    with open(my_csv_file, mode ='w', newline="") as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows)

class Customer:

    new_id = 0
    
    def __init__(self, first_name, last_name, password, balance_checking=0, balance_savings=0, num_of_overdrafts=0, is_active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings
        self.num_of_overdrafts = num_of_overdrafts
        self.is_active = is_active

    # create a default ID to customers when we add them
    def create_account_id(self):
        number_of_existing_customers = 0 # initialize variable
        with open(my_csv_file, mode ='r') as csvfile:
            content = csv.reader(csvfile)
            next(content)  # skip the header row (first row)
            for lines in content: # rows loop
                if lines:  # if the file is not empty
                    number_of_existing_customers += 1  # increment for each existing customer
        
        new_id = 10001 + number_of_existing_customers # generate new ID according to existing customers
        return new_id

    # append the new customer to the csv file
    def add_customer_to_csv(self):
        try:
            # check for empty first or last name before processing the csv file
            if not self.first_name or not self.last_name:
                print(colored("Sorry, first name or last name is empty. Please enter a valid alphabetic input.", 'yellow'))
                return False
            
            # check if first name or last name contains numbers
            elif self.first_name.isdigit() or self.last_name.isdigit():
                print(colored("Sorry, first name or last name should not be numbers.", 'yellow'))
                return False
            
            # check if the customer already exists in the csv file
            with open(my_csv_file, mode='r') as csvfile:
                content = csv.reader(csvfile)
                next(content)  # skip header
                
                for line in content:
                    if len(line) > 2 and line[1].lower() == self.first_name.lower() and line[2].lower() == self.last_name.lower():
                        print(colored(f"Sorry, customer with name ({self.first_name} {self.last_name}) already exists.",'yellow'))
                        return False

            # create a list for the new customer
            new_customer = [
                self.create_account_id(),
                self.first_name,
                self.last_name,
                self.password,
                self.balance_checking,
                self.balance_savings,
                self.num_of_overdrafts,
                self.is_active
            ]

            # append the new customer to the csv file
            with open(my_csv_file, mode='a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(new_customer)

                account_id = new_customer[0]
                print(colored("\nYou have signed up successfully! Please login to the system.", "light_blue"))
                print(colored(f"Your account ID is: {account_id} \n", "grey"))

                return True

        except FileNotFoundError:
            print(f"Sorry, the CSV file ({my_csv_file}) is not found. Please make sure you have the correct file.")
            return False

class Account:
    def __init__(self, account_id, balance_checking, balance_savings, num_of_overdrafts, is_active):
        self.account_id = account_id
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings
        self.num_of_overdrafts = num_of_overdrafts
        self.is_active = is_active

    def update_balance(self, account_id, new_balance, account_type):
        
        updated_info = []
        
        # assign the correct balance to the correct account type
        if account_type == "checking":
            balance_col = "balance_checking"
        elif account_type == "savings":
            balance_col = "balance_savings"

        # read the existing data and update the balance for the correct account
        with open(my_csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)  #got info from: https://docs.python.org/3/library/csv.html
            fieldnames = reader.fieldnames
            for row in reader:
                #by default, csv.DictReader reads all values as strings
                if row["account_id"] == str(account_id):  # check account
                    row[balance_col] = str(new_balance) #update balance
                updated_info.append(row)

        # write updated data to csv file
        with open(my_csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_info)
            
    
    def balance_checking_deposit(self, amount):
        if type(amount) == str:
            print(colored('Sorry, amount should be a number.', 'yellow'))
            return False
        elif amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        else:
            self.balance_checking += amount
            self.update_balance(self.account_id, self.balance_checking, "checking")  # write to csv file
            print(colored(f"Deposit successful! New balance: ${self.balance_savings}", "light_blue"))
            return self.balance_checking
    
    def balance_savings_deposit(self, amount):
        if type(amount) == str:
            print(colored('Sorry, amount should be a number.', 'yellow'))
            return False
        if amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        else:
            self.balance_savings += amount
            self.update_balance(self.account_id, self.balance_savings, "savings")  # write to csv file
            print(colored(f"Deposit successful! New balance: ${self.balance_savings}", "light_blue"))
            return self.balance_savings
    
    def balance_checking_withdraw(self, amount):
        
        overdraft_amount = 35
        if type(amount) == str:
            print(colored('Sorry, amount should be a number.', 'yellow'))
            return False
        # make sure that the amount is not zero or negative
        if amount < 0:
            print(colored('Sorry, you can\'t withdraw a negative number. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        if amount == 0:
            print(colored('Sorry, you can\'t withdraw zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        
        # check on the balance, if the balance > 0 :
        # successful witdrawal
        if self.balance_checking >= amount:
            self.balance_checking -= amount
            self.update_balance(self.account_id, self.balance_checking, "checking")  # write to csv file
            print(colored(f"Withdrawal successful! New balance: ${self.balance_checking}", "light_blue"))
            return self.balance_checking
            
        if self.balance_checking < 0 and amount > 100:
            # cannot withdraw more than 100$
            print(colored('Withdrawal denied: Cannot withdraw more than $100 when account is negative', 'yellow'))
            return False
            
        # the account cannot have a resulting balance of less than -$100 (range)
        if(self.balance_checking - amount - overdraft_amount) < -100:
            print(colored("Withdrawal denied: Overdraft limit of -$100", 'yellow'))
            return False
                
        # apply protection overdraft
        self.balance_checking -= (amount + overdraft_amount)
        self.num_of_overdrafts += 1
        print(colored(f'Overdraft! Charged $35 fee. new balance: ${self.balance_checking}', 'light_blue'))
                
        # deactivate account after applying 2 overdrafts
        if self.num_of_overdrafts >= 2:
            self.is_active = False
            print(colored('Account deactivated.', 'yellow'))
            
        self.update_balance(self.account_id, self.balance_checking, "checking")  # write to csv file
        return self.balance_checking

    # def balance_savings_withdraw(self, amount):
    #     overdraft_amount = 35
    #     # make sure that the amount is not zero or negative
    #     if amount < 0:
    #         print(colored('Sorry, you can\'t withdraw a negative number. Please ensure it is a positive non-zero number'), 'yellow')
    #         return False
    #     if amount == 0:
    #         print(colored('Sorry, you can\'t withdraw zero. Please ensure it is a positive non-zero number'), 'yellow')
    #         return False
        
    #     # check on the balance, if the balance > 0 :
    #     # successful witdrawal
    #     if self.balance_savings >= amount:
    #         self.balance_savings -= amount
    #         print(colored(f"Withdrawal successful! New balance: ${self.balance_savings}", "light_blue"))
    #         return self.balance_savings
            
        
    #     if self.balance_savings < 0 and amount > 100:
    #         # cannot withdraw more than 100$
    #         print(colored('Withdrawal denied: Cannot withdraw more than $100 when account is negative', 'yellow'))
    #         return False
            
    #     # the account cannot have a resulting balance of less than -$100 (range)
    #     if(self.balance_savings - amount - overdraft_amount) < -100:
    #         print(colored("Withdrawal denied: Overdraft limit of -$100", 'yellow'))
    #         return False
                
    #     # apply protection overdraft
    #     self.balance_savings -= (amount + overdraft_amount)
    #     self.num_of_overdrafts += 1
    #     print(colored(f'Overdraft! Charged $35 fee. new balance: ${self.balance_savings}', 'light_blue'))
                
    #     # deactivate account after applying 2 overdrafts
    #     if self.num_of_overdrafts >= 2:
    #         self.is_active = False
    #         print(colored('Account deactivated.', 'yellow'))

    #     return self.balance_savings

# class Transactions:
    
#     def __init__(self, account_id):
#         self.account_id = account_id
        
    





# def main():
# #------------------------------------------------------------#
#         # read the csv file once and store customer data
# #------------------------------------------------------------#

#     customers_data = []
#     with open(my_csv_file, mode='r') as csvfile:
#         content = csv.reader(csvfile)
#         next(content)  # skip header row
#         customers_data = [line for line in content]  # store all customers in customers_data list
    
# #------------------------------------------------------------#
#                         # MENU intro
# #------------------------------------------------------------#
#     welcome_text = colored('''                         🏦 Welcome to ACME Bank 🏦''', 'green')
#     question_text = colored('''                       What are you looking for today?''', 'light_blue')

#     full_text = f"\n{welcome_text}\n{question_text}\n"

#     print(full_text)
# #------------------------------------------------------------#
#                     # Sign up - Login options
# #------------------------------------------------------------#
#     options1 = ["Sign up", "Login"]
#     terminal_menu = TerminalMenu(options1)
#     menu_entry_index = terminal_menu.show()

#     if options1[menu_entry_index] == options1[0]: # sign up
#         customer_fname = input(colored('Please enter your first name: ' ,'green'))
#         customer_lname = input(colored('Please enter your last name: ' ,'green'))
#         customer_password= input(colored('Please enter your password: ' ,'green'))

#         customer = Customer(customer_fname, customer_lname, customer_password)
#         customer.add_customer_to_csv()

#     elif options1[menu_entry_index] == options1[1]: # login
#         customer_ID = input(colored('Please enter your ID: ' ,'green'))
#         customer_password= input(colored('Please enter your password: ' ,'green'))
        
#         # login process
#         customer_login_info = None
#         for line in customers_data:
#             if line[0] == customer_ID and line[3] == customer_password:
#                 customer_login_info = line
#                 break
#             if customer_login_info:
#                 print(colored(f'''\n                             Hello, {customer_login_info[1]}!\n''', 'light_blue'))
#                 # create account obj for the loggedin customer:
#                 customer_logged_account = Account(
#                     customer_login_info[0],
#                     float(customer_login_info[1]),
#                     float(customer_login_info[2]),
#                     int(customer_login_info[3]),
#                     customer_login_info[4]
#                 )
#         #------------------------------------------------------------#
#             # after successful login, choose an operations
#         #------------------------------------------------------------#
#                 options2 = ["Withdraw", "Deposit", "Transfer"]
#                 terminal_menu = TerminalMenu(options2)
#                 login_menu = terminal_menu.show()
#         #------------------------------------------------------------#
#                                 # Withdraw
#         #------------------------------------------------------------#
#                 if options2[login_menu] == options2[0]: #for withdraw function
#                     print('Account:')
#                     options3 = ["Checking account", "Savings account"]
#                     terminal_menu = TerminalMenu(options3)
#                     accounts_menu1 = terminal_menu.show()
#         #------------------------------------------------------------#
#                                 # Withdraw - choose acc
#         #------------------------------------------------------------#
#                     if options3[accounts_menu1] == options3[0]: # checking account
#                         print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
#                         amount = input(colored('Please enter the amount: ','green'))
#                         try:
#                             float(amount)
#                             new_checking_acc_balance = customer_logged_account.balance_checking_withdraw(amount)
#                             if new_checking_acc_balance != False:
#                                 print(colored(f"Withdraw successful! New checking account balance: $ {new_checking_acc_balance} $", 'light_blue'))
#                         except ValueError:
#                             print(colored("Sorry, invalid input. Please enter a positive number", 'yellow'))

#                     elif options3[accounts_menu1] == options3[1]: # savings account
#                         print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))
#                         amount = input(colored('Please enter the amount: ','green'))
#                         try:
#                             float(amount)
#                             new_savings_acc_balance = customer_logged_account.balance_savings_withdraw(amount)
#                             if new_savings_acc_balance != False:
#                                 print(colored(f"Withdraw successful! New checking account balance: $ {new_savings_acc_balance} $", 'light_blue'))
#                         except ValueError:
#                             print(colored("Sorry, invalid input. Please enter a positive number", 'yellow'))
#         #------------------------------------------------------------#
#                                 # Deposit
#         #------------------------------------------------------------#

#                 if options2[login_menu] == options2[1]: #for deposit function
#                     print('Account:')
#                     options4 = ["Checking account", "Savings account"]
#                     terminal_menu = TerminalMenu(options4)
#                     accounts_menu2 = terminal_menu.show()
#         #------------------------------------------------------------#
#                                 # Deposit - choose acc
#         #------------------------------------------------------------#
#                     if options4[accounts_menu2] == options4[0]: # checking account
#                         print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
#                         amount = input(colored('Please enter the amount: ','green'))
#                         try:
#                             float(amount)
#                             new_checking_acc_balance = customer_logged_account.balance_checking_deposit(amount)
#                             if new_checking_acc_balance != False:
#                                 print(colored(f"Deposit successful! New checking account balance: $ {new_checking_acc_balance} $", 'light_blue'))
#                         except ValueError:
#                             print(colored("Sorry, invalid input. Please enter a positive number", 'yellow'))

#                     elif options4[accounts_menu2] == options4[1]: # savings account
#                         print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))
#                         amount = input(colored('Please enter the amount: ','green'))
#                         try:
#                             float(amount)
#                             new_savings_acc_balance = customer_logged_account.balance_savings_deposit(amount)
#                             if new_savings_acc_balance != False:
#                                 print(colored(f"Deposit successful! New checking account balance: $ {new_savings_acc_balance} $", 'light_blue'))
#                         except ValueError:
#                             print(colored("Sorry, invalid input. Please enter a positive number", 'yellow'))

#         #------------------------------------------------------------#
#                                 # Transfer
#         #------------------------------------------------------------#
#                 elif options2[login_menu] == options2[2]: #for transfer function
#                     pass
#                     break
#             else:
#                 print(colored("\nSorry, invalid ID or password. Please try again.", "yellow"))


# if __name__ == "__main__":
#     main()