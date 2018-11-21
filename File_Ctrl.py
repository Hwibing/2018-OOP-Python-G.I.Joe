


f = open("./prices/price_read", 'r')
while True:
    line = f.readline()
    if not line: break
    print(line)
f.close()