
# Python password validator
**Requirements**:
1. Must be 12-30 characters long
2. Must have a number in it
3. Must have a special character in it

**The solution**:
1. Input the password we need to validate
2. To keep track of the length of the password, make a variable
3. Make sure it has a number with variable initially set to False
4. Has the entire password been searched? If not, go to step 5. If so go to step 9.
5. Iterate to next character in password
6. Increase value of pass length variable by 1
7. Is the current character a number? If not, go straight back to step 4 and continue to iterate over the entire password. If so, set the contains_number variable to True and then go back to step 4.
8. Is the current character a special character? If not, go straight back to step 4 and continue to iterate over the entire password. If so, set the contains_number variable to True and then go back to step 4.
9. Is the pass_length greater than 8 and is contain_number equal to True? If not, then the password is invalid. If so, then the password is valid!
![](https://gitlab.dclabra.fi/wiki/uploads/upload_355010544af7c0e529e7bcdc25a426df.png)

**PSEUDOCODE:**
define password
create a pass_length variable and set it to 0
create a contains_number variable and set it to False
if the entire password hasn't been searched:
  iterate to the next character of the password
  increment the pass_length variable
  if the current character of the password contains number:
    set contains_number to True
if pass_length is greater than 8 and if contain_number is equal to True:
  valid password
otherwise:
  invalid password
 
**The final code:**

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


