# Farbod Shahinfar
# 25/10/95
# bouncy fire load
import pygame
import position_class
import collision_tools
import wall_obj
import timer_obj
from math import degrees,radians, sin, cos, atan2
from my_pygame_tools import reflect, calculate_directional_position, distance
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
                return True  # destroy happend
        return False

    def set_direction(self, value):
        self.direction = value
        self.image = pygame.transform.scale(self.image_original, self.size)
        self.image = pygame.transform.rotozoom(self.image, self.direction, 1)

    def loop(self):
        if self.timer.is_time():
            self.destroy()
            return
        # all collision logic of the bullet is here
        if self.update_position():
            return
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if isinstance(collide_object.get_parent(), wall_obj.Wall):
                self.position = self.collision_obj.move_to_edge(collide_object, self.direction)
                self.set_direction(reflect(self.direction, collide_object.get_colliding_surface_angle(self.collision_obj)))
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
        pass

    def draw(self, screen):
        red = (150, 0, 0)
        green = (0, 200, 0)
        pygame.draw.aalines(screen, red, False, self.break_points, 3)
        # for pos in self.break_points:
        #     pygame.draw.circle(screen, green, pos.int_cordinates(), 2)


class LaserBullet(BulletBase):
    def __init__(self, pos, direction, speed=3, room=None):
        size = (2, 2)
        image = pygame.image.load("./images/laser_bullet.png")
        collision_obj = collision_tools.CollisionPoint(pos, self)
        BulletBase.__init__(self, pos, direction, speed, image, size, collision_obj, 500, room)
        self.collision_points = [pos]
        self.length = 100

    def add_collision_point(self, p):
        self.collision_points.append(p)

    def loop(self):
        if self.timer.is_time():
            self.destroy()
            return
        # all collision logic of the bdistance(p, list_temp[0])ullet is here
        if self.update_position():
            return
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if isinstance(collide_object.get_parent(), wall_obj.Wall):
                self.position = self.collision_obj.move_to_edge(collide_object, self.direction)
                self.set_direction(reflect(self.direction, collide_object.get_colliding_surface_angle(self.collision_obj)))
                self.add_collision_point(self.position)
            elif collide_object.is_solid():
                self.destroy()
                print('{0} destroy by {1}'.format(self, collide_object))

    def line_length(self):
        list_temp = self.collision_points + [self.position]
        d = 0
        for i in range(len(list_temp) - 1):
            d += distance(list_temp[i], list_temp[i + 1])
        return d

    def update_collision_points(self):
        list_temp = self.collision_points + [self.position]
        d = self.line_length()
        if d > self.length:
            len_need = d - self.length
            p0 = list_temp[0]
            p1 = list_temp[1]
            dy = p1[1] - p0[1]
            dx = p1[0] - p0[0]
            line_dir = degrees(atan2(dy, dx))
            p = position_class.Position(calculate_directional_position(line_dir, p0, len_need))
            if distance(p, list_temp[1]) < 10 and len(list_temp)>2:
                del self.collision_points[0]
            else:
                self.collision_points[0] = p

    def draw(self, screen):
        blue = (50, 75, 200)
        self.update_collision_points()
        screen.blit(self.image, self.get_left_corner())
        pygame.draw.aalines(screen, blue, False, self.collision_points + [self.position])


class WiredLaserBullet(BulletBase):
    def __init__(self, pos, direction, speed=3, room=None):
        size = (2, 2)
        image = pygame.image.load("./images/laser_bullet.png")
        collision_obj = collision_tools.CollisionPoint(pos, self)
        BulletBase.__init__(self, pos, direction, speed, image, size, collision_obj, 500, room)
        self.collision_points = [pos]
        self.length = 100

    def add_collision_point(self, p):
        self.collision_points.append(p)

    def loop(self):
        if self.timer.is_time():
            self.destroy()
            return
        # all collision logic of the bdistance(p, list_temp[0])ullet is here
        if self.update_position():
            return
        collide_object = collision_tools.is_colliding(self.collision_obj, self.position, self.collision_obj)
        if collide_object is not None:
            if isinstance(collide_object.get_parent(), wall_obj.Wall):
                self.position = self.collision_obj.move_to_edge(collide_object, self.direction)
                self.set_direction(reflect(self.direction, collide_object.get_colliding_surface_angle(self.collision_obj)))
                self.add_collision_point(self.position)
            elif collide_object.is_solid():
                self.destroy()
                print('{0} destroy by {1}'.format(self, collide_object))

    def update_collision_points(self):
        list_temp = self.collision_points + [self.position]
        d = 0
        for i in range(len(list_temp)-1):
            d += distance(list_temp[i], list_temp[i+1])
        if d > self.length:
            len_need = d - self.length
            p0 = list_temp[0]
            p1 = list_temp[1]
            dy = p1[1] - p0[1]
            dx = p1[0] - p0[0]
            line_dir = degrees(atan2(dy, dx))
            p = position_class.Position(calculate_directional_position(line_dir, p0, len_need))
            if len(list_temp)>2:
                del self.collision_points[1]
            self.collision_points[0] = p

    def draw(self, screen):
        blue = (50, 75, 200)
        self.update_collision_points()
        screen.blit(self.image, self.get_left_corner())
        pygame.draw.aalines(screen, blue, False, self.collision_points + [self.position])




