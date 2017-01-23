# Panzer Game
# room object
# 7/10/95
import pygame


class Room:
    def __init__(self, screen, name, size=(1024, 800), clock=None, caption="window", next_room=None):
        self.Name = name  # Room name
        self.flag_end = False  # represents if room is end
        self.flag_GameOver = False  # Game End (all done quit)
        self.flag_pause = False
        self.screen_size = self.width, self.height = size
        # self.screen = pygame.display.set_mode(self.screen_size)
        self.screen = screen
        # pygame.display.toggle_fullscreen()
        pygame.display.set_caption(caption)
        self.clock = clock
        self.next_room = next_room

    def __str__(self):
        return "Room: "+self.Name

    def destroy(self):
        # del self.clock
        # del self.screen
        del self.screen_size
        del self.flag_end
        del self.Name
        del self.flag_GameOver
        del self.next_room

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
        pass
    
    def run_logic(self):
        pass
    
    def draw_frame(self):
        pass

    def get_next_room(self):
        return self.next_room

    def set_next_room(self, next_room):
        self.next_room = next_room

    def goto_next_room(self):
        self.flag_end = True

    def quit_game(self):
        self.flag_end = True
        self.flag_GameOver = True

    def is_out_of_room(self, pos):
        if pos[0] > self.width or pos[1] > self.height or pos[0] < 0 or pos[1] < 0:
            return True
        return False

    def clock_tick(self):
        self.clock.tick(60)
