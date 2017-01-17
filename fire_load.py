# Farbod Shahinfar
# 25/10/95
# bouncy fire load
import pygame
import position_class
import collision_tools
import wall_obj
import timer_obj
from math import radians, sin, cos
from my_pygame_tools import reflect, calculate_directional_position
from random import randrange
FireLoadObjectsList = []


class BulletBase(object):
    def __init__(self, pos, direction=0, speed=0, image=None, size=None, collision_object=None, t=5, room=None):
        self.size = size
        self.image_original = image
        # todo it is a good idea to create a class able to handle animation and use it instead
        self.image = pygame.transform.scale(self.image_original, self.size)
        self.image = pygame.transform.rotozoom(self.image, direction, 1)
        self.position = position_class.Position(pos)  # current position of obj
        self.speed = speed
        self.direction = direction
        self.collision_obj = collision_object
        # todo Do I really need to give the room to object ??
        self.room = room  # room which this object is in
        self.timer = timer_obj.Timer(t)  # t sec to self destruction
        self.timer.set_timer()  # start of timer is creation time
        FireLoadObjectsList.append(self)  # add self to object list

    def __str__(self):
        return "Bullet"

    def destroy(self):
        self.collision_obj.destroy()
        FireLoadObjectsList.remove(self)
        del self  # does it do anything or not??

    def calculate_new_position(self):
        # move with constant speed
        theta = radians(self.direction)
        return self.position + (self.speed * cos(theta), self.speed * sin(theta))

    def update_position(self):
        self.position = self.calculate_new_position()
        self.collision_obj.set_position(self.position)
        if self.room is not None:
            if self.room.is_out_of_room(self.position):
                self.destroy()

    def loop(self):
        if self.timer.is_time():
            self.destroy()
            return
        # all collision logic of the bullet is here
        self.update_position()
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if isinstance(collide_object.get_parent(), wall_obj.Wall):
                self.position = self.collision_obj.move_to_edge(collide_object, self.direction)
                self.direction = reflect(self.direction, collide_object.get_colliding_surface_angle(self.collision_obj))
            elif collide_object.is_solid():
                self.destroy()
                print('{0} destroy by {1}'.format(self, collide_object))

    def get_left_corner(self):
        return self.position - position_class.Position(self.size)/2

    def draw(self, screen):
        screen.blit(self.image, self.get_left_corner())


class BouncyFireLoad(BulletBase):
    def __init__(self, pos, direction, speed=8, room=None):
        img = pygame.image.load("./images/bouncy_fire_load.png")
        size = (10, 10)
        collision_obj = collision_tools.CollisionCircle(pos, 5, self)
        BulletBase.__init__(self, pos, direction, speed, img, size, collision_obj, 5, room)


class TarKesh(BulletBase):
    def __init__(self, pos, direction, speed=6, room=None):
        img = pygame.image.load("./images/TarKesh.png")
        size = (8, 8)
        collision_obj = collision_tools.CollisionCircle(pos, 4, self)
        BulletBase.__init__(self, pos, direction, speed, img, size, collision_obj, 2, room)

    def loop(self):
        if self.timer.is_time():
            self.destroy()
            return
        # all collision logic of the bullet is here
        self.update_position()
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if collide_object.is_solid():
                self.destroy()
                print('{0} destroy by {1}'.format(self, collide_object))


class TirKoloft(BulletBase):
    def __init__(self, pos, direction, speed=5, room=None):
        img = pygame.image.load("./images/bouncy_fire_load.png")
        size = (16, 16)
        collision_obj = collision_tools.CollisionCircle(pos, 8, self)
        BulletBase.__init__(self, pos, direction, speed, img, size, collision_obj, 5, room)

    def destroy(self):
        for i in range(20):
            direction = randrange(0, 361)
            TarKesh(self.position, direction, room=self.room)
        BulletBase.destroy(self)


class Laser(object):
    def __init__(self, pos, direction):
        self.fire_position = position_class.Position(pos)
        self.direction = direction
        self.fire_direction = direction
        self.collision_object = collision_tools.CollisionPoint(self.fire_position, self)
        self.fire_state = 'Aim'
        self.length = 200
        self.break_points = [pos]
        self.update()
        FireLoadObjectsList.append(self)

    def set_direction(self, value, rel=False, update=True):
        if rel:
            self.direction += value
            self.fire_direction += value
        else:
            self.direction = value
            self.fire_direction = value
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
        d = 10
        while l < self.length:
            self.collision_object.set_position(calculate_directional_position(self.direction, self.collision_object.get_position(), d))
            collide_obj = collision_tools.is_colliding(self.collision_object, self.collision_object.get_position(),
                                                       self.collision_object)
            if collide_obj is not None and isinstance(collide_obj, collision_tools.CollisionFixRectangle):
                pos = position_class.Position(self.collision_object.move_to_edge(collide_obj, self.direction))
                self.break_points.append(pos)
                self.direction = reflect(self.direction, collide_obj.get_colliding_surface_angle(self.collision_object))
            l += d
        self.break_points.append(position_class.Position(self.collision_object.get_position()))

    def fire(self, room):
        self.fire_state = 'Fire'
        LaserBullet(self.fire_position, self.fire_direction, room=room)

    def loop(self):
        if self.fire_state == 'Fire':
            self.set_position(calculate_directional_position(self.fire_direction, self.fire_position, 10))

    def draw(self, screen):
        red = (150, 0, 0)
        green = (0, 200, 0)
        pygame.draw.aalines(screen, red, False, self.break_points, 3)
        for pos in self.break_points:
            pygame.draw.circle(screen, green, pos.int_cordinates(), 2)


class LaserBullet:
    def __init__(self, pos, direction, speed=20, room=None):
        self.size = (16, 8)
        self.image_original = pygame.image.load("./images/laser_bullet.png")
        # todo it is a good idea to create a class able to handle animation and use it instead
        self.image = pygame.transform.scale(self.image_original, self.size)
        self.position = position_class.Position(pos)  # current position of obj
        self.speed = speed  # moving speed
        self.direction = direction  # movement direction
        self.collision_obj = collision_tools.CollisionPoint(self.position, self)
        # todo Do I really need to give the room to object ??
        self.room = room  # room which this object is in
        self.timer = timer_obj.Timer(5)  # 5 sec to self destruction
        self.timer.set_timer()  # start of timer is creation time
        FireLoadObjectsList.append(self)  # add self to object list

    def destroy(self):
        self.collision_obj.destroy()
        FireLoadObjectsList.remove(self)
        del self  # does it do anything or not??


