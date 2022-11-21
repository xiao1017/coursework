from plotter import Plotter


# Define read file from file_address
def read_file(file_address):
    with open(file_address) as f:
        data = f.read().splitlines()
    point_list = []  # Creat point list
    for row in data:
        point_list.append(row.split(','))
    return point_list


# Create a line class, use (x1, y1), (x2, y2) to represent the line
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


# Create a polygon class and create a list of lines
class Polygon:
    def __init__(self, points):
        self.__points = points   # Data type is[[id,x,y],[str,str,str],...]
        lines = []
        # Create line list according to pointlist
        for i in range(len(points)-2):
            line = Line(name=points[i+1][0]+'-'+points[i+2][0], x1=points[i+1][1],
                        y1=points[i+1][2], x2=points[i+2][1], y2=points[i+2][2])
            lines.append(line)
        self.__lines = lines

    def get_points(self):
        return self.__points

    # Define to get a specific point according to index
    def get_point(self, index):
        return self.__points[index]

    def get_lines(self):
        return self.__lines

    # Define to get a specific line according to index
    def get_line(self, index):
        return self.__lines[index]


# Define MBR method
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
    # Determine whether the point is outside the rectangle
    if x < minx or x > maxx or y < miny or y > maxy:
        return True
    return False


# Get a ray that does not pass through the vertices of the graph
def get_ray(x, y, polygon):
    xr = 6
    yr = 5
    n = 1
    while n != 0:
        xr = xr + 1   # Get new points
        yr = yr + xr+1
        # Avoid overlapping selected ray float with original float
        # Precision of *1000 is used to represent the float
        if int((x-xr) * 1000) != 0 and int((y-yr) * 1000) != 0:
            n = 0
            for point in polygon.get_points()[1:]:  # Judgment point coincidence
                point = list(map(float, point))  # Data type converted to float
                if round(((point[2]-y)*(xr-x)-(yr-y)*(point[1]-x))*100) == 0:
                    n = n + 1
    return xr, yr


# Determine whether the point is on a line segment
def is_point_on_the_line(x, y, line):
    c = list(map(float, line.get_point()))
    # Determine whether three points on one line, the point in the rectangle
    if round(((x-c[0])*(c[3]-c[1])-(c[2]-c[0])*(y-c[1]))*1000) == 0\
        and ((min(c[0], c[2]) <= x and x <= max(c[0], c[2]))
             or -0.001 < (x - c[0]) < 0.001)\
        and ((min(c[1], c[3]) <= y and y <= max(c[1], c[3]))
             or -0.001 < (y - c[1]) < 0.001):
        return True
    return False


# Judging that the ray passes through the graphic line segment
def is_ray_cross_line(xo, yo, xr, yr, line):
    c = list(map(float, line.get_point()))
    m1 = (yr-yo)/(xr-xo)  # The slope of the ray
    b1 = -((yr-yo)/(xr-xo))*xo+yo  # The ray intercept
    # Judging the situation where the ray is parallel to the y-axis
    if(c[2]-c[0]) == 0:
        xc = c[0]
        yc = m1*xc+b1
        if(is_point_on_the_line(xc, yc, line) and
            ((xc-xo)*(xr-xo) >= 0 and (yc-yo)*(yr-yo) >= 0)):
            return True
        return False
    m2 = (c[3]-c[1])/(c[2]-c[0])
    b2 = -((c[3]-c[1])/(c[2]-c[0]))*c[0]+c[1]
    # Judging the ray is parallel to the x-axis, the slope of the ray not 0
    if m1 == m2:
        return False
    xc = (b2-b1)/(m1-m2)  # Intersection coordinates
    yc = (b2*m1 - b1*m2)/(m1-m2)
    if is_point_on_the_line(xc, yc, line):
        if ((xc-xo)*(xr-xo)) >= 0 and ((yc-yo)*(yr-yo)) >= 0:
            return True
    return False


# Define categorize point
def categorize_point(x, y, polygon):
    if mbr_method(x, y, polygon):  # Use MBR method
        return "outside"
    for line in polygon.get_lines():  # Classify points on a line segments
        if is_point_on_the_line(x, y, line):
            return "boundary"
    # Use RcA method
    xr, yr = get_ray(x, y, polygon)
    count = 0
    for line in polygon.get_lines():
        # number of times the ray crosses the edge
        if is_ray_cross_line(x, y, xr, yr, line):
            count = count+1
    if count % 2 == 1:
        return "inside"  # Number of intersection points is odd
    return "outside"  # Number of intersection points is even


def main():
    plotter = Plotter()
    print('read polygon.csv')
    polygon_points = read_file("polygon.csv")  # Relative path to read file
    polygon = Polygon(polygon_points)

    print('read input.csv')
    input_points = read_file("input.csv")

    print('categorize points')
    categorize_output = []
    for point in input_points[1:]:
        categorize_output.append(categorize_point(float(point[1]),
                                                  float(point[2]), polygon))

    print('write output.csv')  # Create output csv file
    with open("output.csv", 'w') as f:
        f.writelines('id' + ',' + 'category' + '\n')
        for i in range(len(categorize_output)):
            f.writelines(str(i + 1) + ',' + categorize_output[i] + '\n')

    print('plot polygon and points')
    xs = []
    ys = []
    for point in polygon_points[1:]:
        xs.append(float(point[1]))
        ys.append(float(point[2]))
    plotter.add_polygon(xs, ys)  # Draw polygon
    for i in range(len(input_points[1:])):
        xo = float(input_points[i + 1][1])
        yo = float(input_points[i + 1][2])
        plotter.add_point(xo, yo, kind=categorize_output[i])  # Draw judged points
        if categorize_output[i] != 'boundary':
            xr, yr = get_ray(xo, yo, polygon)
            plotter.add_ray(xo, yo, xr, yr)  # Draw rays
    plotter.show()


if __name__ == '__main__':
    main()
