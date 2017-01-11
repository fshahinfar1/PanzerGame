# Farbod Shahinfar
# 16/10/95
# map_obj
import pygame
import wall_obj
pygame.init()


class Map:
    def __init__(self, file_add):
        self.walls_list = []
        map_file = open(file_add, 'r')
        for line in map_file:
            if line[0] == '#':
                continue
            if 'Size' in line:
                data_string = remove_title(line, 'Size')
                data_string = data_string.strip()
                self.size = eval(data_string)
                continue
            elif 'Wall' in line:
                data_string = remove_title(line, 'Wall')
                data_string = data_string.strip()
                wall_image = pygame.image.load('images/wall.png')
                wall_pos = brace_data(data_string, 0)
                wall_dir = brace_data(data_string, 1)
                wall_size = brace_data(data_string, 2)
                new_wall = wall_obj.Wall(wall_image, wall_size, wall_pos, wall_dir)
                self.walls_list.append(new_wall)


def get_walls(file_add):
    walls_list = []
    map_file = open(file_add, 'r')
    for line in map_file:
        if line[0] == '#':
            continue
        elif 'Wall' in line:
            data_string = remove_title(line, 'Wall')
            data_string = data_string.strip()
            wall_image = pygame.image.load('images/wall.png')
            wall_pos = brace_data(data_string, 0)
            wall_dir = brace_data(data_string, 1)
            wall_size = brace_data(data_string, 2)
            new_wall = wall_obj.Wall(wall_image, wall_size, wall_pos, wall_dir)
            walls_list.append(new_wall)
    print walls_list
    return walls_list


def remove_title(string, title):
    """
    string = title: data
    :param string: string having data in it
    :param title: starting title of line
    :return: str
    """
    return string[len(title)+2:]


def find_comma(string, index):
    count = -1
    last_comma = 1
    for i in range(len(string)):
        if string[i] == ';' or string[i]=='}':
            count += 1
            if count == index:
                return last_comma, i
            last_comma = i+1
    # if not found
    return -1, -1


def brace_data(string, index):
    comma_pos = find_comma(string, index)
    print(comma_pos)
    data = string[comma_pos[0]:comma_pos[1]].strip()
    print(data)
    if data != '':
        return eval(data)
