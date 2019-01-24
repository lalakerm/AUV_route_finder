import os

INFO_POINTS = ('start point', 'final point', 'refuel points',
               'scale(1:km)', 'speed(km/h)', 'battery life(h)',
               'charging time(min)')


def txt_parse(filepath):
    try:
        file = open(os.getcwd() + filepath, 'r')
        text = file.readlines()
        if check_structure(text, INFO_POINTS):
            data = dict()
            for p in INFO_POINTS:
                for line in text:
                    if p in line:
                        data[p] = get_value(line, p)
            return data
        else:
            print('Check file structure.')
    except FileNotFoundError:
        print('File not found, check directory.')


def check_structure(text, info_points):  # check file structure
    for p in info_points:
        i = 0  # number of info_point occurrence in file
        for line in text:
            if p in line:
                i += 1
        if i != 1:
            return False
    return True


def get_value(line, p):
    if p in INFO_POINTS[0:3]:
        return eval(line[line.find('('):line.rfind(')') + 1])
    else:
        return [int(s) for s in line.split() if s.isdigit()][0]
