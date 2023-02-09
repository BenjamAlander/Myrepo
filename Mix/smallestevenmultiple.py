def smallestEvenMultiple(n):
        multiplier = 2
        while True:
            if multiplier % n == 0:
                return multiplier
                break
            else:
                multiplier += 2

smallestEvenMultiple(10)
        