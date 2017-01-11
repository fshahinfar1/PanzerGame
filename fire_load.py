# Farbod Shahinfar
# 13/10/95
# bouncy fire load
import pygame
import position_class
import collision_tools
from math import radians, sin, cos


class BouncyFireLoad(object):
    def __init__(self, pos, direction, speed=2, room=None, holder=None):
        self.size = (16, 16)
        self.image_original = pygame.image.load("./images/bouncy_fire_load.png")
        self.image = pygame.transform.scale(self.image_original, self.size)
        self.position = position_class.Position(pos)
        self.speed = speed
        self.direction = direction
        self.collision_obj = collision_tools.CollisionCircle(self.position, 8, self)
        self.room = room
        self.holder = holder

    def destroy(self):
        print('bullet destroy')
        self.collision_obj.destroy()
        self.holder.remove(self)
        del self

    def update_position(self):
        theta = radians(self.direction)
        self.position += (self.speed*cos(theta), self.speed*sin(theta))
        self.collision_obj.set_position(self.position)
        if self.room.is_out_of_room(self.position):
            self.destroy()

    def loop(self):
        self.update_position()
        may_collide_list = collision_tools.get_object_may_collide(self.collision_obj, 30)
        for obj in may_collide_list:
            if self.collision_obj.is_colliding_with(obj):
                self.destroy()
                print('destroy by {0}'.format(obj))
                return True  # True means it is time to say goodbye
        return False

    def link_holder(self, holder):
        self.holder = holder

    def draw(self, screen):
        left_corner = self.position - (8, 8)
        screen.blit(self.image, left_corner)


