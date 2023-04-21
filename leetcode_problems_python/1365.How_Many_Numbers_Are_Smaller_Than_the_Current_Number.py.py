def smallerNumbersThanCurrent(nums):
    sortedlist = sorted(nums)
    return [sortedlist.index(num) for num in nums]

ans = smallerNumbersThanCurrent([8,1,2,2,3])
print(ans)

"""
1365. How Many Numbers Are Smaller Than the Current Number

Input: nums = [8,1,2,2,3]
Output: [4,0,1,1,3]
Explanation: 
For nums[0]=8 there exist four smaller numbers than it (1, 2, 2 and 3). 
For nums[1]=1 does not exist any smaller number than it.
For nums[2]=2 there exist one smaller number than it (1). 
For nums[3]=2 there exist one smaller number than it (1). 
For nums[4]=3 there exist three smaller numbers than it (1, 2 and 2).

"""



