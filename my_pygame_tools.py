# farbod shahinfar
# MyPyGameTools
# version 0.000beta
# last update : 22/10/95
import pygame
from math import sin, cos, atan, degrees, radians



class Colors:
    """
    this class attributes are RGB value for colors
    this helps to avoid giving a tuple of (R, G, B)
    and instead say Colors.color which makes more sense
    """
    def __init__(self):
        #                    R    G    B
        self.WHITE       = (255, 255, 255)
        self.GRAY        = (185, 185, 185)
        self.BLACK       = (  0,   0,   0)
        self.RED         = (155,   0,   0)
        self.LIGHTRED    = (175,  20,  20)
        self.GREEN       = (  0, 155,   0)
        self.LIGHTGREEN  = ( 20, 175,  20)
        self.BLUE        = (  0,   0, 155)
        self.LIGHTBLUE   = ( 20,  20, 175)
        self.YELLOW      = (155, 155,   0)
        self.LIGHTYELLOW = (175, 175,  20)


class Key(object):
    """
    it represents a key on key board and
    give me some good functions to check their state
    """
    def __init__(self, name):
            self.key_name = name
            self.key_hold = False

    def __eq__(self, other):
        if isinstance(other, Key):
            return self.is_key(other.key_name)

    def get_key(self):
        return self.key_name

    def change_key(self, looking):
        self.key_name = looking

    def is_key(self, name):
        if self.key_name == name:
            return True
        return False

    def set_key_down(self):
        self.key_hold = True

    def set_key_up(self):
        self.key_hold = False

    def check_event_key_down(self, event):
        if pygame.key.name(event.key) == self.key_name:
            self.key_hold = True
            return True
        return False
    
    def check_event_key_up(self, event):
        if pygame.key.name(event.key) == self.key_name:
            self.key_hold = False
            return True
        return False
    
    def check_hold(self):
        return self.key_hold


class KeyboardHandler(object):
    def __init__(self):
        self.connected_keys = {}
    
    def connect_keys(self, *params):
        """
        add Key to self.connected_keys for further process

        :param params: name of the key (string)
        :return: None
        """
        for item in params:
            key = Key(item)
            self.connected_keys[item] = key

    def is_key_connected(self, key_name):
        if key_name in self.connected_keys:
            return True
        return False

    def get_key(self, key_name):
        """
        if key is connected
        it will give access to that key
        :param key_name:
        :return:
        """
        if key_name in self.connected_keys:
            return self.connected_keys[key_name]
        return None

    def get_events(self, events):
        """
        it will gets all events and loops between
        events and set values for connected keys
        :param events:
        :return:
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if self.is_key_connected(key_name):
                    self.connected_keys[key_name].set_key_down()
            elif event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                if self.is_key_connected(key_name):
                    self.connected_keys[key_name].set_key_up()

    def get_event(self, event):
        """
        it will take an event it is much like get_events() but
        it is used in a loop it self instead of creating a loop in
        side of function
        :param event:
        :return:
        """
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if self.is_key_connected(key_name):
                self.connected_keys[key_name].set_key_down()
        elif event.type == pygame.KEYUP:
            key_name = pygame.key.name(event.key)
            if self.is_key_connected(key_name):
                self.connected_keys[key_name].set_key_up()

    def is_key_hold(self, key_name):
        """
        with this function I can check connected key state
        :param key_name:
        :return:
        """
        if key_name in self.connected_keys:
            return self.connected_keys[key_name].check_hold()


class Mouse(object):
    """
        this class handles mouse
        use event_btn_pressed() and event_btn_released()
        in events loop and supply them with event
        it will set values it self
        you just need to check for thing you want
        in logic loop
        use is_btn_hold()
        num = 1 -> left_btn
        num = 2 -> right_btn
    """
    def __init__(self):
        self.btn1 = False
        self.btn1Pressed = False
        self.btn2 = False
        self.btn2Pressed = False

    def get_pos(self):
        return pygame.mouse.get_pos()

    def event_btn_pressed(self, event):
        if event.button == 1:
            self.btn1 = True
            self.btn1Pressed = True
        else:
            self.btn2 = True
            self.btn2Pressed = True

    def event_btn_released(self, event):
        if event.button == 1:
            self.btn1 = False
            self.btn1Pressed = False
        else:
            self.btn2 = False
            self.btn2Pressed = False
        
    def is_btn_pressed(self, num):
        n = int(num)
        ans = None
        if n == 1:
            ans = self.btn1Pressed
            self.btn1Pressed = False
        elif n == 2:
            ans = self.btn2Pressed
            self.btn2Pressed = False
        return ans
    
    def is_btn_hold(self, num):
        n = int(num)
        if n == 1:
            return self.btn1
        elif n == 2:
            return self.btn2
        return None


# Screen
def init_screen(size, caption):
    scr = pygame.display.set_mode(size)
    pygame.display.set_caption(caption)
    return scr


# Functions
def absolute(value):
    if value < 0:
        return -1*value
    return value


def sgn(value):
    if isinstance(value, (int, float)):
        if value == 0:
            return 0
        else:
            return int(value/absolute(value))
    else:
        print("Unsupported Type for function sgn in <my_pygame_tools.py>")
        raise


def is_in_rectangle(pos,rect):
        if pos[0] > rect[0] and pos[0] < rect[0] + rect[2]:
            if pos[1] > rect[1] and pos[1]< rect[1] + rect[3]:
                return True
        return False


def distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


def get_direction(p1, p2):
    pi = 3.14159
    flag_plus_pi = False
    delta_y = p2[1]-p1[1]
    delta_x = p2[0]-p1[0]
    if delta_x == 0:
        if delta_y > 0:
            return 90
        else:
            return -90
    if delta_x < 0:
        flag_plus_pi = True
    m = delta_y/delta_x
    if flag_plus_pi:
        return degrees(atan(m) + pi)
    return degrees(atan(m))


def is_between_two_point(pos, p1, p2):
    min_x = min(p1[0], p2[0])
    max_x = max(p1[0], p2[0])
    width = max_x-min_x
    min_y = min(p1[1], p2[1])
    max_y = max(p1[1], p2[1])
    height = max_y - min_y
    rect = [min_x, min_y, width, height]
    return is_in_rectangle(pos, rect)


def rotate_point(point, degree):
    theta = radians(degree)
    new_x = cos(theta) * point[0] - sin(theta) * point[1]
    new_y = sin(theta) * point[0] + cos(theta) * point[1]
    return new_x, new_y


def calculate_directional_position(direction, position, speed):
    """
    it calculates a new position which has a distance of size speed from the position
    in direction of this object
    :param direction:
    :param position:
    :param speed:
    :return: position_class.Position
    """
    theta = radians(direction)
    return position + (speed * cos(theta), speed * sin(theta))


def in_360_degree(degree):
    if degree > 360:
        return degree % 360
    if degree < 0:
        return 360 - (degree % 360)
    return degree


def reflect(degree, surface_degree):
    ref_degree = 2 * surface_degree - degree + 360
    return ref_degree


def draw_polyline(screen, color, list_point, width=1):
    for i in range(len(list_point)-1):
        pygame.draw.line(screen, color, list_point[i], list_point[i+1], width)

