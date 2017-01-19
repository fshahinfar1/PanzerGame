# Farbod Shahinfar
# Panzer Game
# label_obj
# 7/10/95
from __future__ import division
import pygame
import position_class
from my_pygame_tools import is_in_rectangle
pygame.font.init()


class Label:
    def __init__(self, text, pos, color, font=pygame.font.SysFont('serif', 20, True, False), click_able=False):
        self.label_name = text
        self.text_str = text
        self.pos = position_class.Position(pos)
        self.color = color
        self.font = font
        self.render = font.render(self.text_str,True,self.color)
        self.click_able = click_able
        self.background = None
        self.background_size = None

    def __eq__(self, other):
        if isinstance(other, Label):
            if self.label_name == other.label_name:
                return True
        return False

    def __del__(self):
        self.destroy()

    def destroy(self):
        del self.label_name
        del self.text_str
        del self.pos
        del self.color
        del self.font
        del self.render
        del self.click_able
        del self.background
        del self.background_size

    def get_name(self):
        return self.label_name

    def get_size(self):
        return self.render.get_size()
    
    def get_height(self):
        return self.render.get_height()
    
    def get_width(self):
        return self.render.get_width()

    def get_pos(self):
        return self.pos

    def set_name(self, name):
        self.label_name = name

    def set_pos(self, new_pos):
        self.pos = new_pos

    def set_background(self, img):
        self.background = img
        self.background_size = img.get_rect().size()

    def change_text(self,text):
        self.__init__(text,self.pos,self.color,self.font,self.click_able)
    
    def change_color(self,color):
        self.__init__(self.text_str,self.pos,color,self.font,self.click_able)
    
    def change_pos(self,pos):
        self.__init__(self.text_str,pos,self.color,self.font,self.click_able)
    
    def change_clickable(self,f):
        self.__init__(self.text_str,self.pos,self.color,self.font,f)
    
    def is_clickable(self):
        return self.click_able
    
    def is_mouse_on(self):
        mouse_pos = pygame.mouse.get_pos()
        size = self.get_size()
        rect = [self.pos[0]-5, self.pos[1]-5, size[0]+10, size[1]+10]
        if is_in_rectangle(mouse_pos, rect):
            return True
        return False
    
    def draw(self, screen, shadow=False, shadow_color=(0, 0, 0)):
        if self.background is not None:
            pos = self.pos - (self.background_size[0]/2, self.background_size[1]/2)
            screen.blit(self.background, pos)
        if shadow:
            render_shadow = self.font.render(self.text_str, True, shadow_color)
            screen.blit(render_shadow, [self.pos[0]-1, self.pos[1]+1])
        screen.blit(self.render, tuple(self.pos))
