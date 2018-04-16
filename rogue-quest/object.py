import libtcodpy as tcod
from external import con

class Object(object):

    """
    Generic object class.
    Always represented by a character on screen.
    """

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, game_map, dx, dy):
        if not game_map.is_blocking(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)
    
    def clear(self):
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)
