with open('C:/Users/XIAOYU/Desktop/polygon.csv') as f:
    data = f.read().splitlines()
for row in data:
    print(row.split(','))
