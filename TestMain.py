# farbod shahinfar
# test main

import sys
import pygame
import test_room


pygame.init()
clock = pygame.time.Clock()
room = test_room.TestRoom(clock)
states = room.is_end()



def main(game, game_state):
    """
     Here is Main Main loop of the game and it's the most simplest
     place of the job.
     we have a game that is current room which we are in
     and this room should process_events, run_logic and draw_frame
     then if the game state of continues changed
     we do what we have to do stop the game or go to next room
    :param game: room
    :param game_state: start states
    :return: game_state (flag_End(bool), flag_GameOver(bool))
    """
    while not game_state[0]:
        game.process_events()
        game.run_logic()
        game.draw_frame()
        game_state = game.is_end()
        clock.tick(60)
    return game_state

states = main(room, states)

if states[1]:  # if flag_GameOver is True Then it's The End
    pygame.quit()
    sys.exit()
