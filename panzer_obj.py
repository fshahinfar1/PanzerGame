# Farbod Shahinfar
# 8/10/95
# panzer game
# panzer object
from __future__ import division
import pygame
import position_class
import collision_tools
import timer_obj
import fire_load
from math import sin, cos, radians
from my_pygame_tools import sgn, KeyboardHandler


class Panzer(object):
    def __init__(self, pos, image, size, clock, room=None):
        # position
        self.position = position_class.Position(pos)  # center of panzer
        self.speed = 0
        self.acceleration = 0
        self.direction = 0
        # image
        self.original_image = image
        self.image = pygame.transform.scale(image, size)
        self.size = size
        self.clock = clock
        # keyboard
        self.keyboard = KeyboardHandler()
        self.keyboard.connect_keys('right', 'left', 'up', 'down', 'space')
        # collision
        self.collision_obj = collision_tools.CollisionCircle(self.position, 27, self, solid=True)
        # fire
        self.flag_ready_fire = True
        self.timer = timer_obj.Timer(1)
        self.room = room
        self.bullets_list = []

    def get_acceleration(self):
        return self.acceleration

    def get_direction(self):
        return self.direction

    def get_speed(self):
        return self.speed

    def set_acceleration(self, value):
        self.acceleration = value

    def set_direction(self, value, rel=False):
        self.image = pygame.transform.scale(self.original_image, self.size)
        if rel:
            self.direction += value
        else:
            self.direction = value
        if self.direction > 360:
            t = self.direction//360
            self.direction -= (t * 360)
        self.image = pygame.transform.rotozoom(self.image, -self.direction, 1)

    def set_speed(self, value, rel=False):
        if rel:
            self.speed += value
        else:
            self.speed = value

    def set_position(self, pos):
        self.position = position_class.Position(pos)
        self.collision_obj.set_position(self.position)

    def add_friction(self):
        if self.acceleration == 0:
            if self.speed != 0:
                if abs(self.speed) < 0.1:
                    self.speed = 0
                else:
                    self.update_speed(-3 * sgn(self.speed))

    def update_speed(self, acceleration):
        speed_limit = 5
        if acceleration == 0:
            return
        if self.speed * sgn(acceleration) < speed_limit:
            self.speed += acceleration * self.clock.get_time() / 1000

    def calculate_directional_position(self, position, speed):
        """
        it calculates a new position which has a distance of size speed from the position
        in direction of this object
        :param position:
        :param speed:
        :return: position_class.Position
        """
        theta = radians(self.direction)
        return position + (speed * cos(theta), speed * sin(theta))

    def update_position(self):
        new_pos = self.calculate_directional_position(self.position, self.speed)
        may_collide_list = collision_tools.get_object_may_collide(self.collision_obj, 100)
        for obj in may_collide_list:
            if obj.is_solid():  # if other obj is solid to collide
                if self.collision_obj.will_collide_with_at(obj, new_pos):
                    print(self.speed)
                    print("will collide at {0} with {1}".format(new_pos, str(obj)))
                    self.set_acceleration(0)
                    self.set_speed(0)
                    return  # Done updating position
        self.position = new_pos
        self.collision_obj.set_position(self.position)

    def fire(self, bullet_type):
        bullet = \
            bullet_type(self.calculate_directional_position(self.position, 28+abs(self.speed)), self.direction,\
                        speed=10, room=self.room)
        return bullet

    def draw(self, screen):
        #
        self.update_speed(self.acceleration)
        self.update_position()
        self.add_friction()
        #draw
        left_top_corner = [0, 0]
        left_top_corner[0] = self.position[0] - self.image.get_size()[0]/2
        left_top_corner[1] = self.position[1] - self.image.get_size()[1]/2
        # pygame.draw.circle(screen, (0, 0, 0), self.collision_obj.position.int_cordinates(), self.collision_obj.radius, 0)
        screen.blit(self.image, left_top_corner)

        #pygame.draw.circle(screen, (0, 255, 0), self.collision_obj.position, 2, 0)

    def key_right(self):
        self.set_direction(1, True)

    def key_left(self):
        self.set_direction(-1, True)

    def key_up(self):
        self.acceleration = 4

    def key_down(self):
        self.acceleration = -4

    def key_space(self):
        if self.flag_ready_fire:
            self.flag_ready_fire = False
            self.timer.set_timer()
            return self.fire(fire_load.BouncyFireLoad)

    def loop(self):
        if self.timer.is_time():
            self.flag_ready_fire = True
            print("ready to fire")

