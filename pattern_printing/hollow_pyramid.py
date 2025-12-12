n = 5
for i in range(1,n+1):
    if i == n:
        print("* "*n, sep="")
    else:
        print(" "*(n-i),"*"," "*(i-1)," "*(i-2), ("*" if i>1 else ""), sep="")