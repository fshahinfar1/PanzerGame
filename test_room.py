# farbod shahinfar
# 7/10/95
# Test Room
import pygame
import room_obj
import panzer_obj
import wall_obj
import player_class
import collision_tools
import map_obj
import key_map_sets
import my_pygame_tools as tools
cp = tools.Colors()


class TestRoom(room_obj.Room):
    def __init__(self, clock):
        room_obj.Room.__init__(self, 'Test', clock=clock)  # create room with name Test
        # init_player
        self.Players = []
        self.init_player()
        self.wall_list = map_obj.get_walls("maps/map01.txt")
        self.fire_load_list = []
        self.mouse = tools.Mouse()

    def init_player(self):
        panzer_img = pygame.image.load("images/panzer.png")
        # player1
        panzer1 = panzer_obj.Panzer((60, 60), panzer_img, (54, 54), self.clock, self)
        player1 = player_class.Player(key_map_sets.KeySetOne.keyboard, panzer1, key_map_sets.KeySetOne.key_map)
        self.Players.append(player1)
        # player2
        panzer2 = panzer_obj.Panzer((60, 400), panzer_img, (54, 54), self.clock, self)
        player2 = player_class.Player(key_map_sets.KeySetTwo.keyboard, panzer2, key_map_sets.KeySetTwo.key_map)
        self.Players.append(player2)

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                [player.get_controller().get_event(event) for player in self.Players]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def run_logic(self):
        for player in self.Players:
            if isinstance(player.get_controller(), tools.KeyboardHandler):
                # turn
                if player.key_map['rotate_right'].check_hold():
                    player.get_panzer().key_right()
                elif player.key_map['rotate_left'].check_hold():
                    player.get_panzer().key_left()
                # forward / backward
                if player.key_map['forward'].check_hold():
                    player.get_panzer().key_up()
                elif player.key_map['backward'].check_hold():
                    player.get_panzer().key_down()
                else:
                    player.get_panzer().set_acceleration(0)
                # fire
                if player.key_map['fire'].check_hold():
                    load = player.get_panzer().key_space()
                    if load is not None:
                        self.fire_load_list.append(load)
                        load.link_holder(self.fire_load_list)
        # player2
        # turn
        # hat_num = self.Players[1].get_controller().get_hat(0)
        # if hat_num[0] == 1:
        #     self.Players[1].get_panzer().key_right()
        # elif hat_num[0] == -1:
        #     self.Players[1].get_panzer().key_left()
        # # forward / backward
        # if hat_num[1] == 1 or self.Players[1].get_controller().get_button(5):
        #     self.Players[1].get_panzer().key_up()
        # elif hat_num[1] == -1 or self.Players[1].get_controller().get_button(4):
        #     self.Players[1].get_panzer().key_down()
        # else:
        #     self.Players[1].get_panzer().set_acceleration(0)
        # # fire
        # if self.Players[1].get_controller().get_button(2):
        #     load = self.Players[1].get_panzer().key_space()
        #     if load is not None:
        #         self.fire_load_list.append(load)
        #         load.link_holder(self.fire_load_list)
        # mouse
        if self.mouse.is_btn_pressed(1):
            print('left_btn_pressed')
        if self.mouse.is_btn_pressed(2):
            print('right_btn_pressed')

        # object loop
        [player.get_panzer().loop() for player in self.Players]
        [load.loop() for load in self.fire_load_list]
        collision_tools.update_collidable_objects_list_position()

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        [player.get_panzer().draw(self.screen) for player in self.Players]
        [wall.draw(self.screen) for wall in self.wall_list]
        [load.draw(self.screen) for load in self.fire_load_list]
        pygame.display.flip()  # update display
