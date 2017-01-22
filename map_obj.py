# 3/11/95
# map_obj
import pygame
import wall_obj
import collectable_object
pygame.init()


def load(file_add):
    map_file = open(file_add, 'r')
    for line in map_file:
        if line[0] == '#':
            continue
        if 'Size' in line:
            data_string = remove_title(line, 'Size')
            data_string = data_string.strip()
            size = eval(data_string)
            continue
        elif 'Wall' in line:
            data_string = remove_title(line, 'Wall')
            data_string = data_string.strip()
            wall_image = pygame.image.load('images/wall.png').convert_alpha()
            wall_pos = brace_data(data_string, 0)
            wall_dir = brace_data(data_string, 1)
            wall_size = brace_data(data_string, 2)
            wall_obj.Wall(wall_image, wall_size, wall_pos, wall_dir)
        elif 'Collectable' in line:
            if 'Laser' in line:
                data_string = remove_title(line, 'Collectable-Laser').strip()
                collectable_pos = brace_data(data_string, 0)
                collectable_object.LaserObject(collectable_pos)
            if 'TirKoloft' in line:
                data_string = remove_title(line, 'Collectable-TirKoloft').strip()
                collectable_pos = brace_data(data_string, 0)
                collectable_object.TirKoloftObject(collectable_pos)
            if 'Amoo' in line:
                data_string = remove_title(line, 'Collectable-Amoo').strip()
                collectable_pos = brace_data(data_string, 0)
                collectable_object.AmooObject(collectable_pos)
            if 'TirNazok' in line:
                data_string = remove_title(line, 'Collectable-TirNazok').strip()
                collectable_pos = brace_data(data_string, 0)
                collectable_object.TirNazokObject(collectable_pos)
    map_file.close()


def get_walls(file_add):
    map_file = open(file_add, 'r')
    for line in map_file:
        if line[0] == '#':
            continue
        elif 'Wall' in line:
            data_string = remove_title(line, 'Wall')
            data_string = data_string.strip()
            wall_image = pygame.image.load('images/wall.png').convert_alpha()
            wall_pos = brace_data(data_string, 0)
            wall_dir = brace_data(data_string, 1)
            wall_size = brace_data(data_string, 2)
            wall_obj.Wall(wall_image, wall_size, wall_pos, wall_dir)
    map_file.close()


def get_start_points(file_add):
    points = []
    map_file = open(file_add, 'r')
    for line in map_file:
        if line[0] == '#':
            continue
        elif 'Start_Point' in line:
            data_string = remove_title(line, "Start_Point").strip()
            pos = brace_data(data_string, 0)
            dire = brace_data(data_string, 1)
            points.append((pos, dire))
    return points


def remove_title(string, title):
    """
    string = title: data
    :param string: string having data in it
    :param title: starting title of line
    :return: str
    """
    return string[len(title)+2:]


def find_semi_colon(string, index):
    count = -1
    last_comma = 1
    for i in range(len(string)):
        if string[i] == ';' or string[i]=='}':
            count += 1
            if count == index:
                return last_comma, i
            last_comma = i+1 # it is not simi colon's index. it is next character's index.
    # if not found
    return -1, -1


def brace_data(string, index):
    semi_colon_pos = find_semi_colon(string, index)
    data = string[semi_colon_pos[0]:semi_colon_pos[1]].strip()
    if data != '':
        return eval(data)
