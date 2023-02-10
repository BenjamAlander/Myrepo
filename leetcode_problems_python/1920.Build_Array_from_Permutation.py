
def buildArray(nums):
    ans = [0] * len(nums) # ans prints [0,0,0,0,0,0], now the list is the right length
        
    for i in range(len(nums)): # this could be for i in nums: aswell
        ans[i] = nums[nums[i]] # in a list [0,2,1,5,3,4] list[2] would be the index, so number 1 at index [2]
    return ans                 # in a list [0,2,1,5,3,4] list[list[2]] refers to index of the value 2,  
                                                                           # in this case index 1

print(buildArray([0,2,1,5,3,4]))

"""
1920. Build Array from Permutation

Input: nums = [0,2,1,5,3,4]
Output: [0,1,2,4,5,3]
Explanation: The array ans is built as follows: 
ans = [nums[nums[0]], nums[nums[1]], nums[nums[2]], nums[nums[3]], nums[nums[4]], nums[nums[5]]]
    = [nums[0], nums[2], nums[1], nums[5], nums[3], nums[4]]
    = [0,1,2,4,5,3]

"""