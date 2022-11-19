
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
    def __init__(self, name, x1, y1, x2, y2):
        self.__name = name
        self.__x1 = float(x1)
        self.__y1 = float(y1)
        self.__x2 = float(x2)
        self.__y2 = float(y2)

    def get_name(self):
        return self.__name

    def get_point(self):
        return self.__x1, self.__y1, self.__x2, self.__y2

# 建立图形的class,并建立lines的list，第一行是名称 ，两个点组成一条线，用for循环-2,0行是id,因此选择point从1列开始


class Polygon():
    def __int__(self, points):
        self.__points = points
        lines = []
        for i in range(len(points)-2):
            line = Line(name=points[i+1][0]+'-'+points[i+2][0], x1=points[i+1][1],
                        y1=points[i+1][2], x2=points[i+2][1], y2=points[i+2][2])
            lines.append(line)
        self.__lines = lines

# 定义选取所有点

    def get_points(self):
        return self.__points

# 根据index得到特定的想要的点

    def get_point(self, index):
        return self._points[index]

# 定义选取所有line
    def get_lines(self):
        return self.__lines

# 根据index得到特定的想要的line

    def get_line(self, index):
        return self._lines[index]












point_file_address = 'C:/Users/XIAOYU/Desktop/input.csv'


def read_file(point_file_address):
    with open(point_file_address) as f:
        data = f.read().splitlines()
    point_list_b = []
    for row in data:
        point_list_b.append(row.split(','))
    return point_list_b


print(read_file(point_file_address))

