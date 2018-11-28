newstype=int(input())
f = open("./news", 'r', encoding='UTF-8')
while True:
    newline = f.readline()
    if not newline:
