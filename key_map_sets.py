# farbod shahinfar
# panzer game
# 23/10/95
import pygame as pg
import panzer_obj as pz
from my_pygame_tools import KeyboardHandler


class KeySetOne:
    def __init__(self):
        # self.keyboard = KeyboardHandler()
        # self.keyboard.connect_keys('right', 'left', 'up', 'down', 'space')
        # self.keyboard.connect_keys(pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN, pg.K_SPACE)
        # self.key_map = {'rotate_right': self.keyboard.get_key('right'), 'rotate_left': self.keyboard.get_key('left'),\
        #                 'forward': self.keyboard.get_key('up'),  'backward': self.keyboard.get_key('down'),\
        #                 'fire': self.keyboard.get_key('space')}
        self.control = "keyboard"
        self.key_map = {'rotate_right': pg.K_RIGHT, 'rotate_left': pg.K_LEFT,\
                        'forward': pg.K_UP,  'backward': pg.K_DOWN,\
                        'fire': pg.K_SPACE}


class KeySetTwo:
    def __init__(self):
        self.keyboard = KeyboardHandler()
        self.keyboard.connect_keys('d', 'a', 'w', 's', 'q')
        self.key_map = {'rotate_right': self.keyboard.get_key('d'), 'rotate_left': self.keyboard.get_key('a'),\
                        'forward': self.keyboard.get_key('w'), 'backward': self.keyboard.get_key('s'), 'fire': self.keyboard.get_key('q')}


class KeySetThree:
    def __init__(self):
        # self.keyboard = KeyboardHandler()
        # self.keyboard.connect_keys(pg.K_KP6, pg.K_KP4, pg.K_KP8, pg.K_KP2, pg.K_KP5)
        # self.key_map = {'rotate_right': self.keyboard.get_key('[6]'), 'rotate_left': self.keyboard.get_key('[4]'),\
        #                 'forward': self.keyboard.get_key('[8]'), 'backward': self.keyboard.get_key('[2]'),\
        #                 'fire': self.keyboard.get_key('[5]')}
        self.control = "keyboard"
        self.key_map = {'rotate_right': pg.K_KP6, 'rotate_left': pg.K_KP4, \
                        'forward': pg.K_KP8, 'backward': pg.K_KP2, \
                        'fire': pg.K_KP5}


class JoystickSetOne:
    # todo Not useful yet
    def __init__(self, joystick_set_number):
        pg.joystick.init()
        if pg.joystick.get_count() < 1:
            print("Error: please connect game pad !!!")
            raise
        self.joystick = pg.joystick.Joystick(joystick_set_number)
        self.joystick.init()
        self.key_map = {'rotate_right': (self.joystick.get_hat(0) == (1, 0)),\
                        'rotate_left': (self.joystick.get_hat(0) == (-1, 0)),\
                        'forward': (self.joystick.get_hat(0) == (0, 1)),\
                        'backward': (self.joystick.get_hat(0) == (0, -1)),\
                        'fire': (self.joystick.get_button(2))}


