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
