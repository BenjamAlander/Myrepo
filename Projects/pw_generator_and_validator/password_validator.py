# Python password validator
"""
Requirements
1. Must be 12-30 characters long
2. Must have a number in it
3. Must have a special character in it
"""

password = "Iceman1337!234"
pass_length = 0
has_number = False
special_characters = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
special_char_checker = False

    
while pass_length is not len(password):
    current_char = password[pass_length]
    pass_length += 1
    if current_char.isdigit():
        contains_num = True
    if current_char in special_characters:
        special_char_checker = True
            
if pass_length > 12 and pass_length < 30 and contains_num  is True and special_char_checker is True:
    print("Valid password!")
else:
    print("Invalid password")


