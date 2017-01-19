# Farbod Shahinfar
# 26/10/95
# Panzer Game
import pygame
import position_class
import collision_tools
import fire_load
object_list = []


class CollectableObject(object):
    def __init__(self, img, pos):
        self.position = position_class.Position(pos)
        self.size = img.get_rect().size
        self.image = img
        self.collision_object =\
            collision_tools.CollisionFixRectangle(self.get_left_corner(), self.size[0], self.size[1], self)
        object_list.append(self)

    def destroy(self):
        del self.position
        del self.size
        del self.image
        self.collision_object.destroy()
        del self.collision_object
        object_list.remove(self)

    def get_size(self):
        return self.size

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def get_left_corner(self):
        return self.position - position_class.Position(self.size)/2

    def get_position(self):
        return self.position

    def is_colliding_with(self, other):
        return self.collision_object.is_colliding_with(other)

    def collided_with(self, other):
        self.destroy()

    def draw(self, screen):
        screen.blit(self.image, self.get_left_corner())


class TirKoloftObject(CollectableObject):
    def __init__(self, pos):
        img = pygame.image.load("images/laser.png").convert_alpha()
        img = pygame.transform.scale(img, (16, 16))
        CollectableObject.__init__(self, img, pos)

    def collided_with(self, other):
        other.set_bullet_type(fire_load.TirKoloft)
        self.destroy()


class LaserObject(CollectableObject):

    def __init__(self, pos):
        img = pygame.image.load("images/laser.png").convert_alpha()
        img = pygame.transform.scale(img, (16, 16))
        CollectableObject.__init__(self, img, pos)

    def collided_with(self, other):
        self.destroy()
        other.set_bullet_type(fire_load.LaserBullet)
        other.Gun = fire_load.LaserGun(other.calculate_directional_position(other.position, 28 + abs(other.speed)), other.direction, other)


def clear():
    object_list.clear()
