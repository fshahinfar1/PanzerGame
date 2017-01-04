# Farbod Shahinfar
# panzer game
# 10/10/95
# wall object
import pygame
import position_class
import collision_tools
pygame.init()


class Wall(object):
    def __init__(self, image, size, pos, direction=0):
        self.image = pygame.transform.rotozoom(image, direction, 1)
        self.image = pygame.transform.smoothscale(self.image, size)
        self.size = size
        self.direction = direction
        self.pos = position_class.Position(pos)
        self.collision_obj = collision_tools.CollisionFixRectangle(self.pos, size[0], size[1], self)

    def __str__(self):
        return "wall at position {0} with size of {1}; direction = {2}".format(self.pos, self.size, self.direction)

    def draw(self, screen):
        #left_corner = tuple(self.pos - position_class.Position(self.size)/2)
        screen.blit(self.image, tuple(self.pos))
        rect = [self.collision_obj.position[0], self.collision_obj.position[1],\
                self.collision_obj.width, self.collision_obj.height]
        # pygame.draw.rect(screen, (255, 0, 0), rect)
        # pygame.draw.circle(screen, (0, 255, 0), self.collision_obj.position, 2)
        # pygame.draw.circle(screen, (0, 255, 255), self.collision_obj.position + (54,0), 2)




