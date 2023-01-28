def encrypt(s:str):
    encrypted = ""
    for i in range(len(s)):
        char = s[i]
        if char.isalpha() and char.islower():
            char = chr((ord(char) - ord('a') + i + 1) % 26 + ord('a'))
        encrypted += char
    return encrypted


if __name__ == "__main__":
    print(encrypt("abc")) # bdf
    print(encrypt("xz")) # yb
    print(encrypt("kkkkkkkk")) # lmnopqrs
    print(encrypt("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")) # bcdefghijklmnopqrstuvwxyzabcde