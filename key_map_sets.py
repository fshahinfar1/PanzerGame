# farbod shahinfar
# panzer game
# 23/10/95
import pygame
from my_pygame_tools import KeyboardHandler


class KeySetOne:
    keyboard = KeyboardHandler()
    keyboard.connect_keys('right', 'left', 'up', 'down', 'space')
    key_map = {'rotate_right': keyboard.get_key('right'), 'rotate_left': keyboard.get_key('left'),\
               'forward': keyboard.get_key('up'),  'backward': keyboard.get_key('down'),\
               'fire': keyboard.get_key('space')}


class KeySetTwo:
    keyboard = KeyboardHandler()
    keyboard.connect_keys('d', 'a', 'w', 's', 'q')
    key_map = {'rotate_right': keyboard.get_key('d'), 'rotate_left': keyboard.get_key('a'),\
               'forward': keyboard.get_key('w'), 'backward': keyboard.get_key('s'), 'fire': keyboard.get_key('q')}


class KeySetThree:
    keyboard = KeyboardHandler()
    keyboard.connect_keys('[6]', '[4]', '[8]', '[2]', '[5]')
    key_map = {'rotate_right': keyboard.get_key('[6]'), 'rotate_left': keyboard.get_key('[4]'),\
               'forward': keyboard.get_key('[8]'), 'backward': keyboard.get_key('[2]'),\
               'fire': keyboard.get_key('[5]')}


class Joystic_set_one:
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
