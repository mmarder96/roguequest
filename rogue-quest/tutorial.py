from external import *
from object import Object
from map import Map

import os
import libtcodpy as tcod

def handle_keys(game_map, player):
    """
    Handles all user keyboard input.
    """
    # check if an input has been pressed
    key = tcod.console_check_for_keypress()
    # toggle fullscreen on LCtrl+Enter
    if key.vk == tcod.KEY_ENTER and key.lctrl:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    # exit game on Esc
    elif key.vk == tcod.KEY_ESCAPE:
        return True

    # HANDLE MOVEMENT -------------------------------------------
    fov_recompute = False
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(game_map, 0, -1)
        fov_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(game_map, 0, 1)
        fov_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(game_map, -1, 0)
        fov_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.move(game_map, 1, 0)
        fov_recompute = True

def main():
    game_map = Map(MAP_WIDTH, MAP_HEIGHT)
    player_start = game_map.generate_dungeon()
    player =    Object( player_start[0], player_start[1], '@', tcod.white )
    #  npc =       Object( SCREEN_WIDTH / 2 - 5, SCREEN_HEIGHT / 2, '@', tcod.yellow )
    objects = [player]

    # Main game loop 
    while not tcod.console_is_window_closed():
        # set text colr
        tcod.console_set_default_foreground(0, tcod.white)
        # put objects
        game_map.recalculate_fov(player.x, player.y)
        game_map.render()
        for obj in objects:
            obj.draw()
    
        # blit consoles to root
        tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        # refresh the screen
        tcod.console_flush()
        
        # update keyboard input and remove object char
        for obj in objects:
            obj.clear()
        exit = handle_keys(game_map, player)
        if exit:
            break

if __name__ == "__main__":
    main()


















