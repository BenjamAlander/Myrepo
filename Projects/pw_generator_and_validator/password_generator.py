import random
import string

def generate_password(length, complexity):
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
options = [1,2,3]
length = int(input("Enter desired password length: "))
complexity = int(input("Enter desired password complexity (weak, medium, strong) choose (1, 2, 3): "))
if complexity in options:
    password = generate_password(length, complexity)
    print("Generated password: ", password)
    
elif complexity not in options:
    print("Try again, please choose number 1 for weak, number 2 for medium or number 3 for strong.")
