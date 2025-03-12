import unittest
from main import Customer, Account, Transactions

class TestCustomer(unittest.TestCase):
    
    def setUp(self): # create a customer object
        self.test_customer_one = Customer('jake', 'paul','password123') # defining a pre-existed customer
        self.test_customer_two = Customer('Stacey', 'Abrams','DEU8_qw3y72$') # case insensitive
        self.test_customer_three = Customer('', '','') # empty
        self.test_customer_four = Customer('11', '22','xxx123') # numbers 
        self.test_customer_five = Customer('melvin', 'gordon','uYWE732g4ga1') 
        self.test_customer_six = Customer('Haya', 'Almutairi','password432') 

    def test_add_customer_to_csv(self):
        self.assertEqual(self.test_customer_three.add_customer_to_csv(), False)  # test empty inputs
        self.assertEqual(self.test_customer_four.add_customer_to_csv(), False)  # test first name, last name as numbers
        self.assertEqual(self.test_customer_one.add_customer_to_csv(), False)  # test a pre-existed customer
        self.assertEqual(self.test_customer_two.add_customer_to_csv(), False)  # test a pre-existed customer (case insensitive)
        self.assertEqual(self.test_customer_six.add_customer_to_csv(), True)  # test adding a valid customer


class TestDeposit(unittest.TestCase):
    
    def setUp(self): # create a account object
        self.test_account_one= Account(10003, 2000, 20000, 0, True)
        self.test_account_two = Account(10006, 0, 0, 1, True)  # num of overdrafts = 1
        self.test_account_three = Account(10002, -50, 500, 1, True)  # already negative balance

    def test_balance_checking_deposit(self):
        self.assertEqual(self.test_account_one.balance_checking_deposit('hello!'), False) # enter amount as a string
        self.assertEqual(self.test_account_one.balance_checking_deposit(-50), False) # deposit a negative number
        self.assertEqual(self.test_account_one.balance_checking_deposit(0), False) # deposit zero 
        self.assertEqual(self.test_account_one.balance_checking_deposit(50), 2050) # deposit : success

    def test_balance_savings_deposit(self):
        self.assertEqual(self.test_account_one.balance_savings_deposit('100'), False) # enter amount as a string
        self.assertEqual(self.test_account_one.balance_savings_deposit(-50), False) # deposit a negative number
        self.assertEqual(self.test_account_one.balance_savings_deposit(0), False) # deposit zero    
        self.assertEqual(self.test_account_one.balance_savings_deposit(50), 20050) #  deposit : success

class TestWithdraw(unittest.TestCase):
    
    def setUp(self):  
            self.test_account_one = Account(10001, 1000, 10000, 0, True) 
            self.test_account_two = Account(10006, 0, 0, 1, True)  # num of overdrafts = 1
            self.test_account_three = Account(10002, -50, 500, 1, True)  # already negative balance in checking

    def test_balance_checking_withdraw(self):
        self.assertEqual(self.test_account_one.balance_checking_withdraw('hello!'), False)  # enter amount as a string
        self.assertEqual(self.test_account_one.balance_checking_withdraw(-50), False)  # withdraw a negative number 
        self.assertEqual(self.test_account_one.balance_checking_withdraw(0), False)  # withdraw zero   
        self.assertEqual(self.test_account_one.balance_checking_withdraw(50), 950)  # withdraw : success

    def test_balance_checking_withdraw_with_overdraft(self):
            self.assertEqual(self.test_account_two.balance_checking_withdraw(40), -75)  
            self.assertEqual(self.test_account_two.balance_checking_withdraw(100), False)  

    def test_balance_saving_withdraw(self):
        self.assertEqual(self.test_account_one.balance_checking_withdraw('100!'), False)  # enter amount as a string
        self.assertEqual(self.test_account_one.balance_checking_withdraw(-50), False)  # withdraw a negative number 
        self.assertEqual(self.test_account_one.balance_checking_withdraw(0), False)  # withdraw zero   
        self.assertEqual(self.test_account_one.balance_savings_withdraw(25000), False)  # withdraw > balance
        self.assertEqual(self.test_account_two.balance_savings_withdraw(50), -85) # withdraw : success

    def test_balance_checking_withdraw_negative_balance(self):
        self.assertEqual(self.test_account_three.balance_checking_withdraw(10), -95)  # balance updated
        self.assertEqual(self.test_account_three.balance_checking_withdraw(100), False)  
    
class TestTransactions(unittest.TestCase):
    def setUp(self): # create a account object

        self.test_account_one= Transactions(10001, True)
        self.test_account_two= Transactions(10006, False)
        self.test_account_three= Transactions(10005, True)
        self.test_account_four= Transactions(10004, True)


    def test_transfer_between_my_accounts(self):
        self.assertEqual(self.test_account_one.transfer_between_accounts(200, "checking", "savings"), True)  # success
        self.assertEqual(self.test_account_two.transfer_between_accounts(-10, "checking", "savings"), False)  # negative amount
        self.assertEqual(self.test_account_two.transfer_between_accounts(10, "xxxx", "yyy"), False)  # different from (checking/savings)
        self.assertEqual(self.test_account_two.transfer_between_accounts(200, "checking", "savings"), False)  # transfer for inactive account
        self.assertEqual(self.test_account_three.transfer_between_accounts("200", "checking", "savings"), True)  # take amount as string (number)
        self.assertEqual(self.test_account_three.transfer_between_accounts("Hello", "checking", "savings"), False)  # take amount as string (letters)
        self.assertEqual(self.test_account_four.transfer_between_accounts(3000, "checking", "savings"), False)  # amount > balance
        self.assertEqual(self.test_account_four.transfer_between_accounts(10, "savings", "checking"), True)  # from savings to checking

    def test_transfer_to_other_user(self):
        self.assertEqual(self.test_account_one.transfer_to_other_user(300, "checking", 10005), True)  # success
        self.assertEqual(self.test_account_one.transfer_to_other_user("1", "checking", 10005), True)  # amount as string (number)
        self.assertEqual(self.test_account_one.transfer_to_other_user("Hello", "checking", 10005), False)  # amount as string (letters)
        self.assertEqual(self.test_account_one.transfer_to_other_user(-10, "checking", 10005), False)  # negative amount
        self.assertEqual(self.test_account_one.transfer_to_other_user(10, "xxxx", 10005), False)  # different from (checking/savings)
        self.assertEqual(self.test_account_two.transfer_to_other_user(10, "checking", 10005), False)  # transfer form inactive account
        self.assertEqual(self.test_account_four.transfer_to_other_user(2000, "checking", 10005), False)  # amount > balance
        self.assertEqual(self.test_account_three.transfer_to_other_user(10, "checking", 10006), False)  # transfer to an inactive account
        self.assertEqual(self.test_account_three.transfer_to_other_user(10, "checking", 121), False)  # beneficiary account is not in csv file
        self.assertEqual(self.test_account_three.transfer_to_other_user(10, "checking", 121), False)  # beneficiary account is not in csv file





if __name__ == '__main__':
    unittest.main(verbosity=2)

