
class Tile(object):

    """A tile of the map and its properties"""

    def __init__(self, blocking, block_sight = None):
        self._blocking = blocking
        self._block_sight = blocking if block_sight is None else block_sight
        self._explored = False
    
    @property
    def blocking(self):
        return self._blocking
    
    @property
    def block_sight(self):
        return self._blocking
    
    @property
    def explored(self):
        return self._explored

    @blocking.setter
    def blocking(self, value):
        self._blocking = value

    @block_sight.setter
    def block_sight(self, value):
        self._block_sight = value
    
    @explored.setter
    def explored(self, value):
        self._explored = value

    def set_tile(self, blocking, block_sight):
        self._blocking = blocking
        self._block_sight = block_sight
       
