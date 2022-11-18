polygon_file_address = 'C:/Users/XIAOYU/Desktop/polygon.csv'


def read_file(polygon_file_address):
    with open(polygon_file_address) as f:
        data = f.read().splitlines()
    point_list_a = []
    for row in data:
        point_list_a.append(row.split(','))
    return point_list_a