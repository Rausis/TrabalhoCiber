import threading as th
def A(n):

    while n > 1:
        n= n-1
        print(f"a{n}")

def B(n):

    while n > 1:
        n= n-1
        print(f"b{n}")
def C(n):

    while n > 1:
        n= n-1
        print(f"c{n}")
    

n = 10000
thread1 = th.Thread(target=A, args=[n])
thread2 = th.Thread(target=B, args=[n])
thread3 = th.Thread(target=C, args=[n])

thread1.start()
thread2.start()
thread3.start()