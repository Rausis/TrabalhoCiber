import threading as th
def A(n):
    n =10 
    while n > 1:
        n= n-1
        print(f"a{n}")

def B(n):
    n =10 
    while n > 1:
        n= n-1
        print(f"b{n}")
def C(n):
    n =10 
    while n > 1:
        n= n-1
        print(f"c{n}")
    

n = 100
thread1 = th.Thread(target=A, args=[n])
thread2 = th.Thread(target=B, args=[n])
thread3 = th.Thread(target=C, args=[n])

thread1.start()
thread2.start()
thread3.start()