def isPalindrome(x):
    if str(x)[::] == str(x)[::-1]:
        return True
    return False

ans = isPalindrome(505)
print(ans)
ans2 = isPalindrome(1254)
print(ans2)

"""
9. Palindrome Number

Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

"""