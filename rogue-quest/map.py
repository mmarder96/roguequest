import libtcodpy as tcod

from tile import Tile

class Rectangle(object):

    """Rectangle helper class used tod efine a room"""

    def __init__(self, x, y, w, h):
        """Initialize a rectangel

        :x: top left corner x
        :y: top left corner y
        :w: width
        :h: width

        """
        self._x1 = x
        self._y1 = y
        self._x2 = x + w
        self._y2 = y + h

    def is_intersecting(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    @property
    def x1(self):
        return self._x1

    @property
    def y1(self):
        return self._y1

    @property
    def x2(self):
        return self._x2
    
    @property
    def y2(self):
        return self._y2

    def __str__(self):
        return \
            """
            Center: {}, {}
            Width: {}
            Height: {}
            """.format(self.center[0], self.center[1], self.x2 - self.x1, self.y2 - self.y1)

class Map(object):

    """Represents the map of the game."""

    def __init__(self, con, width, height, max_room_size, min_room_size, max_rooms,
            torch_radius, light_walls, algorithm):
        """Initialize the map to a width and height

        :width: width of the map
        :height: height of the map

        """
        self.dark_wall = tcod.Color(0, 0, 100)
        self.light_wall = tcod.Color(130, 110, 50)
        self.dark_ground = tcod.Color(50, 50, 150)
        self.light_ground = tcod.Color(200, 180, 50)

        self._torch_radius = torch_radius
        self._light_walls = light_walls
        self._algorithm = algorithm
        
        self._max_room_size = max_room_size
        self._min_room_size = min_room_size
        self._max_rooms = max_rooms

        self._width = width
        self._height = height
        self._map = [ [Tile(True) 
            for y in range(self._height) ]
                for x in range(self._width) ]

        self._fov_map = tcod.map_new(width, height)

        self._con = con


    def set_blocking(self, blocking, x, y):
        self._map[x][y].blocking = blocking

    def is_blocking(self, x, y):
        return self._map[x][y].blocking

    def set_sight(self, block_sight, x, y):
        self._map[x][y].block_sight = sight

    def set_tile(self, blocking, block_sight, x, y):
        self._map[x][y].blocking = blocking
        self._map[x][y].block_sight = block_sight

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self._map[x][y].set_tile(False, False)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self._map[x][y].set_tile(False, False)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self._map[x][y].set_tile(False, False)

    def recalculate_fov(self, player_x, player_y):
        tcod.map_compute_fov(self._fov_map, player_x, player_y,
                self._torch_radius, self._light_walls, self._algorithm)

    def generate_dungeon(self):
        """
        Generates the dungeon from the parameters specified

        process is mostly random and only checks for intersections of rooms
        intersection of hallways is allowed.
        """
        rooms = []
        num_rooms = 0
        
        for r in range(self._max_rooms):
            # Random width and height
            w = tcod.random_get_int(0, self._min_room_size, self._max_room_size)
            h = tcod.random_get_int(0, self._min_room_size, self._max_room_size)
            # Random position
            x = tcod.random_get_int(0, 0, self._width - w - 1)
            y = tcod.random_get_int(0, 0, self._height - h - 1)
            
            new_room = Rectangle(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.is_intersecting(other_room):
                    failed = True
                    break
            if not failed:
                # room is valid
                self.create_room(new_room)
                new_x, new_y = new_room.center()
                
                if num_rooms > 0:
                    prev_x, prev_y = rooms[num_rooms - 1].center()

                    if tcod.random_get_int(0, 0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                rooms.append(new_room)
                num_rooms += 1


        for y in range(self._height):
            for x in range(self._width):
                tcod.map_set_properties(self._fov_map, x, y, \
                        not self._map[x][y].block_sight, not self._map[x][y].blocking)
        return rooms[0].center()

    def render(self, recalculate_fov, player_x, player_y):
        """
        Renders the dungeon map and recalculates the fov
        if necessary
        """
        if recalculate_fov:
            self.recalculate_fov(player_x, player_y)

        for y in range(self._height):
            for x in range(self._width):
                visible = tcod.map_is_in_fov(self._fov_map, x, y)
                wall = self._map[x][y].block_sight
                if not visible:
                    # if the tile hasnt been explored leave it black
                    if self._map[x][y].explored:
                        if wall:
                            tcod.console_put_char_ex(self._con, x, y, '#',
                                    self.dark_wall, tcod.black)
                        else:
                            tcod.console_put_char_ex(self._con, x, y, '.',
                                    self.dark_ground, tcod.black)
                else:
                    if wall:
                        tcod.console_put_char_ex(self._con, x, y, '#',
                                self.light_wall, tcod.black)
                    else:
                        tcod.console_put_char_ex(self._con, x, y, '.',
                                self.light_ground, tcod.black)
                    # if the tile is in vision and hasnt been seen before mark it explored
                    self._map[x][y].explored = True


