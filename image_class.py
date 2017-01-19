# Farbod Shahinfar
# image_class
# 29/10/95
import pygame
import timer_obj
object_list = []


class AnimatedImage(object):
    def __init__(self, img, frame_size, frame_count, frame_rate=0.0625, offset=(0, 0), dist=0, start=True):
        self.frame_count = frame_count  # number of frames
        self.frame_index = 0  # current frame number
        self.images = []
        self.timer = timer_obj.Timer(frame_rate)  # frame rate per second
        self.play = False
        for i in range(self.frame_count):
            rect = pygame.Rect((offset[0]+i*(frame_size[0]+dist), offset[1], frame_size[0], frame_size[1]))
            image = pygame.Surface(frame_size)  # current frame image
            # image = img.subsurface(rect)
            image.blit(img, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            self.images.append(image)
        if start:
            self.start_animation()

        object_list.append(self)

    def __len__(self):
        return self.frame_count

    def destroy(self):
        object_list.remove(self)

    def get_frame_index(self):
        return self.frame_index

    def start_animation(self):
        self.timer.set_timer()
        self.play = True

    def loop(self):
        if self.play:
            if self.timer.is_time():
                if self.frame_index < self.frame_count-1:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                self.timer.set_timer()

    def get_image(self):
        return self.images[self.frame_index]


class Explosion(AnimatedImage):
    def __init__(self, pos):
        img = pygame.image.load("images/x.png").convert_alpha()
        AnimatedImage.__init__(self, img, (48, 48), 16)
        self.pos = pos

    def loop(self):
        if self.play:
            if self.timer.is_time():
                if self.frame_index < self.frame_count-1:
                    self.frame_index += 1
                    self.timer.set_timer()
                else:
                    self.destroy()

    def draw(self, screen):
        self.loop()
        screen.blit(self.get_image(), self.pos)
