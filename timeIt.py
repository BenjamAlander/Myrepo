import time
def primeCount(n):
    count = 0
    for i in range(2, n+1):
        prime = True
        for j in range(2, i-1):
            if i%j == 0:
                prime = False
                break
    if prime:
        count += 1
        print(count)

def timeIt(n):
    start = time.time()
    primeCount(n)
    stop = time.time()
    return f'For {n} it took {stop-start} seconds'



print(timeIt(100))
print(timeIt(1000))
print(timeIt(10_000))
print(timeIt(100_000))