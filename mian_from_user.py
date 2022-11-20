
from plotter import Plotter


def read_file(file_address):
    with open(file_address) as f:
        data = f.read().splitlines()
    point_list = []
    for row in data:
        point_list.append(row.split(','))
    return point_list


class Line:
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


class Polygon:
    def __init__(self, points):
        self.__points = points
        lines = []
        for i in range(len(points)-2):
            line = Line(name=points[i+1][0]+'-'+points[i+2][0], x1=points[i+1][1],
                        y1=points[i+1][2], x2=points[i+2][1], y2=points[i+2][2])
            lines.append(line)
        self.__lines = lines

    def get_points(self):
        return self.__points

    def get_point(self, index):
        return self.__points[index]

    def get_lines(self):
        return self.__lines

    def get_line(self, index):
        return self.__lines[index]


def mbr_method(x, y, polygon):
    minx = float(polygon.get_point(1)[1])
    maxx = float(polygon.get_point(1)[1])
    miny = float(polygon.get_point(1)[2])
    maxy = float(polygon.get_point(1)[2])
    for point in polygon.get_points()[1:]:
        point = list(map(float, point))
        minx = min(minx, point[1])
        maxx = max(maxx, point[1])
        miny = min(miny, point[2])
        maxy = max(maxy, point[2])
    if x < minx or x > maxx or y < miny or y > maxy:      # 没用括号 判断点是否在区域外
        return True
    return False

# categorize point


def categorize_point(x, y, polygon):

    if mbr_method(x, y, polygon):  # true运行里面的东西，false就不运行了
        return "outside"
    for line in polygon.get_lines():
        if is_point_on_the_line(x, y, line):
            return "boundary"
    xr, yr = get_ray(x, y, polygon)
    count = 0
    for line in polygon.get_lines():
        if is_ray_cross_line(x, y, xr, yr, line):
            count = count+1
    if count % 2 == 1:
        return "inside"
    return "outside"


def get_ray(x, y, polygon):
    xr = 6
    yr = 5
    n = 1
    while n != 0:
        xr = xr + 1
        yr = yr + xr+1
        if int((x-xr) * 10) != 0 and int((y-yr) * 10) != 0:
            n = 0
            for point in polygon.get_points()[1:]:
                point = list(map(float, point))
                if round(((point[2]-y)*(xr-x)-(yr-y)*(point[1]-x))*100) == 0:
                    n = n + 1
    return xr, yr


def is_point_on_the_line(x, y, line):
    c = list(map(float, line.get_point()))
    if round(((x-c[0])*(c[3]-c[1])-(c[2]-c[0])*(y-c[1]))*1000) == 0\
        and ((min(c[0], c[2]) <= x and x <= max(c[0], c[2])) or -0.001 < (x - c[0]) < 0.001)\
        and ((min(c[1], c[3]) <= y and y <= max(c[1], c[3])) or -0.001 < (y - c[1]) < 0.001):
        return True
    return False


def is_ray_cross_line(xo, yo, xr, yr, line):
    c = list(map(float, line.get_point()))
    m1 = (yr-yo)/(xr-xo)
    b1 = -((yr-yo)/(xr-xo))*xo+yo
    if(c[2]-c[0]) == 0:
        xc = c[0]
        yc = m1*xc+b1
        if(is_point_on_the_line(xc, yc, line) and
            ((xc-xo)*(xr-xo) >= 0 and (yc-yo)*(yr-yo) >= 0)):
            return True
        return False
    m2 = (c[3]-c[1])/(c[2]-c[0])
    b2 = -((c[3]-c[1])/(c[2]-c[0]))*c[0]+c[1]
    if m1 == m2:
        return False
    xc = (b2-b1)/(m1-m2)
    yc = (b2*m1 - b1*m2)/(m1-m2)
    if is_point_on_the_line(xc, yc, line):
        if ((xc-xo)*(xr-xo)) >= 0 and ((yc-yo)*(yr-yo)) >= 0:
            return True
    return False


def check_number(x):
    if x.isdigit():  # 采用.isdigit()方法对内容做基本判断
        return True
    if x.count('.') == 1:
        left = x.split('.')[0]
        right = x.split('.')[1]
        if left.isdigit() and right.isdigit():
            return True
        if left.startswith('-') and left[1:].isdigit():
            return True
    return False


def main():
    plotter = Plotter()
    print('read polygon.csv')
    polygon_points = read_file("polygon.csv")
    polygon = Polygon(polygon_points)

    print('Insert point information')
    x = input('x coordinate: ')
    y = input('y coordinate: ')
    while not (check_number(x) and check_number(y)):
        print("The input character is invalid, please re-enter……")
        x = input('x coordinate: ')
        y = input('y coordinate: ')
    x = float(x)
    y = float(y)

    print('categorize point')
    categorize_output = categorize_point(float(x), float(y), polygon)

    print('plot polygon and point')
    xs = []
    ys = []
    for point in polygon_points[1:]:
        xs.append(float(point[1]))
        ys.append(float(point[2]))
    plotter.add_polygon(xs, ys)
    plotter.add_point(float(x), float(y), kind=categorize_output)
    if categorize_output != 'boundary':
        xr, yr = get_ray(x, y, polygon)
        plotter.add_ray(x, y, xr, yr)
    plotter.show()


if __name__ == '__main__':
    main()
