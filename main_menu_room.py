# Farbod Shahinfar
# 10/10/95
# main menu room
import pygame
import room_obj
import menu_list_obj
import label_obj
import test_room
import key_map_sets
import panzer_obj
import player_class
from my_pygame_tools import Colors, Mouse
pygame.init()
cp = Colors()


class MainMenuRoom(room_obj.Room):
    def __init__(self, clock):
        room_obj.Room.__init__(self, 'main_menu', clock=clock)  # Create a room object with name main_menu
        self.menu = menu_list_obj.Menu((100, 100))  # Create a menu object
        self.init_label()  # Add labels to menu
        self.mouse = Mouse()
        self.init_player()

    def init_player(self):
        # player1
        key_set = key_map_sets.KeySetOne()
        player_class.Player(key_set.keyboard, key_set.key_map, "player1")
        # self.Players.append(player1)
        key_set = key_map_sets.KeySetThree()
        player_class.Player(key_set.keyboard, key_set.key_map, "player2")
        # self.Players.append(player2)
        # # player2
        # key_set = key_map_sets.JoystickSetOne(0)
        # panzer2 = panzer_obj.Panzer((60, 400), panzer_img, (54, 54), self.clock, self)
        # # fixme key_set.key_map is not usable here
        # player2 = player_class.Player(key_set.joystick, panzer2, key_set.key_map)
        # self.Players.append(player2)

    def destroy(self):
        del self.menu
        del self.mouse
        room_obj.Room.destroy(self)

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
            index = self.menu.mouse_on_index(self.mouse.get_pos())
            if index is not None:
                print(index)
                if index == 0:
                    room = test_room.TestRoom(self.clock, "maps/map01.txt")
                    self.set_next_room(room)
                    self.goto_next_room()
                    return
                elif index == 4:
                    self.quit_game()

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        self.menu.draw(self.screen)
        pygame.display.flip()  # update display
