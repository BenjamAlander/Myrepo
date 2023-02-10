def smallestEvenMultiple(n):
        multiplier = 2
        while True:
            if multiplier % n == 0:
                return multiplier
            else:
                multiplier += 2

ans = smallestEvenMultiple(5)
print(ans)

"""
2413. Smallest Even Multiple

Input: n = 5
Output: 10
Explanation: The smallest multiple of both 5 and 2 is 10.

"""