import libtcodpy as tcod

class Object(object):

    """
    Generic object class.
    Always represented by a character on screen.
    """

    def __init__(self, con, x, y, char, color):
        self.x = x
        self.y = y
        self._char = char
        self._color = color
        self._con = con

    def move(self, game_map, dx, dy):
        if not game_map.is_blocking(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(self._con, self._color)
        tcod.console_put_char(self._con, self.x, self.y, self._char, tcod.BKGND_NONE)
    
    def clear(self):
        tcod.console_put_char(self._con, self.x, self.y, ' ', tcod.BKGND_NONE)
