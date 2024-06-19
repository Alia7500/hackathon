def F(n):
    bins = bin(n).replace("0b","")
    sums = bins.count("1")
    bins += str(sums%2)
    sums = bins.count("1")
    bins += str(sums%2)
    return bins
for i in range(300):
    valss = int(F(i),2)

    if valss > 126:
        print(valss)