class Solution(object):
    def smallerNumbersThanCurrent(self, nums):
        sortedlist = sorted(nums)
        return [sortedlist.index(num) for num in nums]

        