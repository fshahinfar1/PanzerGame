# 10/10/95
# main menu room
import pygame
import room_obj
import menu_list_obj
import label_obj
import setting_reader
import os
from test_room import TestRoom
from multi_room import MultiRoom
from my_pygame_tools import Colors, Mouse
from random import randrange
pygame.init()
cp = Colors()


class MainMenuRoom(room_obj.Room):
    def __init__(self, screen, clock):
        room_obj.Room.__init__(self, screen, 'main_menu', clock=clock, caption="Main Menu")  # Create a room object with name main_menu
        self.menu = menu_list_obj.Menu((100, 100))  # Create a menu object
        self.init_label()  # Add labels to menu
        self.mouse = Mouse()

    def init_player(self):
        setting_reader.init_players("setting/setting.txt")

    def destroy(self):
        del self.menu
        del self.mouse
        room_obj.Room.destroy(self)

    def init_label(self):
        pos = (0, 0)
        l1 = label_obj.Label("Single Player", pos, cp.BLACK, click_able=True)
        l2 = label_obj.Label("Multi Player", pos, cp.BLACK, click_able=True)
        l3 = label_obj.Label("Setting", pos, cp.BLACK, click_able=True)
        l4 = label_obj.Label("Quit", pos, cp.BLACK, click_able=True)
        self.menu.add_label(l1, l2, l3, l4)

    # main loop functions

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def run_logic(self):
        # mouse
        # todo add hover mode to menu and give some animation to it
        # todo for this I should check mouse hover on object
        if self.mouse.is_btn_pressed(1):
            index = self.menu.mouse_on_index(self.mouse.get_pos())
            if index is not None:
                print(index)
                if index == 0:
                    self.init_player()
                    i = randrange(1, 4)
                    room = TestRoom(self.screen, self.clock, "maps/map{0}.txt".format(i))
                    # room = TestRoom(self.screen, self.clock, "maps/map1.txt")
                    self.set_next_room(room)
                    self.goto_next_room()
                    return
                elif index == 1:
                    room = MultiRoom(self.screen, self.clock)
                    self.set_next_room(room)
                    self.goto_next_room()
                    return
                elif index == 2:
                    os.system("python3 setting/setting.py")
                elif index == 3:
                    self.quit_game()

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        self.menu.draw(self.screen)
        pygame.display.flip()  # update display
