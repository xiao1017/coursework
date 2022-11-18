
polygon_file_address='C:/Users/XIAOYU/Desktop/polygon.csv'
def read_file(polygon_file_address):
    with open(polygon_file_address) as f:
        data = f.read().splitlines()
    point_list_a=[]
    for row in data:
        point_list_a.append(row.split(','))
    return point_list_a

print(read_file(polygon_file_address))
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

point_file_address= 'C:/Users/XIAOYU/Desktop/input.csv'
def read_file(point_file_address):
    with open(point_file_address) as f:
        data = f.read().splitlines()
    point_list_b=[]
    for row in data:
        point_list_b.append(row.split(','))
    return point_list_b
print(read_file(point_file_address))



