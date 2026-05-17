from abc import ABC, abstractmethod

# In this example:

# We are importing the ABC class and abstractmethod from the abc module.
# We then create an Animal class that inherits from ABC, and create an abstract method make_sound in it that each subclass of Animal must override.
# We create the concrete classes Dog, Cat, and Monkey, which must override the make_sound abstract method.
# We instantiate the concrete classes and call their make_sound method to show how each of them implements the make_sound abstract method in its own way.

class Animal(ABC): # Inherits from abstract base class
   @abstractmethod # Abstract method decorator
   def make_sound(self):  # The method subclasses must override
       pass

# Concrete class that will override the abstract method
class Dog(Animal):
   def make_sound(self):
       print('Woof!')

# Another concrete class that will override the abstract method
class Cat(Animal):
   def make_sound(self):
       print('Meow!')

# Another concrete class that will override the abstract method
class Monkey(Animal):
   def make_sound(self):
       print('Ooh ooh aah aah!')

# Create instances of each concrete class
animals = [Dog(), Cat(), Monkey()]

# Loop through the instances to call the make_sound method
for animal in animals:
   animal.make_sound()

# Output:
# Woof!
# Meow!
# Ooh ooh aah aah!