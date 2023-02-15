# Learn and comprehend these using python visualizer

def iterative_factorial(n): # Iteratiivisesti laskettu kertoma
    factorial = 1 
    for i in range(2, n + 1):
        factorial *= i
    return factorial
    
print("Iterative factorial is: ",iterative_factorial(5))

def recur_factorial(n): # Rekursiivisesti laskettu kertoma
    if n == 1:
        return n
    else:
        temp = recur_factorial(n-1)
        temp = temp * n
    return temp
    
print("Recursive factorial is: ",recur_factorial(5))

def permute(string, pocket=""): # Rekursiivisesti 
    if len(string) == 0:
        print(pocket)
    else:
        for i in range(len(string)):
            letter = string[i]
            front = string[0:i]
            back = string[i+1:]
            together = front + back
            permute(together, letter + pocket)
            
print(permute("ABCD"))
