# farbod shahinfar
# battleShip game
# 18/9/95
# main
import sys
import pygame
import main_menu_room
pygame.init()


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

    game_state = ( flag_end, flag_GameOver )
    """
    while not (game_state[0] or game_state[1]):
        if game.flag_pause:
            continue
        game.draw_frame()
        game.process_events()
        game.run_logic()
        game_state = game.is_end()
        game.clock_tick()
    return game_state

clock = pygame.time.Clock()
room = main_menu_room.MainMenuRoom(clock)
states = room.is_end()
states = main(room, states)  # Start the game

while True:
    if states[1]:  # if flag_GameOver is True Then it's The End
        pygame.quit()
        sys.exit()
    else:  # else it is time to switch the room
        t = room
        room = room.get_next_room()
        states = room.is_end()
        states = main(room, states)
        t.destroy()
