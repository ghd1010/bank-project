import unittest
from main import Customer

class TestCustomer(unittest.TestCase):
    
    def setUp(self): # create a cart object
        self.test_customer = Customer('jake', 'paul','password123')
        self.test_customer.balance_checking = 150
        self.test_customer.balance_savings = 100

        self.test_customer_two = Customer('Haya', 'Almutairi','password432')

    def test_add_customer_to_csv(self):
        self.assertFalse(self.test_customer.add_customer_to_csv(), False)  # test a pre-existed customer

    def test_deposit(self):
        self.assertFalse(self.test_customer.balance_checking.deposit(50), 200) # deposit from savings
        self.assertFalse(self.test_customer.balance_savings.deposit(50), 150) # deposit from checking

    def test_withdraw(self):
            
            self.assertFalse(self.test_customer.balance_checking.withdraw(50), 150) # withdraw from savings
            self.assertFalse(self.test_customer.balance_savings.withdraw(50), 100) # withdraw from checking

            self.assertFalse(self.test_customer_two.balance_checking.withdraw(100), -35.0) # overdraft in checking
            self.assertFalse(self.test_customer_two.balance_savings.withdraw(100), -35.0) # overdraft in savings




if __name__ == '__main__':
    unittest.main(verbosity=2)

