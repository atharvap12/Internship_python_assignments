def lengthOfLIS(nums: list[int]) -> int:

        #Here lis = [] is the list in which lis[i] contains the length of the Longest Increasing Subsequence(LIS) which ends at nums[i].
        #In essesnce, lis[i] is the length of LIS till nums[i].

        lis = [1] * len(nums) #Min. length of Longest Increasing Subsequence(LIS) till 'i'th index will always be 1.
        max_l = 0
        for i in range(len(nums)):
            for prev in range(i):
                if (nums[i] > nums[prev] and lis[prev] + 1 > lis[i]): #we check if nums[prev] is smaller than current element i.e nums[i].
                    #if yes, we can include it in our Increasing Subsequence. And if we include it, nums[prev] along with nums[i] will form an
                    # increasing subsequence. So length of LIS till 'i'th index(lis[i]) will be updated only if length of LIS till 'prev' index 
                    # + 1 (lis[prev] + 1) becomes greater than length of LIS till 'i'th index(lis[i])
                    lis[i] = 1 + lis[prev]

            max_l = max(max_l, lis[i])
        
        return max_l

somelist = [5, 4, 11, 1, 16, 8]
print(lengthOfLIS(somelist))