# Farbod Shahinfar
# Panzer Game
# 22/10/95
# player class
import label_obj
from my_pygame_tools import KeyboardHandler
from pygame import joystick
player_list = []


class Player(object):
    def __init__(self, controller, panzer, key_map, name):
        # if using joystick then it should be supplied if keyboard a keyboard handler should be given
        self.name = name
        self.controller = controller
        self.key_map = key_map
        self.panzer = panzer
        self.score = 0
        self.killed = False
        player_list.append(self)

    def destroy(self):
        player_list.remove(self)
        self.panzer.destroy()

    def get_panzer(self):
        return self.panzer

    def get_controller(self):
        return self.controller

    def controller_type(self):
        if isinstance(self.controller, KeyboardHandler):
            return "keyboard"
        elif isinstance(self.controller, joystick.JoystickType):
            return "joystick"

    def add_score(self, value):
        self.score += value

    def draw(self, screen, pos):
        label = label_obj.Label(self.name + ": " + str(self.score), pos, (0, 0, 0))
        label.draw(screen)


def clear():
    player_list.clear()