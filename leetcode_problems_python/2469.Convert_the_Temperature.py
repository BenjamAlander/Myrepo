import numpy as np

def convertTemperature(celsius):
    kelvin = celsius + 273.15
    fahrenheit = celsius * 1.80 + 32.00
    return np.array([kelvin,fahrenheit])

ans = convertTemperature(36.50)
print(ans)
    

"""
2469. Convert the Temperature

Input: celsius = 36.50
Output: [309.65000,97.70000]
Explanation: Temperature at 36.50 Celsius converted in Kelvin is 309.65 and converted in Fahrenheit is 97.70.

"""