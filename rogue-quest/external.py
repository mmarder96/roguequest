import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import libtcodpy as tcod

# set screen width and height SCREEN_WIDTH = 80
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
# limit fps ( affects speed of game )
LIMIT_FPS = 20

# Map dimensions
MAP_WIDTH = 80
MAP_HEIGHT = 45

# Room dimension
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Vision System
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

# set custom font and import into console
__font = os.path.join('../data', 'fonts', 'arial12x12.png')
tcod.console_set_custom_font(__font, tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD)

# initialize the root console with static parameters
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Hello World', False)
tcod.sys_set_fps(LIMIT_FPS)

# initialize offscreen consoles
con = tcod.console_new( SCREEN_WIDTH, SCREEN_HEIGHT )
