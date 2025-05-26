from devtools import debug


class TryStuff():

    def __init__(self):
        self.name = "TryStuff"
        self.value = 0

    def scalling():   
        line = "x"
        for i in range(10):
            for j in range(i):
                line += " Y "                
                print(line)
            print(line + " Z ")




class SmallClient():
    def __init__(self):
        self.name = "SmallClient"
        self.value = 0
        self.phone_book: dict = {}


    def add_contact(self):

        userinputname: str = input("enter a name: ")
        userinputnumber: str = input("enter a number: ")
        print ("contact added!")
        self.phone_book[userinputname] = userinputnumber
        debug(self.phone_book)

    def remove_contact(self, userinputremove: str):
        if userinputremove in self.phone_book:
            del self.phone_book[userinputremove]
            print("contact removed!")
        else:
            print("contact not found!")

    def search_contact(self, userinputsearch: str):
        if userinputsearch in self.phone_book:
            print(f"contact found: {userinputsearch}: {self.phone_book[userinputsearch]}")
        else:
            print("contact not found!")
        


    def clientloop(self):
        while True:
            print("Welcome to the address book manager, what you want to do?")
            print("1. Add a contact")
            print("2. Remove a contact")
            print("3. Search for a contact")
            print("4. List all contacts")
            print("5. Exit")
            userinput: str = input("Enter your choice: ")
            if userinput == "1":
                self.add_contact()
            elif userinput == "2":
                userinputremovename: str = input("selected the name of the contact to remove:  ")
                self.remove_contact(userinputremovename)

            elif userinput == "3":
                userinputsearch: str = input("selected the name of the contact to search:  ")
                self.search_contact(userinputsearch)
            elif userinput == "4":
                print("list contacts")
                for name, number in self.phone_book.items():
                    print(f"{name}: {number}")
            else:
                print("invalid input")

client = SmallClient()
client.clientloop()