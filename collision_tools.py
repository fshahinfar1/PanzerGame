# Farbod Shahinfar
# 12/10/95
# collision tools
import position_class
from my_pygame_tools import distance, sgn
from math import sin, cos, radians
collidable_objects = {}  # a dictionary of all objects of CollisionCircle


class CollisionCircle(object):

    def __init__(self, pos, r, link_object=None, solid=False):
        self.position = position_class.Position(pos)
        self.radius = r
        self.object = link_object
        self.solid = solid
        # add object to collidabel objects dictionary
        collidable_objects[self] = self.position

    def destroy(self):
        del collidable_objects[self]

    def __str__(self):
        return "Circle at {0}".format(self.position)

    def is_solid(self):
        return self.solid

    def set_solid(self):
        self.solid = True

    def get_radius(self):
        return self.radius

    def set_radius(self, value):
        self.radius = value

    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = position_class.Position(pos)
        # self.position.int_cordinates()

    def is_colliding_with(self, other):
        if isinstance(other, CollisionCircle):
            R = self.radius + other.radius
            dist = distance(self.position, other.position)
            if dist > R:
                return False
            return True
        if isinstance(other, CollisionFixRectangle):
            dx = other.position[0] - self.position[0]
            dy = other.position[1] - self.position[1]
            if dx < 0:
                dx += other.width
                if dx > 0:
                    dx = 0
            if dy < 0:
                dy += other.height
                if dy > 0:
                    dy = 0
            dx = abs(dx)
            dy = abs(dy)
            if dx**2 + dy**2 <= self.radius**2:
                return True
            return False

    def will_collide_with_at(self, other, pos):
        if isinstance(other, CollisionCircle):
            R = self.radius + other.radius
            dist = distance(pos, other.position)
            if dist >= R:
                return False
            return True
        if isinstance(other, CollisionFixRectangle):
            dx = other.position[0] - pos[0]
            dy = other.position[1] - pos[1]
            if dx < 0:
                dx += other.width
                if dx > 0:
                    dx = 0
            if dy < 0:
                dy += other.height
                if dy > 0:
                    dy = 0
            dx = abs(dx)
            dy = abs(dy)
            if dx**2 + dy**2 <= self.radius**2:
                return True
            return False

    def move_to_edge(self, other, direction):
        # fixme direction of the panzer will affect this and \
        # fixme there is a huge problem on left side and will moving backward
        dp = 0.01
        theta = radians(direction)
        while self.is_colliding_with(other):
            self.position -= (dp * cos(theta), dp * sin(theta))
        return self.position


class CollisionFixRectangle(object):
    def __init__(self, pos, w, h, link_object=None, solid=False):
        self.position = position_class.Position(pos)  # left top corner of rectangle
        self.width = w
        self.height = h
        self.object = link_object
        self.solid = solid
        # add object to collidabel objects dictionary
        collidable_objects[self] = self.position

    def destroy(self):
        del collidable_objects[self]

    def __str__(self):
        return "FixRectangle at {0}".format(self.position)

    def is_solid(self):
        return self.solid

    def set_solid(self):
        self.solid = True

    def get_position(self):
        return self.position

    def set_position(self, pos):
        self.position = position_class.Position(pos)

    def get_corner(self, right, down):
        """
        c = 0 -> top left corner
        c = 1 -> top right corner
        c = 2 -> bellow left corner
        c = 3 -> bellow right corner
        :param right:
        :param down:
        :return:
        """
        map_dict = {0: self.position, 1: self.position+(self.width, 0),\
                   2: self.position + (0, self.height), 3: self.position + (self.width, self.height)
                    }
        c = 0
        if right:
            c += 1
        if down:
            c += 2

        return map_dict[c]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.width, self.height

    def is_colliding_with(self, other):
        if isinstance(other, CollisionFixRectangle):
            if (self.position[0] < other.position[0] + other.width) and\
                    (self.position[0] + self.width > other.position[0]) and\
                    (self.position[1] < other.position[1] + other.height) and\
                    (self.position[1] + self.height > other.position[1]):
                return True
            return False
        if isinstance(other, CollisionCircle):
            dx = self.position[0] - other.position[0]
            dy = self.position[1] - other.position[1]
            if dx < 0:
                dx += self.width
                if dx > 0:
                    dx = 0
            if dy < 0:
                dy += self.height
                if dy > 0:
                    dy = 0
            dx = abs(dx)
            dy = abs(dy)
            if dx**2 + dy**2 < other.radius**2:
                return True
            return False

    # todo Add move to Edge function here
    # todo this is important

    def move_to_edge(self, other, direction):
        # fixme direction of the panzer will affect this and \
        # fixme there is a huge problem on left side and will moving backward
        dp = 1
        theta = radians(direction * sgn(self.object.get_speed()))
        while self.is_colliding_with(other):
            self.position -= (dp * cos(theta), dp * sin(theta))
        return self.position


# Functions
def get_object_may_collide(object, range_radius, *args):
    result = []
    log = open('log.txt', 'a')
    log.write(str(args)+'\n')
    if isinstance(object, (CollisionCircle, CollisionFixRectangle)):
        for item in collidable_objects.items():
            if isinstance(item[0], CollisionFixRectangle):
                if distance(object.get_position(), item[1]) - item[0].get_width() < range_radius:
                    if (item[0] is not object) and (item[0] not in list(args)):  # exclude object it self and args
                        result.append(item[0])
            elif isinstance(item[0], CollisionCircle):
                if distance(object.get_position(), item[1]) < range_radius:
                    if (item[0] is not object) and (item[0] not in list(args)):  # exclude object it self and args
                        result.append(item[0])
        return result


def update_collidable_objects_list_position():
    # fixme It looks it is not working
    for item in collidable_objects:
        collidable_objects[item] = item.get_position()
