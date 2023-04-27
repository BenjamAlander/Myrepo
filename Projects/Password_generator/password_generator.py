import random
import string

class Pw_generator:
    def __init__(self):
        pass
    def generate_password(self,length, complexity):
        password = ""
        characters = ""
        if complexity == 1:
            characters = string.ascii_letters
        elif complexity == 2:
            characters = string.ascii_letters + string.digits
        elif complexity == 3:
            characters = string.ascii_letters + string.digits + string.punctuation
        for i in range(length):
            password += random.choice(characters)
        return password

    def query_user(self):
        options = [1,2,3]
        print("Welcome to the password generator!")
        length = int(input("Enter desired password length: "))
        complexity = int(input("Enter desired password complexity (weak, medium, strong) choose (1, 2, 3): "))
        if complexity in options:
            pw = self.generate_password(length, complexity)
            print("Here is a generated password: " + pw)
        elif complexity not in options:
            print("Try again, please choose number 1 for weak, number 2 for medium or number 3 for strong.")
        return length, complexity

    def main(self):
        self.query_user()

    if __name__ == "__main__":
        main()

