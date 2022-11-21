from plotter import Plotter


# define read file from file_address 定义读取文件
def read_file(file_address):
    with open(file_address) as f:
        data = f.read().splitlines()
    point_list = []  # creat point list
    for row in data:
        point_list.append(row.split(','))
    return point_list


# 创建line的class,利用(x1,y1),(x2,y2）表示线// Create a line class, use (x1, y1), (x2, y2) to represent the line
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


# Create a polygon class //建立图形的class,并建立lines的list，第一行是名称 ，两个点组成一条线，用for循环-2,0行是id,因此选择point从1列开始
class Polygon:
    def __init__(self, points):
        self.__points = points  # 数据类型是[[id,x,y],[str,str,str],...]
        lines = []
        # 根据pointlist 创建line list 0 row is header row, two points from a line, thus -2// 由于第一行是标题行，两个点连成一条线，所以用-2
        for i in range(len(points)-2):
            line = Line(name=points[i+1][0]+'-'+points[i+2][0], x1=points[i+1][1],
                        y1=points[i+1][2], x2=points[i+2][1], y2=points[i+2][2])
            lines.append(line)
        self.__lines = lines

    def get_points(self):
        return self.__points

# 根据index得到特定的想要的点 Define to get a specific point according to index
    def get_point(self, index):
        return self.__points[index]

    def get_lines(self):
        return self.__lines

# 根据index得到特定的想要的line Define to get a specific line according to index
    def get_line(self, index):
        return self.__lines[index]


# Define MBR method (用for循环语句，比较出x的最大最小值，比较出y的最大最小值 在pdf里面解释）
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
    if x < minx or x > maxx or y < miny or y > maxy:  # Determine whether the point is outside the //graph //判断点是否在矩形外部
        return True
    return False


# Get a ray that does not pass through the vertices of the graph 定义一条不穿过顶点的射线
def get_ray(x, y, polygon):
    xr = 6  # 设定一个初始点，如果两点组成的射线穿过任意一个顶点，就重新选取新的点组成射线
    yr = 5
    n = 1
    while n != 0:
        xr = xr + 1  # 获得新的点
        yr = yr + xr+1
        if int((x-xr) * 1000) != 0 and int((y-yr) * 1000) != 0:  # 避免选取的射线浮点和原浮点重合, 因为选取的是浮点，利用*100表示点的精准度
            n = 0
            for point in polygon.get_points()[1:]:  #判断多少个点重合
                point = list(map(float, point))  # 数据类型转变为float
                if round(((point[2]-y)*(xr-x)-(yr-y)*(point[1]-x))*1000) == 0:
                    n = n + 1
    return xr, yr


# 判断点是否在线端上 浮点数：*1000表示精准性
def is_point_on_the_line(x, y, line):
    c = list(map(float, line.get_point()))
    # 一。判断是否三点一线，二；判断点是否在线段所组成的矩形中，
    if round(((x-c[0])*(c[3]-c[1])-(c[2]-c[0])*(y-c[1]))*1000) == 0\
        and ((min(c[0], c[2]) <= x and x <= max(c[0], c[2])) or -0.001 < (x - c[0]) < 0.001)\
        and ((min(c[1], c[3]) <= y and y <= max(c[1], c[3])) or -0.001 < (y - c[1]) < 0.001):
        return True
    return False


# 判断射线穿过图形线段
def is_ray_cross_line(xo, yo, xr, yr, line):
    c = list(map(float, line.get_point()))
    m1 = (yr-yo)/(xr-xo)  # 表示射线斜率
    b1 = -((yr-yo)/(xr-xo))*xo+yo  # 表示射线截距
    if(c[2]-c[0]) == 0:  # 判断射线平行于y轴的情况
        xc = c[0]
        yc = m1*xc+b1
        if(is_point_on_the_line(xc, yc, line) and
            ((xc-xo)*(xr-xo) >= 0 and (yc-yo)*(yr-yo) >= 0)):
            return True
        return False
    m2 = (c[3]-c[1])/(c[2]-c[0])  # 线段斜率
    b2 = -((c[3]-c[1])/(c[2]-c[0]))*c[0]+c[1]
    if m1 == m2:  # 判断射线平行于x轴和斜率不为0的情况
        return False
    xc = (b2-b1)/(m1-m2)  # 交点坐标
    yc = (b2*m1 - b1*m2)/(m1-m2)
    if is_point_on_the_line(xc, yc, line):  # 判断交点是否在线段上
        if ((xc-xo)*(xr-xo)) >= 0 and ((yc-yo)*(yr-yo)) >= 0:  # 判断交点是否在射线上
            return True
    return False


# Define categorize point
def categorize_point(x, y, polygon):
    if mbr_method(x, y, polygon):  # Use MBR method 调用MBR方法(true运行里面的东西，false就不运行了 文档内解释）
        return "outside"
    for line in polygon.get_lines():  # 分类出点在线上的情况
        if is_point_on_the_line(x, y, line):
            return "boundary"
    # 接下来使用RcA方法
    xr, yr = get_ray(x, y, polygon)  # 得到一个点形成的射线，不穿过任何一个多边形顶点
    count = 0
    for line in polygon.get_lines():
        if is_ray_cross_line(x, y, xr, yr, line):  # 判断射线穿过边的次数
            count = count+1
    if count % 2 == 1:
        return "inside"  # 交点是奇数个，点在图形内部
    return "outside"  # 交点是偶数个，点在图形外部


def main():
    plotter = Plotter()
    print('read polygon.csv')
    polygon_points = read_file("polygon.csv")  # 相对路径读取文件
    polygon = Polygon(polygon_points)

    print('read input.csv')
    input_points = read_file("input.csv")

    print('categorize points')
    categorize_output = []
    for point in input_points[1:]:
        categorize_output.append(categorize_point(float(point[1]), float(point[2]), polygon))

    print('write output.csv')  # 创建输出的csv文件
    with open("output.csv", 'w') as f:
        f.writelines('id' + ',' + 'category' + '\n')
        for i in range(len(categorize_output)):
            f.writelines(str(i + 1) + ',' + categorize_output[i] + '\n')

    print('plot polygon and points')  # 作图
    xs = []
    ys = []
    for point in polygon_points[1:]:
        xs.append(float(point[1]))
        ys.append(float(point[2]))
    plotter.add_polygon(xs, ys)  # 画出多边形
    for i in range(len(input_points[1:])):
        xo = float(input_points[i + 1][1])
        yo = float(input_points[i + 1][2])
        plotter.add_point(xo, yo, kind=categorize_output[i])  # 画出判断后的点
        if categorize_output[i] != 'boundary':
            xr, yr = get_ray(xo, yo, polygon)
            plotter.add_ray(xo, yo, xr, yr)  # 在图上画出射线
    plotter.show()


if __name__ == '__main__':
    main()
