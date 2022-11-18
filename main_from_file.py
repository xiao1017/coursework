
file_address='C:/Users/XIAOYU/Desktop/polygon.csv'
def read_file(file_address):
    with open(file_address) as f:
        data = f.read().splitlines()
    point_list=[]
    for row in data:
        point_list.append(row.split(','))
    return point_list

print(read_file(file_address))
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



