class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    # Customizing python custom methods
    def __len__(self):
        return self.pages
    
    def __str__(self):
        return f"'{self.title}' has {self.pages} pages"
    
    def __eq__(self, value):
        return self.pages == value.pages
    
book1 = Book("Built Wealth Like a Boss", 420)
book2 = Book("Be Your Own Start", 420)
book3 = Book("The Millionaire Fastlane", 500)

print(len(book1)) # 420
print(len(book2)) # 420
print(str(book1)) # 'Built Wealth Like a Boss' has 420 pages
print(str(book2)) # 'Be Your Own Start' has 420 pages
print(book1 == book2) # True
print(book1 == book3) # False