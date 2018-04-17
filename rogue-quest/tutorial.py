from object import Object
from map import Map

import os
import json
import libtcodpy as tcod

def handle_keys():
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

def handle_movement(game_map, player):
    # HANDLE MOVEMENT -------------------------------------------
    # if the player has moved we need to recalcualte the fov
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

    return fov_recompute

def read_config(path):
    """
    Reads the game config into a dictionary
    """
    with open(path) as json_config:
        data = json.load(json_config)
    return data

def init_engine(font, screen_width, screen_height, frame_rate, title):
    """
    Initialize the game engine and create the root console
    """
    tile_set = os.path.join('../data', 'fonts', font)
    tcod.console_set_custom_font(tile_set, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, title, False)
    tcod.sys_set_fps(frame_rate)

    return tcod.console_new(screen_width, screen_height)

def main():

    # Read in the configuration file
    config = read_config('config.json')
    
    # Initialize the root console
    con = init_engine(config['engine']['font'], config['screen']['width'],
        config['screen']['height'], config['engine']['frame_rate'],
        config['engine']['title'])

    # Create the game map
    game_map = Map( con,
            config['map']['width'], config['map']['height'], 
            config['map']['max_room_size'], config['map']['min_room_size'],
            config['map']['max_rooms'],
            config['vision']['torch_radius'], config['vision']['light_walls'],
            config['vision']['algorithm']
        )
    
    # generate the dungeon and get a location inside the first room
    # and instatiate the player object
    player_start = game_map.generate_dungeon()
    player = Object( con, player_start[0], player_start[1], '@', tcod.white )

    # add the player to the list of renderable objects
    objects = [player]

    recalculate_fov = True
    # Main game loop 
    while not tcod.console_is_window_closed():
        # set text colr
        tcod.console_set_default_foreground(0, tcod.white)
        # put objects
        game_map.render(recalculate_fov, player.x, player.y)
        for obj in objects:
            obj.draw()
    
        # blit consoles to root
        tcod.console_blit(con, 0, 0, config['screen']['width'], config['screen']['height'], 0, 0, 0)
        # refresh the screen
        tcod.console_flush()
        
        # update keyboard input and remove object char
        for obj in objects:
            obj.clear()
        recalculate_fov = handle_movement(game_map, player)

        exit = handle_keys()
        if exit:
            break

if __name__ == "__main__":
    main()


















