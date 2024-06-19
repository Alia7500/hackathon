def F(s):
    ss = s
    n = 0

    while s < 85:
        s += 4
        n += 11
    if n == 242:
        print(ss)

for i in range(10000):
    F(i)