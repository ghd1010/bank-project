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
    fields = ['account_id', 'frst_name', 'last_name', 'password', 'balance_checking', 'balance_savings','num_of_overdrafts', 'is_active']  
    
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
    def create_customer_id(self):
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
            # check if customer already exists
            with open(my_csv_file, mode='r') as csvfile:
                content = csv.reader(csvfile)
                next(content)  # skip header
                
                for line in content:
                    if not self.first_name or not self.last_name:  # empty input check
                        print("Sorry, first name or last name is empty. Please enter a valid alphabetic input.")
                        return False
                    elif self.first_name.isdigit() or self.last_name.isdigit():  # numeric name check
                        print("Sorry, first name or last name should not be numbers.")
                        return False
                    elif len(line) > 2 and line[1].lower() == self.first_name.lower() and line[2].lower() == self.last_name.lower():
                        print(f"Sorry, customer with name ({self.first_name} {self.last_name}) already exists.")
                        return False

            # create a list to add the customer
            new_customer = [
                self.create_customer_id(),
                self.first_name,
                self.last_name,
                self.password,
                self.balance_checking,
                self.balance_savings,
                self.num_of_overdrafts,
                self.is_active
            ]

            # append the customer to the CSV file
            with open(my_csv_file, mode='a', newline='') as csvfile:  #newline='' to avoid extra blank lines
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
        
    def balance_checking_deposit(self, amount):
        if amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positivr non-zero number', 'yellow'))
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number', 'yellow'))
            return False
        else:
            self.balance_checking += amount
            return self.balance_checking
    
    def balance_savings_deposit(self, amount):
        if amount < 0:
            print(colored('Sorry, you can\'t deposit a negative number. Please ensure it is a positive non-zero number'), 'yellow')
            return False
        elif amount == 0:
            print(colored('Sorry, you can\'t deposit zero. Please ensure it is a positive non-zero number'), 'yellow')
            return False
        else:
            self.balance_savings += amount
            return self.balance_savings
    
    def balance_checking_withdraw(self):
        pass
    
    def balance_savings_withdraw(self):
        pass


def main():
    #MENU
    welcome_text = colored('''                         🏦 Welcome to ACME Bank 🏦''', 'green')
    question_text = colored('''                       What are you looking for today?''', 'light_blue')

    full_text = f"\n{welcome_text}\n{question_text}\n"

    print(full_text)

    options = ["Sign up", "Login"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    if options[menu_entry_index] == options[0]:
        customer_fname = input(colored('Please enter your first name: ' ,'green'))
        customer_lname = input(colored('Please enter your last name: ' ,'green'))
        customer_password= input(colored('Please enter your password: ' ,'green'))

        customer = Customer(customer_fname, customer_lname, customer_password)
        customer.add_customer_to_csv()

    elif options[menu_entry_index] == options[1]:
        customer_ID = input(colored('Please enter your ID: ' ,'green'))
        customer_password= input(colored('Please enter your password: ' ,'green'))
        
        # login process
        with open(my_csv_file, mode='r') as csvfile:
            content = csv.reader(csvfile)
            next(content)  # skip header
            for line in content:
                if line[0] == customer_ID and line[3] == customer_password:
                    print(colored(f'''\n                             Hello, {line[1]}!\n''', 'light_blue'))
                    
                    # after successful login, show account options
                    options2 = ["Withdraw", "Deposit", "Transfer"]
                    terminal_menu = TerminalMenu(options2)
                    login_menu = terminal_menu.show()

                    if options2[login_menu] == options2[0]: #for withdraw function
                        pass
                    elif options2[login_menu] == options2[1]: #for deposit function
                        pass
                    elif options2[login_menu] == options2[2]: #for transfer function
                        pass
                    break
            else:
                print(colored("\nSorry, invalid ID or password. Please try again.", "yellow"))


if __name__ == "__main__":
    main()