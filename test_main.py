import unittest
# from main import Customer
from main import Account


# class TestCustomer(unittest.TestCase):
    
#     def setUp(self): # create a customer object
#         self.test_customer_one = Customer('jake', 'paul','password123') # defining a pre-existed customer
#         self.test_customer_two = Customer('Stacey', 'Abrams','DEU8_qw3y72$') # case insensitive
#         self.test_customer_three = Customer('', '','') # empty
#         self.test_customer_four = Customer('11', '22','xxx123') # numbers 
#         self.test_customer_five = Customer('melvin', 'gordon','uYWE732g4ga1') 
#         self.test_customer_six = Customer('Haya', 'Almutairi','password432') 

#     def test_add_customer_to_csv(self):
#         self.assertEqual(self.test_customer_three.add_customer_to_csv(), False)  # test empty inputs
#         self.assertEqual(self.test_customer_four.add_customer_to_csv(), False)  # test first name, last name as numbers
#         self.assertEqual(self.test_customer_one.add_customer_to_csv(), False)  # test a pre-existed customer
#         self.assertEqual(self.test_customer_two.add_customer_to_csv(), False)  # test a pre-existed customer (case insensitive)
#         self.assertEqual(self.test_customer_six.add_customer_to_csv(), True)  # test adding a valid customer


class TestAccount(unittest.TestCase):
    
    def setUp(self): # create a account object
        self.test_account_one= Account(10003, 2000, 20000, 0, True)
        self.test_account_two = Account(10006, 0, 0, 1, True)  # num of overdrafts = 1
        self.test_account_three = Account(10002, -50, 500, 1, True)  # already negative balance
        # self.test_account_two= Account(10006, 0, 0, 0, True)

    def test_balance_checking_deposit(self):
        self.assertEqual(self.test_account_one.balance_checking_deposit('hello!'), False) # enter amount as a string
        self.assertEqual(self.test_account_one.balance_checking_deposit(-50), False) # deposit a negative number from checking account
        self.assertEqual(self.test_account_one.balance_checking_deposit(0), False) # deposit zero in checking account
        self.assertEqual(self.test_account_one.balance_checking_deposit(50), 2050) # deposit from checking account

#     def test_balance_savings_deposit(self):
#         self.assertEqual(self.test_account_one.balance_savings_deposit(50), 20050) # deposit from savings account
#         self.assertEqual(self.test_account_one.balance_savings_deposit(-50), False) # deposit a negative number from savings account
#         self.assertEqual(self.test_account_one.balance_savings_deposit(0), False) # deposit zero in savings account       

#     def test_balance_checking_withdraw(self):
#         self.assertEqual(self.test_account_one.balance_checking_withdraw(50), 1950) # withdraw from checking account
#         self.assertEqual(self.test_account_one.balance_checking_withdraw(-50), False) # withdraw a negative number from checking account
#         self.assertEqual(self.test_account_one.balance_checking_withdraw(0), False) # withdraw zero from checking account
        
#         self.assertEqual(self.test_account_two.balance_checking_withdraw(100), False) # overdraft in checking account
#         self.assertEqual(self.test_account_two.balance_checking_withdraw(40), -75) # deativate account
#         self.assertEqual(self.test_account_three.balance_checking_withdraw(150), False) # deativate account

#     def test_balance_savings_withdraw(self):
#         self.assertEqual(self.test_account_one.balance_savings_withdraw(100), 19900)  # withdraw from savings account
#         self.assertEqual(self.test_account_one.balance_savings_withdraw(-50), False) # withdraw a negative number from savings account
#         self.assertEqual(self.test_account_one.balance_savings_withdraw(0), False) # withdraw zero from savings account
#         self.assertEqual(self.test_account_one.balance_savings_withdraw(25000), False)  # withdraw more than what is in the balance
#         self.assertEqual(self.test_account_two.balance_savings_withdraw(50), -85) 




if __name__ == '__main__':
    unittest.main(verbosity=2)

