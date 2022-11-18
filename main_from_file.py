polygon_file_address = 'C:/Users/XIAOYU/Desktop/polygon.csv'


def read_file(polygon_file_address):
    with open(polygon_file_address) as f:
        data = f.read().splitlines()
    point_list_a = []
    for row in data:
        point_list_a.append(row.split(','))
    return point_list_a


print(read_file(polygon_file_address))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def get_point_1(self):
        return self.point_1

    def get_point2(self):
        return self.point_2


class Polygon:
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
