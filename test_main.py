import unittest
from main import Customer

class TestCustomer(unittest.TestCase):
    
    def setUp(self): # create a customer object
        self.test_customer_one = Customer('jake', 'paul','password123') # defining a pre-existed customer
        self.test_customer_two = Customer('Stacey', 'Abrams','DEU8_qw3y72$') # case insensitive
        self.test_customer_three = Customer('', '','') # empty
        self.test_customer_four = Customer('11', '22','xxx123') # numbers 
        self.test_customer_five = Customer('melvin', 'gordon','uYWE732g4ga1') 
        self.test_customer_five.balance_checking = 150
        self.test_customer_five.balance_savings = 100
        self.test_customer_six = Customer('Haya', 'Almutairi','password432') # customer with 0 checking and savings balance


    def test_add_customer_to_csv(self):
        self.assertEqual(self.test_customer_one.add_customer_to_csv(), False)  # test a pre-existed customer
        self.assertEqual(self.test_customer_two.add_customer_to_csv(), False)  # test a pre-existed customer (case insensitive)
        self.assertEqual(self.test_customer_three.add_customer_to_csv(), False)  # test empty inputs
        self.assertEqual(self.test_customer_four.add_customer_to_csv(), False)  # test first name, last name as numbers

# class TestAccount(unittest.TestCase):
    
#     def setUp(self): # create a account object
#         self.test_account_one = Account(account_id, balance_checking, balance_savings, num_of_overdrafts, is_active

#     def test_balance_checking_deposit(self):
#         self.assertEqual(self.test_customer_five.balance_checking_deposit(50), 200) # deposit from checking account
#         self.assertEqual(self.test_customer_five.balance_checking_deposit(-50), False) # deposit a negative number from checking account
#         self.assertEqual(self.test_customer_five.balance_checking_deposit(0), False) # deposit zero in checking account

#     def test_balance_savings_deposit(self):
#         self.assertEqual(self.test_customer_five.balance_savings_deposit(50), 200) # deposit from savings account
#         self.assertEqual(self.test_customer_five.balance_savings_deposit(-50), False) # deposit a negative number from savings account
#         self.assertEqual(self.test_customer_five.balance_savings_deposit(0), False) # deposit zero in savings account       

#     def test_balance_checking_withdraw(self):
#         self.assertEqual(self.test_customer_five.balance_checking_withdraw(50), 150) # withdraw from checking account
#         self.assertEqual(self.test_customer_five.balance_checking_withdraw(-50), False) # withdraw a negative number from checking account
#         self.assertEqual(self.test_customer_five.balance_checking_withdraw(0), False) # withdraw zero from checking account
#         self.assertEqual(self.test_customer_six.balance_checking_withdraw(100), -35.0) # overdraft in checking account


#     def test_balance_savings_withdraw(self):
#         self.assertEqual(self.test_customer_five.balance_savings_withdraw(50), 150) # withdraw from savings account
#         self.assertEqual(self.test_customer_five.balance_savings_withdraw(-50), False) # withdraw a negative number from savings account
#         self.assertEqual(self.test_customer_five.balance_savings_withdraw(0), False) # withdraw zero from savings account
#         self.assertEqual(self.test_customer_six.balance_savings_withdraw(100), -35.0) # overdraft in savings account



if __name__ == '__main__':
    unittest.main(verbosity=2)

