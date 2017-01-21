# Farbod Shahinfar
# Panzer Game
# 22/10/95
# player class
import label_obj
import panzer_obj
from my_pygame_tools import KeyboardHandler
from pygame import joystick

player_list = []


class Player(object):
    def __init__(self, controller, key_map, name, img):
        # if using joystick then it should be supplied if keyboard a keyboard handler should be given
        self.name = name
        self.controller = controller
        self.key_map = key_map
        self.panzer_img = img
        self.panzer = None
        self.score = 0
        self.killed = False
        player_list.append(self)

    def ready_panzer(self, pos, dire, clock, room):
        self.panzer = panzer_obj.Panzer(pos, self.panzer_img, (54, 54), clock, self, room, dire)

    def destroy(self):
        player_list.remove(self)
        # self.panzer.destroy()

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
        label = label_obj.Label(self.name + ": " + str(self.score), pos, (100, 120, 160))
        label.draw(screen)


def clear():
    player_list.clear()


def activate_all_players():
    for p in player_list:
        p.killed = False


def active_player():
    c = 0
    for p in player_list:
        if not p.killed:
            c += 1
    return c


def release_all_keys():
    for player in player_list:
        if player.controller_type() == 'keyboard':
            player.controller.all_keys_up()

