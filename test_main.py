import unittest
from main import Customer

class TestCustomer(unittest.TestCase):
    
    def setUp(self): # create a cart object
        self.test_customer_one = Customer('jake', 'paul','password123') # defining a pre-existed customer
        self.test_customer_one.balance_checking = 150
        self.test_customer_one.balance_savings = 100
        self.test_customer_two = Customer('Stacey', 'Abrams','DEU8_qw3y72$') # case insensitive
        self.test_customer_three = Customer('', '','') # empty
        self.test_customer_four = Customer('11', '22','xxx123') # numbers 
        self.test_customer_five = Customer('Haya', 'Almutairi','password432') # customer with 0 checking and saving balance


    def test_add_customer_to_csv(self):
        self.assertFalse(self.test_customer_one.add_customer_to_csv(), False)  # test a pre-existed customer
        self.assertFalse(self.test_customer_two.add_customer_to_csv(), False)  # test a pre-existed customer (case insensitive)
        self.assertFalse(self.test_customer_three.add_customer_to_csv(), False)  # test empty inputs
        self.assertFalse(self.test_customer_four.add_customer_to_csv(), False)  # test first name, last name as numbers

    def test_deposit(self):
        self.assertFalse(self.test_customer_one.balance_checking.deposit(50), 200) # deposit from savings
        self.assertFalse(self.test_customer_one.balance_savings.deposit(50), 150) # deposit from checking
        self.assertFalse(self.test_customer_one.balance_checking.deposit(-50), False) # deposit a negative number
        self.assertFalse(self.test_customer_one.balance_checking.deposit(0), False) # deposit zero

    def test_withdraw(self):
            
            self.assertFalse(self.test_customer_one.balance_checking.withdraw(50), 150) # withdraw from savings
            self.assertFalse(self.test_customer_one.balance_savings.withdraw(50), 100) # withdraw from checking
            self.assertFalse(self.test_customer_one.balance_savings.withdraw(-50), 100) # withdraw a negative number
            self.assertFalse(self.test_customer_one.balance_savings.withdraw(0), 100) # withdraw zero

            self.assertFalse(self.test_customer_three.balance_checking.withdraw(100), -35.0) # overdraft in checking
            self.assertFalse(self.test_customer_three.balance_savings.withdraw(100), -35.0) # overdraft in savings




if __name__ == '__main__':
    unittest.main(verbosity=2)

