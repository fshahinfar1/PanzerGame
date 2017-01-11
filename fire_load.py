# Farbod Shahinfar
# 20/10/95
# bouncy fire load
import pygame
import position_class
import collision_tools
import wall_obj
from math import radians, sin, cos


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
                # fixme find a better way to calculate reflaction from surface with angle = theta
                self.position = self.collision_obj.move_to_edge(obj, self.direction)
                self.direction = 360 - self.direction  # reflect the ball from theta = 0 surface
                if self.collision_obj.will_collide_with_at(obj, self.calculate_new_position()):
                    self.direction = 90 - self.direction  # reflect the ball from theta = 90 surface
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


