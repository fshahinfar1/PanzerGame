# farbod shahinfar
# Panzer Game
# room object
# 7/10/95
import pygame


class Room:
    def __init__(self, name, size=(800, 500), clock=None, caption="window"):
        self.Name = name  # Room name
        self.flag_end = False  # represents if room is end
        self.flag_GameOver = False  # Game End (all done quit)
        self.screen_size = size
        self.width, self.height = size
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(caption)
        self.clock = clock

    def get_name(self):
        return self.Name

    def get_width(self):
        return self.height

    def get_height(self):
        return self.width

    def get_size(self):
        return self.screen_size

    def is_end(self):
        return self.flag_end, self.flag_GameOver
    
    def process_events(self):
        # for event in pygame.event.get():
        pass
    
    def run_logic(self):
        pass
    
    def draw_frame(self):
        # self.screen.fill((255,255,255))
        #
        # Draw something
        #
        # pygame.display.flip()
        pass
    
    def get_next_room(self):
        pass

    def is_out_of_room(self, pos):
        if pos[0] > self.width or pos[1] > self.height or pos[0] < 0 or pos[1] < 0:
            return True
        return False
