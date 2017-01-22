# panzer game
# 3/11/95
import pygame as pg


class KeySetOne:
    def __init__(self):
        self.control = "keyboard"
        self.key_map = {'rotate_right': pg.K_RIGHT, 'rotate_left': pg.K_LEFT,
                        'forward': pg.K_UP,  'backward': pg.K_DOWN,
                        'fire': pg.K_SPACE}


class KeySetTwo:
    def __init__(self):
        self.control = "keyboard"
        self.key_map = {'rotate_right': pg.K_d, 'rotate_left': pg.K_a,
                        'forward': pg.K_w, 'backward': pg.K_s, 'fire': pg.K_q}


class KeySetThree:
    def __init__(self):
        self.control = "keyboard"
        self.key_map = {'rotate_right': pg.K_KP6, 'rotate_left': pg.K_KP4,
                        'forward': pg.K_KP8, 'backward': pg.K_KP2,
                        'fire': pg.K_KP5}


class JoystickSetOne:
    def __init__(self, joystick_set_number):
        pg.joystick.init()
        if pg.joystick.get_count() < 1:
            print("Error: please connect game pad !!!")
            raise
        self.control = JoystickSetOne
        self.joystick = pg.joystick.Joystick(joystick_set_number)
        self.joystick.init()
        self.key_map = {'rotate_right': (self.joystick.get_hat(0) == (1, 0)),
                        'rotate_left': (self.joystick.get_hat(0) == (-1, 0)),
                        'forward': (self.joystick.get_hat(0) == (0, 1)),
                        'backward': (self.joystick.get_hat(0) == (0, -1)),
                        'fire': (self.joystick.get_button(2))}


control_map = {"KeySetOne": KeySetOne, "KeySetTwo": KeySetTwo, "KeySetThree": KeySetThree,
               "JoystickSetOne": JoystickSetOne}
