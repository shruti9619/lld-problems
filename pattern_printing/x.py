n = 10
for i in range(0, n):
    for j in range(0, n):
        if i + j == n-1 or i == j:
            print("*", end="", sep="")
        else:
            print(" ", end="", sep="")
    print('\n')
        
