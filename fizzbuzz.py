import numpy as np
class Solution(object):
    def fizzBuzz(self, n):
        fizzBuzzArr = np.array([])
        for i in range(1,(n+1)):
            if (i % 3 == 0) and (i % 5 == 0):
                fizzBuzzArr = np.append(fizzBuzzArr, "FizzBuzz")
            elif (i % 3 == 0):
                fizzBuzzArr = np.append(fizzBuzzArr, "Fizz")
            elif (i % 5 == 0):
                fizzBuzzArr = np.append(fizzBuzzArr, "Buzz")
            else:
                fizzBuzzArr = np.append(fizzBuzzArr, str(i)) 
        return fizzBuzzArr       

# My fizzbuzz with numpy