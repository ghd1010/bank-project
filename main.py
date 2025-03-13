# Writing data to CSV file, from: https://www.geeksforgeeks.org/reading-and-writing-csv-files-in-python/
# menu format, from: https://pypi.org/project/simple-term-menu/
# terminal colors format, from: https://pypi.org/project/termcolor/
import csv 
import os
from termcolor import colored
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

    def update_balance(self, account_id, new_balance, account_type, num_of_overdrafts, is_active):
        
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
                    row[balance_col] = str(new_balance) # update balance
                    row["num_of_overdrafts"] = str(num_of_overdrafts) # update num_of_overdrafts
                    row["is_active"] = str(is_active) # update is_active
                updated_info.append(row)

        # write updated data to csv file
        with open(my_csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_info)
            
    
    def balance_checking_deposit(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            print(colored("Sorry, invalid amount. Please enter a numeric value.", "yellow"))
            return False
        if amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        else:
            self.balance_checking += amount
            self.update_balance(self.account_id, self.balance_checking, "checking", self.num_of_overdrafts, self.is_active)  # write to csv file
            print(colored(f"Deposit successful! New balance: ${self.balance_checking}", "light_blue"))
            return self.balance_checking
        
    def reactivate_account(self, deposit_amount):
        overdraft_amount = 35 
        activate_total = abs(self.balance_checking) + overdraft_amount # total amount needed to reactivate

        if deposit_amount >= activate_total:
            self.balance_checking += deposit_amount  
            self.num_of_overdrafts = 0
            self.is_active = True 
            self.update_balance(self.account_id, self.balance_checking, "checking", self.num_of_overdrafts, self.is_active)
            print(colored(f"Account reactivated! New balance: ${self.balance_checking}", "light_blue"))
        else:
            print(colored(f"Sorry, your account is still deactivated. You need at least ${activate_total} to bring the account current.", "yellow"))
    
    def balance_savings_deposit(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            print(colored("Sorry, invalid amount. Please enter a numeric value.", "yellow"))
            return False
        if amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
            
        self.balance_savings += amount
        self.update_balance(self.account_id, self.balance_savings, "savings", self.num_of_overdrafts, self.is_active)  # write to csv file
        print(colored(f"Deposit successful! New balance: ${self.balance_savings}", "light_blue"))
        return self.balance_savings
    
    def balance_checking_withdraw(self, amount):
        overdraft_amount = 35
        try:
            amount = float(amount)
        except ValueError:
            print(colored("Sorry, invalid amount. Please enter a numeric value.", "yellow"))
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
            self.update_balance(self.account_id, self.balance_checking, "checking" ,self.num_of_overdrafts, self.is_active)  # write to csv file
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
        print(colored(f'Overdraft! Charged $35 fee, new balance: ${self.balance_checking}', 'light_blue'))
                
        # deactivate account after applying 2 overdrafts
        if self.num_of_overdrafts >= 2:
            self.is_active = False
            print(colored('Account deactivated.', 'yellow'))
            
        self.update_balance(self.account_id, self.balance_checking, "checking" ,self.num_of_overdrafts, self.is_active)  # write to csv file
        return self.balance_checking

    def balance_savings_withdraw(self, amount):
        overdraft_amount = 35
        try:
            amount = float(amount)
        except ValueError:
            print(colored("Sorry, invalid amount. Please enter a numeric value.", "yellow"))
            return False
        # make sure that the amount is not zero or negative
        if amount < 0:
            print(colored('Sorry, you can\'t withdraw a negative number. Please ensure it is a positive non-zero number'), 'yellow')
            return False
        if amount == 0:
            print(colored('Sorry, you can\'t withdraw zero. Please ensure it is a positive non-zero number'), 'yellow')
            return False
        
        # check on the balance, if the balance > 0 :
        # successful witdrawal
        if self.balance_savings >= amount:
            self.balance_savings -= amount
            self.update_balance(self.account_id, self.balance_checking, "savings", self.num_of_overdrafts, self.is_active)  # write to csv file
            print(colored(f"Withdrawal successful! New balance: ${self.balance_savings}", "light_blue"))
            return self.balance_savings
            
        
        if self.balance_savings < 0 and amount > 100:
            # cannot withdraw more than 100$
            print(colored('Withdrawal denied: Cannot withdraw more than $100 when account is negative', 'yellow'))
            return False
            
        # the account cannot have a resulting balance of less than -$100 (range)
        if(self.balance_savings - amount - overdraft_amount) < -100:
            print(colored("Withdrawal denied: Overdraft limit of -$100", 'yellow'))
            return False
                
        # apply protection overdraft
        self.balance_savings -= (amount + overdraft_amount)
        self.num_of_overdrafts += 1
        print(colored(f'Overdraft! Charged $35 fee, new balance: ${self.balance_savings}', 'light_blue'))
                
        # deactivate account after applying 2 overdrafts
        if self.num_of_overdrafts >= 2:
            self.is_active = False
            print(colored('Account deactivated.', 'yellow'))

        self.update_balance(self.account_id, self.balance_checking, "savings", self.num_of_overdrafts, self.is_active)  # write to csv file
        return self.balance_savings
    


class Transactions:
    
    def __init__(self, account_id, is_active):
        self.account_id = account_id
        self.is_active = is_active

    def transfer_between_accounts(self, amount, from_account, to_account):
        
        updated_info = []
        found = False
        
        try:
            amount = float(amount)
        except ValueError:
            print(colored("Sorry, invalid amount. Please enter a numeric value.", "yellow"))
            return False
        
        if amount <= 0:
            print(colored("Transfer amount must be greater than zero", "yellow"))
            return False
        
        if from_account == "checking" and to_account == "savings":
            from_col = "balance_checking"
            to_col = "balance_savings"
        elif from_account == "savings" and to_account == "checking":
            from_col= "balance_savings"
            to_col = "balance_checking"
        else:
            print(colored("Invalid account type. Please use'checking' or 'savings'", "yellow"))
            return False
        
        with open(my_csv_file, mode="r", newline="") as file: # read csv file
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                    if row["account_id"] == str(self.account_id):
                        found = True
                        from_balance = float(row[from_col])
                        to_balance = float(row[to_col])

                        if not self.is_active:
                            print(colored(f"Account {self.account_id} is inactive. Transfer not allowed", "yellow"))
                            return False

                        if from_balance >= amount:
                            row[from_col] = str(from_balance - amount)
                            row[to_col] = str(to_balance + amount)
                            print(colored(f"Transfer successful! ${amount} moved from {from_account} to {to_account}", "light_blue"))
                        else:
                            print(colored(f"Sorry, ${amount} is more than the balance of the {from_account} account", "yellow"))
                            return False
                    
                    updated_info.append(row)

            if not found:
                print(colored("Account not found", "yellow"))
                return False
            
            with open(my_csv_file, mode="w", newline="") as file: # write the updated info
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_info)
        
            return True
    
    def transfer_to_other_user(self, amount, from_account, to_account_id):

        try:
            amount = float(amount)
        except ValueError:
            print(colored("Invalid amount. Please enter a numeric value", "yellow"))
            return False
        try:
            to_account_id = int(to_account_id)
        except ValueError:
            print(colored("Invalid recipient ID. Please enter a numeric value", "yellow"))
            return False
                
        if amount <= 0:
            print(colored("Transfer amount must be greater than zero", "yellow"))
            return False
        
        if from_account == "checking":
            sender_col = "balance_checking"
        elif from_account == "savings":
            sender_col= "balance_savings"
        else:
            print(colored("Invalid account type. Please use'checking' or 'savings'", "yellow"))
            return False
        
        updated_info = []
        sender_found = False
        beneficiary_found = False
        sender_balance = 0
        beneficiary_balance = 0
        
        with open(my_csv_file, mode="r", newline="") as file: # read csv file
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            
            for row in reader:
                #---------- sender account ----------#
                if row["account_id"] == str(self.account_id):  
                    sender_found = True
                    sender_balance = float(row[sender_col])
                    sender_is_active = row["is_active"].strip().lower() == "true"
                    # print(sender_is_active)
                    
                    if sender_is_active == False:
                        print(colored(f"Sorry, you can't transfer due to your inactive account", "yellow"))
                        return False

                    if sender_balance < amount:
                        print(colored(f"Sorry, ${amount} is more than the balance of the account", "yellow"))
                        return False

                    row[sender_col] = str(sender_balance - amount) # apply the transfer
                    
                #---------- beneficiary account ----------#
                if row["account_id"] == str(to_account_id): 
                    beneficiary_found = True
                    beneficiary_is_active = row["is_active"].strip().lower() == "true"
                    # print(beneficiary_is_active)

                    if beneficiary_is_active == False:
                        print(colored(f"Sorry, the account you are trying to transfer to is inactive", "yellow"))
                        return False
                    
                    beneficiary_balance = float(row["balance_checking"])  # transfer money to checking account
                    row["balance_checking"] = str(beneficiary_balance + amount)  # apply transfer

                updated_info.append(row)

        if not sender_found:
            print(colored("Sender account not found", "yellow"))
            return False

        if not beneficiary_found:
            print(colored("Beneficiary account not found", "yellow"))
            return False

        with open(my_csv_file, mode="w", newline="") as file: # write the updated info
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_info)

        print(colored(f"Transfer successful! ${amount} sent to account {to_account_id}", "light_blue"))
        return True


def main():
    #------------------------------------------------------------#
    #      read the csv file once and store customer data
    #------------------------------------------------------------#
    customers_data = []
    with open(my_csv_file, mode='r') as csvfile:
        content = csv.reader(csvfile)
        next(content)  # skip header row
        customers_data = [line for line in content]  # store all customers in customers_data list
    #------------------------------------------------------------#
    #                       MENU intro
    #------------------------------------------------------------#
    welcome_text = colored('''                         🏦 Welcome to ACME Bank 🏦''', 'green')
    question_text = colored('''                       What are you looking for today?''', 'light_blue')

    full_text = f"\n{welcome_text}\n{question_text}\n"

    print(full_text)
    #------------------------------------------------------------#
    #                Sign up - Login options
    #------------------------------------------------------------#
    options_A = ["Sign up", "Login", "Exit"]
    terminal_menu = TerminalMenu(options_A)
    menu_entry_index = terminal_menu.show()

    if options_A[menu_entry_index] == options_A[0]:  # sign up
        customer_fname = input(colored('Please enter your first name: ', 'green'))
        customer_lname = input(colored('Please enter your last name: ', 'green'))
        customer_password = input(colored('Please enter your password: ', 'green'))

        customer = Customer(customer_fname, customer_lname, customer_password)
        customer.add_customer_to_csv()

    elif options_A[menu_entry_index] == options_A[1]:  # login
        customer_ID = input(colored('Please enter your ID: ', 'green'))
        customer_password = input(colored('Please enter your password: ', 'green'))
        # print("Loaded Customer Data:", customers_data)  #DEBUGGING
        # login process
        customer_login_info = None
        for line in customers_data:
            if line[0] == customer_ID and line[3] == customer_password:
                customer_login_info = line
                break
            
        if customer_login_info:
            print(colored(f'''\n                             Hello, {customer_login_info[1]}!\n''', 'light_blue'))
            # create account obj for the loggedin customer:
            customer_logged_account = Account(
                int(customer_login_info[0]), # acc id
                float(customer_login_info[4]), # checking balance
                float(customer_login_info[5]), # savings
                int(customer_login_info[6]), # overdrafts count
                bool(customer_login_info[7]) #is_active
            )
            # create transaction obj for the loggedin customer:
            transaction = Transactions(
                        customer_logged_account.account_id,
                        customer_logged_account.is_active
            )
            #------------------------------------------------------------#
            #       after successful login, choose an operations
            #------------------------------------------------------------#
            while True:
                options_B = ["Withdraw", "Deposit", "Transfer", "Logout"]
                terminal_menu = TerminalMenu(options_B)
                login_menu = terminal_menu.show()
            #------------------------------------------------------------#
            #                         Withdraw
            #------------------------------------------------------------#
                if options_B[login_menu] == options_B[0]: # withdraw
                    print('Account:')
                    options_C = ["Checking account", "Savings account"]
                    terminal_menu = TerminalMenu(options_C)
                    accounts_menu1 = terminal_menu.show()
            #------------------------------------------------------------#
            #                  Withdraw - choose acc
            #------------------------------------------------------------#
                    if options_C[accounts_menu1] == options_C[0]:  # checking account
                        print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                        amount = input(colored('Please enter the amount: ', 'green'))
                        customer_logged_account.balance_checking_withdraw(amount)

                    elif options_C[accounts_menu1] == options_C[1]:  # savings account
                        print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))
                        amount = input(colored('Please enter the amount: ', 'green'))
                        customer_logged_account.balance_savings_withdraw(amount)
            #------------------------------------------------------------#
            #                         Deposit
            #------------------------------------------------------------#
                elif options_B[login_menu] == options_B[1]: # deposit
                    print('Account:')
                    options_D = ["Checking account", "Savings account"]
                    terminal_menu = TerminalMenu(options_D)
                    accounts_menu2 = terminal_menu.show()
            #------------------------------------------------------------#
            #                  Deposit - choose acc
            #------------------------------------------------------------#
                    if options_D[accounts_menu2] == options_D[0]:  # checking account
                        print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                        amount = input(colored('Please enter the amount: ', 'green'))
                        customer_logged_account.balance_checking_deposit(amount)

                    elif options_D[accounts_menu2] == options_D[1]:  # savings account
                        print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))
                        amount = input(colored('Please enter the amount: ', 'green'))
                        customer_logged_account.balance_savings_deposit(amount)                    
                    
            #------------------------------------------------------------#
            #                          Transfer
            #------------------------------------------------------------#
                elif options_B[login_menu] == options_B[2]:
                    print('Transfer to:')
                    options_E = ["Between your own accounts", "To other account ID"]
                    terminal_menu = TerminalMenu(options_E)
                    accounts_menu3 = terminal_menu.show()
            #------------------------------------------------------------#
            #                 Transfer - own accounts
            #------------------------------------------------------------#
                    if options_E[accounts_menu3] == options_E[0]:  # between own accounts
                        print('Choose:')
                        options_F = ["From checking -> savings", "From savings -> checking"]
                        terminal_menu = TerminalMenu(options_F)
                        chooseMenu = terminal_menu.show()
            #------------------------------------------------------------#
            #     Transfer - From checking -> savings and vice versa
            #------------------------------------------------------------#
                        if options_F[chooseMenu] == options_F[0]:  # From checking -> savings
                            print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                            print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))
                            amount = input(colored('To transfer money from checking -> savings account,\nplease enter the amount: ', 'green'))
                            transaction.transfer_between_accounts(amount, "checking", "savings")

                        elif options_F[chooseMenu] == options_F[1]:  # From savings -> checking
                            print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue'))                        
                            print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                            amount = input(colored('To transfer money from savings -> checking account,\nplease enter the amount: ', 'green'))
                            transaction.transfer_between_accounts(amount, "savings", "checking")
            #------------------------------------------------------------#
            #              Transfer - To other account ID
            #------------------------------------------------------------#
                    elif options_E[accounts_menu3] == options_E[1]:  # to other account ID
                        print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                        print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue')) 
                        print(colored("Which account you want to transfer from?", 'light_blue')) 
                        options_G = ["Checking account", "Savings account"]
                        terminal_menu = TerminalMenu(options_G)
                        transferMenu = terminal_menu.show()
            #------------------------------------------------------------#
            #      Transfer - To other account ID - from checking acc
            #------------------------------------------------------------#                       
                        if options_G[transferMenu] == options_G[0]:  # checking account
                            print(colored(f"Balance of your checking account is = $ {customer_logged_account.balance_checking} $", 'light_blue'))
                            amount = input(colored('Please enter the amount: ', 'green'))
                            to_account_id = input(colored("Please enter the account ID of the recipient", 'green'))
                            transaction.transfer_to_other_user(amount, "checking", to_account_id)
            #------------------------------------------------------------#
            #      Transfer - To other account ID - from savings acc
            #------------------------------------------------------------#                       
                        if options_G[transferMenu] == options_G[1]:  # savings account
                            print(colored(f"Balance of your savings account is = $ {customer_logged_account.balance_savings} $", 'light_blue')) 
                            amount = input(colored('Please enter the amount: ', 'green'))
                            to_account_id = input(colored("Please enter the account ID of the recipient: ", 'green'))
                            transaction.transfer_to_other_user(amount, "savings", to_account_id)
            #------------------------------------------------------------#
            #                           Logout
            #------------------------------------------------------------#
                elif options_B[login_menu] == options_B[3]:  # logout
                    print(colored(f'''\n         🏦 Thank you for using ACME Bank 🏦\n                See you {customer_login_info[1]}!\n''', 'light_blue'))
                    break
        else:
            print(colored("\nSorry, invalid ID or password. Please try again.", "yellow"))

    elif options_A[menu_entry_index] == options_A[2]:  # exit
        print(colored(f'''\n                     🏦 Thank you for using ACME Bank 🏦''', 'light_blue'))
        return 
            
if __name__ == "__main__":
    main()
# if __name__ == "__main__":
#     test_transaction = Transactions(10001, True)  # Active account
#     test_transaction.transfer_to_other_user(10, "checking", 10002)