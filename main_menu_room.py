# Farbod Shahinfar
# 10/10/95
# main menu room
import pygame
import room_obj
import menu_list_obj
import label_obj
from my_pygame_tools import Colors, Mouse
pygame.init()
cp = Colors()


class MainMenuRoom(room_obj.Room):
    def __init__(self, clock):
        room_obj.Room.__init__(self, 'main_menu', clock=clock)  # Create a room object with name main_menu
        self.menu = menu_list_obj.Menu((100, 100))  # Create a menu object
        self.init_label()  # Add labels to menu
        self.mouse = Mouse()

    def init_label(self):
        pos = (0, 0)
        l1 = label_obj.Label("Single Player", pos, cp.BLACK, click_able=True)
        l2 = label_obj.Label("Multi Player", pos, cp.BLACK, click_able=True)
        l3 = label_obj.Label("Play Online", pos, cp.BLACK, click_able=True)
        l4 = label_obj.Label("Setting", pos, cp.BLACK, click_able=True)
        l5 = label_obj.Label("Quit", pos, cp.BLACK, click_able=True)
        self.menu.add_label(l1, l2, l3, l4, l5)

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
            index, b = self.menu.mouse_on_index(self.mouse.get_pos())
            if b:
                print(index)

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        self.menu.draw(self.screen)
        pygame.display.flip()  # update display
