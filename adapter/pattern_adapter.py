
class System:
    """Class for which we adapt another class"""
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class Light:
    """Class that we want to be adapted"""
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class MappingAdapter:
    """Class adapter"""
    def __init__(self, adaptee):
        self.adaptee = adaptee

    @staticmethod
    def _put_on_map(grid, flag):
        coordinates = []
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == flag:
                    coordinates.append((x, y))

        return coordinates

    def lighten(self, grid):
        dim = (len(grid[0]), len(grid))
        self.adaptee.set_dim(dim)

        lights = self._put_on_map(grid, 1)
        obstacles = self._put_on_map(grid, -1)

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)

        return self.adaptee.generate_lights()
