import pygame
import player_class
from key_map_sets import *
control_map = {"KeySetOne": KeySetOne, "KeySetTwo": KeySetTwo, "KeySetThree": KeySetThree,
               "JoystickSetOne": JoystickSetOne,}


def init_players(add):
    infile = open(add, "r")
    n = 0  # number of players
    idx = -1  # joystick index
    name = ""  # player name
    img = ""  # player image
    for line in infile:
        if line[0] == '#':
            continue
        elif "player_num" in line:
            data = remove_title(line, "player_num").strip()
            n = brace_data(data, 0)
        elif "start" in line:
            control = ""
            idx = -1
            name = ""
            img = ""
        elif "control" in line:
            data = remove_title(line, "control").strip()
            control = brace_data(data, 0)
            if "Joystick" in control:
                idx = brace_data(data, 1)
        elif "name" in line:
            data = remove_title(line, "name").strip()
            name = brace_data(data, 0)
        elif "image" in line:
            data = remove_title(line, "image").strip()
            img = brace_data(data, 0)
        elif "end" in line:
            img = pygame.image.load(img).convert_alpha()
            if "Joystick" in control:
                t = control
                control = control_map[control](idx)
                player_class.Player(t, control.joystick, control.key_map, name, img)
            else:
                t = control
                control = control_map[control]()
                player_class.Player(t, control.control, control.key_map, name, img)


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
        if string[i] == ';' or string[i] == '}':
            count += 1
            if count == index:
                return last_comma, i
            last_comma = i+1  # it is not simi colon's index. it is next character's index.
    # if not found
    return -1, -1


def brace_data(string, index):
    semi_colon_pos = find_semi_colon(string, index)
    data = string[semi_colon_pos[0]:semi_colon_pos[1]].strip()
    if data != '':
        return eval(data)
