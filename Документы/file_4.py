def F(n):
    ms = bin(n)[2:]

    if n % 2 == 0:
        ms = '10'+ms
    if n % 2 != 0:
        ms = '1' + ms + '01'
    return int(ms,2)

for x in range(1,400):
    result = F(x)

    if result > 441:
        print(x)
