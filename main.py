from collections import UserDict
import re

# Phone nr validation exception
class PhoneValidationError(Exception):
    pass

# Base class
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
# Contact name class
class Name(Field):
		pass

# Phone nr class
class Phone(Field):
    def __init__(self, value):
        self._validate(value)
        super().__init__(value)

    def _validate(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise PhoneValidationError          # Exception to handle in following implementation


# One contact record: name, phone nr list.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # Add Phone instance into phones list
    def add_phone(self, phone):
        phone_to_add = Phone(phone)   # Validate + add
        self.phones.append(phone_to_add)

    # Remove phone by value
    def remove_phone(self, phone):
        self.phones = [phone_nr for phone_nr in self.phones if phone_nr.value != phone]

    # Update phone nr with a new value
    def edit_phone(self, old_value, new_value):
        for i, p in enumerate(self.phones):
            if p.value == old_value:
                self.phones[i] = Phone(new_value)
                return True
        return False  # Can use in future True/False value to confirm if phone nr was updated or not found.

    # Search for a phone nr
    def find_phone(self, phone):
        for phone_nr in self.phones:
            if phone_nr.value == phone:
                return phone_nr
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


# AddressBook (Map for Records)
class AddressBook(UserDict):
    
    # Add record by contact name
    def add_record(self, record):
        self.data[record.name.value] = record

    # Find Record by name
    def find(self, name):
        return self.data.get(name)

    # Delete Record by name
    def delete(self, name):
        if name in self.data:
            del self.data[name]

# TEST            

#Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

 # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

 # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

#Створення адресної книги після видалення
for name, record in book.data.items():
    print(record)