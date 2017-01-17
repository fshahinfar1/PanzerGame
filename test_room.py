# Farbod Shahinfar
# 25/10/95
# Test Room
import pygame
import room_obj
import panzer_obj
import player_class
import map_obj
import key_map_sets
import fire_load
import collectable_object
import my_pygame_tools as tools
cp = tools.Colors()


class TestRoom(room_obj.Room):
    def __init__(self, clock):
        room_obj.Room.__init__(self, 'Test', clock=clock)  # create room with name Test
        # init_player
        self.Players = []
        self.init_player()
        # walls
        self.wall_list = map_obj.get_walls("maps/map01.txt")
        # collectable objects
        collectable_object.LaserObject((250, 60))
        collectable_object.TirKoloftObject((60, 250))
        self.mouse = tools.Mouse()

    def init_player(self):
        panzer_img = pygame.image.load("images/panzer.png")
        # player1
        key_set = key_map_sets.KeySetOne()
        panzer1 = panzer_obj.Panzer((60, 60), panzer_img, (54, 54), self.clock, self)
        player1 = player_class.Player(key_set.keyboard, panzer1, key_set.key_map)
        self.Players.append(player1)
        # # player2
        # key_set = key_map_sets.JoystickSetOne(0)
        # panzer2 = panzer_obj.Panzer((60, 400), panzer_img, (54, 54), self.clock, self)
        # # fixme key_set.key_map is not usable here
        # player2 = player_class.Player(key_set.joystick, panzer2, key_set.key_map)
        # self.Players.append(player2)

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                for player in self.Players:
                    if player.controller_type() == "keyboard":
                        player.get_controller().get_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def run_logic(self):
        for player in self.Players:
            if player.controller_type() == "keyboard":
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
                    player.get_panzer().key_space()

            elif player.controller_type() == "joystick":
                # turn
                hat_num = player.get_controller().get_hat(0)
                if hat_num[0] == 1:
                    player.get_panzer().key_right()
                elif hat_num[0] == -1:
                    player.get_panzer().key_left()
                # forward / backward
                if hat_num[1] == 1 or player.get_controller().get_button(5):
                    player.get_panzer().key_up()
                elif hat_num[1] == -1 or player.get_controller().get_button(4):
                    player.get_panzer().key_down()
                else:
                    player.get_panzer().set_acceleration(0)
                # fire
                if player.get_controller().get_button(2):
                    player.get_panzer().key_space()

        # mouse
        if self.mouse.is_btn_pressed(1):
            print('left_btn_pressed')
        if self.mouse.is_btn_pressed(2):
            print('right_btn_pressed')

        # object loop
        [player.get_panzer().loop() for player in self.Players]
        [load.loop() for load in fire_load.FireLoadObjectsList]

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        [wall.draw(self.screen) for wall in self.wall_list]  # draw walls
        [obj.draw(self.screen) for obj in collectable_object.object_list]  # draw collectable objects
        [player.get_panzer().draw(self.screen) for player in self.Players]  # draw tanks
        [load.draw(self.screen) for load in fire_load.FireLoadObjectsList]  # draw bullets
        pygame.display.update()  # update display
