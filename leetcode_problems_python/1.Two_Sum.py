
def twoSum(nums, target):
    for i in nums:
        for j in range((i+1),len(nums)):
            if nums[j] + nums[i] == target:
                return [i,j]
                

ans = twoSum([1,2,3,6,7,2,10,2], 12)
print(ans)

"""
1. Two Sum

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

"""