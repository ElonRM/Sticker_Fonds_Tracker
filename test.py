def f(a,b):
    if a == 0:
        return b+1
    elif b == 0:
        return f(a-1,1)
    else:
        return f(a-1,f(a,b-1))

#print(f(0,2))

def f2(a,b,c==0):
    if c==0:
        return a+b
    elif b==0:
        return 0 if c-1 ==0 else 1 if c-1==1 else a if c-1>0