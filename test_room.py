# Farbod Shahinfar
# 25/10/95
# Test Room
import pygame
import room_obj
import player_class
import wall_obj
import map_obj
import fire_load
import collectable_object
import image_class
import collision_tools
import timer_obj
import my_pygame_tools as tools
from random import randrange
import sys
cp = tools.Colors()


class TestRoom(room_obj.Room):
    def __init__(self, clock, map):
        room_obj.Room.__init__(self, 'Test', clock=clock)  # create room with name Test
        # walls/ collectable objects/ ...
        map_obj.load(map)
        # ready_players_tank
        tank_start_point = map_obj.get_start_points(map)
        for player in player_class.player_list:
            idx = randrange(len(tank_start_point))
            pos = tank_start_point[idx][0]
            dire = tank_start_point[idx][1]
            del tank_start_point[idx]
            player.ready_panzer(pos, dire, self.clock, self)
        self.mouse = tools.Mouse()
        self.timer = timer_obj.Timer(3)  # 3 sec

    def destroy(self):
        room_obj.Room.destroy(self)
        # del self.Players
        del self.mouse
        collectable_object.clear()
        collision_tools.clear()
        fire_load.clear()
        wall_obj.clear()

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.flag_GameOver = True
                self.flag_end = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                for player in player_class.player_list:
                    if not player.killed:
                        if player.controller_type() == "keyboard":
                            player.get_controller().get_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.event_btn_pressed(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse.event_btn_released(event)

    def run_logic(self):
        print(len(collision_tools.collidable_objects))
        if player_class.active_player()< 2:
            self.timer.set_timer()
            if self.timer.is_time():
                self.change_map()
                return
        for player in player_class.player_list:
            if player.killed:
                continue
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
        [player.get_panzer().loop() for player in player_class.player_list if not player.killed]
        [load.loop() for load in fire_load.FireLoadObjectsList]

    def draw_frame(self):
        self.screen.fill(cp.WHITE)  # clear display
        [obj.draw(self.screen) for obj in collectable_object.object_list]  # draw collectable objects
        [player.get_panzer().draw(self.screen) for player in player_class.player_list if not player.killed]  # draw tanks
        [load.draw(self.screen) for load in fire_load.FireLoadObjectsList]  # draw bullets
        [wall.draw(self.screen) for wall in wall_obj.object_list]  # draw walls
        [ani.draw(self.screen) for ani in image_class.object_list]
        k = 0
        for player in player_class.player_list:
            pos = (50+k*120, 450)
            player.draw(self.screen, pos)
            k += 1
        pygame.display.update()  # update display

    def change_map(self):
        print("map_changed")
        self.destroy()
        player_class.activate_all_players()
        self.__init__(self.clock, "maps/map01.txt")

