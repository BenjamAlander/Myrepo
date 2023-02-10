import numpy as np

def getConcatenation(nums):
    return np.array(nums+nums)

ans = getConcatenation([1,2,1])
print(ans)

"""
1929. Concatenation of Array

Input: nums = [1,2,1]
Output: [1,2,1,1,2,1] -> my return is a numpy array, not a regular list
Explanation: The array ans is formed as follows:
- ans = [nums[0],nums[1],nums[2],nums[0],nums[1],nums[2]]
- ans = [1,2,1,1,2,1]

"""