# Farbod Shahinfar
# 20/10/95
# bouncy fire load
import pygame
import position_class
import collision_tools
import wall_obj
from math import radians, sin, cos
from my_pygame_tools import in_360_degree, reflect, calculate_directional_position, draw_polyline


class BouncyFireLoad(object):
    def __init__(self, pos, direction, speed=2, room=None, holder=None):
        self.size = (16, 16)
        self.image_original = pygame.image.load("./images/bouncy_fire_load.png")
        # todo it is a good idea to create a class able to handle animation and use it instead
        self.image = pygame.transform.scale(self.image_original, self.size)
        self.position = position_class.Position(pos)  # current position of obj
        self.speed = speed  # moving speed
        self.direction = direction  # movement direction
        self.collision_obj = collision_tools.CollisionCircle(self.position, 8, self)
        # todo Do I really need to give the room to object ??
        self.room = room  # room which this object is in
        # todo it is a good idea to use a class list instead of list below
        self.holder = holder  # list in the room which keeps track of this type object

    def destroy(self):
        print('bullet destroy')
        self.collision_obj.destroy()
        self.holder.remove(self)
        del self  # does it do anything or not??

    def calculate_new_position(self):
        theta = radians(self.direction)
        return self.position + (self.speed * cos(theta), self.speed * sin(theta))

    def update_position(self):
        self.position = self.calculate_new_position()
        # move collision shell to new position
        self.collision_obj.set_position(self.position)
        # if ball is out of the room so lets forget about it
        if self.room.is_out_of_room(self.position):
            self.destroy()

    def loop(self):
        # all collision logic of the bullet is here
        self.update_position()
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if isinstance(collide_object.get_parent(), wall_obj.Wall):
                # fixme problem in_360_degree
                # self.direction = in_360_degree(self.direction)
                self.position = self.collision_obj.move_to_edge(collide_object, self.direction)
                self.direction = reflect(self.direction, collide_object.get_colliding_surface_angle(self.collision_obj))
            else:
                self.destroy()
                print('destroy by {0}'.format(collide_object))
                return True  # True means it is time to say goodbye
        return False

    def link_holder(self, holder):
        self.holder = holder

    def draw(self, screen):
        left_corner = self.position - (8, 8)
        screen.blit(self.image, left_corner)


class Laser(object):
    def __init__(self, pos, direction):
        self.fire_position = position_class.Position(pos)
        self.direction = direction
        self.collision_object = collision_tools.CollisionPoint(self.fire_position, self)
        self.fire_state = 'Aim'
        self.length = 400
        self.break_points = [pos]

    def set_direction(self, value, rel=False, update=True):
        if rel:
            self.direction += value
        else:
            self.direction = value
        if update:
            self.update()

    def set_position(self, value, rel=False, update=True):
        if rel:
            self.fire_position += value
        else:
            self.fire_position = value
        if update:
            self.update()

    def update(self):
        self.collision_object.set_position(self.fire_position)
        self.break_points = [self.fire_position]
        l = 1
        d = 2
        print('================')
        while l < self.length:
            self.collision_object.set_position(calculate_directional_position(self.direction, self.collision_object.get_position(), d))
            collide_obj = collision_tools.is_colliding(self.collision_object, self.collision_object.get_position(),
                                                       self.collision_object)
            if collide_obj is not None and isinstance(collide_obj, collision_tools.CollisionFixRectangle):
                self.break_points.append(position_class.Position(self.collision_object.get_position()))
                print(self.collision_object.get_position())
                self.direction = reflect(self.direction, collide_obj.get_colliding_surface_angle(self.collision_object))
            l += d
        self.break_points.append(position_class.Position(self.collision_object.get_position()))
        print('================')

    def loop(self):
        pass

    def draw(self, screen):
        red = (150, 0, 0)
        green = (0, 200, 0)
        theta = radians(self.direction)
        # u_r = position_class.Position((cos(theta), sin(theta)))
        draw_polyline(screen, red, self.break_points, 3)
        for pos in self.break_points:
            pygame.draw.circle(screen, green, pos.int_cordinates(), 2)
        # pygame.draw.polygon(screen, red, self.break_points, 3)

