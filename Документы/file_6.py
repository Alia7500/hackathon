ch = '4' * 106
while '444' in ch or '555' in ch:
    if '555' in ch:
        ch = ch.replace("555","4",1)
    else:
        ch = ch.replace("444", "5",1)
print(ch) # 44
