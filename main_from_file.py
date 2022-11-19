
# 定义读取文件
def read_file(file_address):
    with open(file_address) as f:
        data = f.read().splitlines()
    point_list = []
    for row in data:
        point_list.append(row.split(','))
    return point_list

# 利用四个点建立line


class Line():
    def __init__(self, name, x1, x2, y1, y2):
        self.__name = name
        self.__x1 = float(x1)
        self.__x2 = float(x2)
        self.__y1 = float(y1)
        self.__y2 = float(y2)

    def get_name(self):
        return self.__name

    def get_point(self):
        return self.__x1, self.__x2, self.__y1, self.__y2


class Polygon():
    def __int__(self, points):
        self.points = points

    def get_points(self):
        return self.points

    def line(self):
        res = []
        points = self.get_points()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + '-' + point_b.get_name(), point_a, point_b))
            point_a = point_b
        res.append(Line(point_a.get_name() + '-' + points[0].get_name(), point_a, points[0]))
        return res














point_file_address = 'C:/Users/XIAOYU/Desktop/input.csv'


def read_file(point_file_address):
    with open(point_file_address) as f:
        data = f.read().splitlines()
    point_list_b = []
    for row in data:
        point_list_b.append(row.split(','))
    return point_list_b


print(read_file(point_file_address))





