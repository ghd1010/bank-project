# Writing data to CSV file, from: https://www.geeksforgeeks.org/reading-and-writing-csv-files-in-python/
import csv  
# name of csv file  
my_csv_file = "bank.csv"
# field names  
fields = ['account_id', 'frst_name', 'last_name', 'password', 'balance_checking', 'balance_savings']  

# data rows of csv file  
rows = [[10001, 'suresh', 'sigera', 'juagw362', 1000, 10000],  
        [10002, 'james', 'taylor', 'idh36%@#FGd', 10000, 10000],  
        [10003, 'melvin', 'gordon', 'uYWE732g4ga1', 2000, 20000],  
        [10004, 'stacey', 'abrams', 'DEU8_qw3y72$', 2000, 20000],  
        [10005, 'jake', 'paul', 'd^dg23g)@', 100000, 100000]]  

# writing to csv file  
with open(my_csv_file, mode ='w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows)

class Customer:

    new_id = 0
    
    def __init__(self, first_name, last_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

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
    def add_customer_to_csv(self, balance_checking=0, balance_savings=0):
        try:
            # check if the customer is already exist
            with open(my_csv_file, mode='r') as csvfile:
                content = csv.reader(csvfile)
                next(content)  # Skip header
                for line in content:
                    if line[1] == self.first_name and line[2] == self.last_name:
                        print(f"Sorry, customer with name ({self.first_name} {self.last_name}) is already exists.")
                        return 
                    
            # create list to add customer
            new_customer = [self.create_customer_id(), 
                            self.first_name,
                            self.last_name,
                            self.password,
                            balance_checking,
                            balance_savings]
            
            # add the customer
            with open(my_csv_file, mode='a') as csvfile:  # 'a' stands for append
                # creating a csv writer object  
                csvwriter = csv.writer(csvfile)  
                # writing the data row
                csvwriter.writerow(new_customer)
                
        except FileNotFoundError:
            print(f"Sorry, the csv file ({my_csv_file}) is not found. Please make sure you have the correct file.")
        

# just testing my function here
# customer = Customer('Ghada', 'Almutairi', 'GH124')
# customer.add_customer_to_csv()

# class Account:
#     def __init__(self, account_id, balance_checking, balance_savings):
#         self.account_id = account_id
#         self.balance_checking = balance_checking
#         self.balance_savings = balance_savings
