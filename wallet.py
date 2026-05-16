class Wallet:
   def __init__(self):
       self.__balance = 0 # Private (internal) attribute

   def __validate(self, amount):
       """Private (internal) function to check insternal balance atttibut

       Args:
           amount (float): Balance amount to be validated

       Raises:
           ValueError: If amount is negative
       """
       if amount < 0:
           raise ValueError('Amount must be positive')

   def deposit(self, amount):
       self.__validate(amount)
       self.__balance += amount

   def withdraw(self, amount):
       """Private (internal) function to withdraw funds from balance attribute

       Args:
           amount (float): Balance amount to be withdrawn

       Raises:
           ValueError: If amount is negative
       """
       self.__validate(amount)
       if amount > self.__balance:
           raise ValueError('Insufficient funds')
       self.__balance -= amount

   def get_balance(self):
       """Public function to access internal private attribute

       Returns:
           Float: The current balance
       """
       return self.__balance

acct_one = Wallet()
acct_one.deposit(3)
print(acct_one.get_balance()) # 3

acct_one.deposit(50)
print(acct_one.get_balance()) # 53

acct_one.deposit(-4)  # ValueError: Amount must be positive
acct_one.withdraw(-8) # ValueError: Amount must be positive
acct_one.withdraw(58) # ValueError: Insufficient funds