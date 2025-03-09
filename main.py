import csv  

# from: https://www.geeksforgeeks.org/reading-and-writing-csv-files-in-python/
# field names  
fields = ['account_id', 'frst_name', 'last_name', 'password', 'balance_checking', 'balance_savings']  
    
# data rows of csv file  
rows = [ [10001, 'suresh', 'sigera', 'juagw362', 1000, 10000],  
        [10002, 'james', 'taylor', 'idh36%@#FGd', 10000, 10000],  
        [10003, 'melvin', 'gordon', 'uYWE732g4ga1', 2000, 20000],  
        [10004, 'stacey', 'abrams', 'DEU8_qw3y72$', 2000, 20000],  
        [10005, 'jake', 'paul', 'd^dg23g)@', 100000, 100000]]  
    
# name of csv file  
filename = "bank.csv"
    
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows)

    