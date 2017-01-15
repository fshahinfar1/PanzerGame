# Farbod Shahinfar
# 25/10/95
# panzer game
# panzer object
from __future__ import division
import pygame
import position_class
import collision_tools
import timer_obj
import fire_load
import collectable_object
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
        # collision
        self.collision_obj = collision_tools.CollisionCircle(self.position, 27, self, solid=True)
        # fire
        self.flag_ready_fire = True
        self.timer = timer_obj.Timer(1)  # reload timer
        self.room = room
        self.bullet_type = fire_load.BouncyFireLoad
        # laser
        # self.laser = fire_load.Laser(self.calculate_directional_position(self.position, 28 + abs(self.speed)), self.direction)

    def get_position(self):
        return self.position

    def get_collision_obj(self):
        return self.collision_obj

    def get_acceleration(self):
        return self.acceleration

    def get_direction(self):
        return self.direction

    def get_speed(self):
        return self.speed

    def set_bullet_type(self, value):
        self.bullet_type = value

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
        if self.speed == 0:
            return
        new_pos = self.calculate_directional_position(self.position, self.speed)
        collide_object = collision_tools.is_colliding(self.collision_obj, new_pos, self.collision_obj)
        if collide_object is not None:
            if collide_object.is_solid():
                print(self.speed)
                print("will collide at {0} with {1}".format(new_pos, str(collide_object)))
                self.set_acceleration(0)
                self.set_speed(0)
                return  # Done updating position
            elif isinstance(collide_object.get_parent(), collectable_object.CollectableObject):
                collide_object.get_parent().collided_with(self)
        self.position = new_pos
        self.collision_obj.set_position(self.position)

    def fire(self, bullet_type):
        if bullet_type == fire_load.BouncyFireLoad:
            bullet_type(self.calculate_directional_position(self.position, 28+abs(self.speed)), self.direction,\
                        speed=8, room=self.room)
        elif bullet_type == fire_load.Laser:
            self.laser.fire(self.room)
            self.bullet_type = fire_load.BouncyFireLoad

    def draw(self, screen):
        #draw
        left_top_corner = [0, 0]
        left_top_corner[0] = self.position[0] - self.image.get_size()[0]/2
        left_top_corner[1] = self.position[1] - self.image.get_size()[1]/2
        # pygame.draw.circle(screen, (0, 0, 0), self.collision_obj.position.int_cordinates(), self.collision_obj.radius, 0)
        # pygame.draw.circle(screen, (0, 255, 0), self.collision_obj.position.int_cordinates(), 2, 0)
        screen.blit(self.image, left_top_corner)

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
            self.fire(self.bullet_type)

    def key_l(self):
        if self.flag_ready_fire:
            self.flag_ready_fire = False
            self.timer.set_timer()
            return self.fire(fire_load.Laser)

    def loop(self):
        self.update_speed(self.acceleration)
        self.update_position()
        self.add_friction()
        if self.timer.is_time():
            self.flag_ready_fire = True
            print("ready to fire")
        if self.bullet_type is fire_load.Laser:
            if self.laser.fire_state == 'Aim':
                self.laser.set_position(self.calculate_directional_position(self.position, 28 + abs(self.speed)),
                                        update=False)  ###
                self.laser.set_direction(self.direction, update=False)  ###
                self.laser.update()

