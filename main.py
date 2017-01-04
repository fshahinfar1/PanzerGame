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
    while not game_state[0]:
        game.process_events()
        game.run_logic()
        game.draw_frame()
        game_state = game.is_end()
        clock.tick(60)
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
        pass
        # rooms = ['BoardRoom', 'FightScene']
        # if room.get_name() == rooms[0]:  # if we were in board room so lets grab our plans and go to fight scene
        #     grids = room.grab_grids()  # tuple of two grids
        #     ships = room.grab_ships()  # tuple of two ship_lists
        #     room = fight_scene.Game(ships, grids)
        #     states = room.IsEnd()
        # elif room.get_name() == rooms[1]:
        #     # if we were in fight scene then lets go to board room for better plan for next round
        #     room = board_room.BoardRoom()
        #     states = room.IsEnd()
        # states = main(room, states)  # Lets Go
