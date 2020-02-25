import pygame
import random

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x: int or float, y: int or float):
        if (isinstance(x, int) or isinstance(x, float)) and \
           (isinstance(y, int) or isinstance(y, float)):
            self.x = x
            self.y = y
        else:
            raise TypeError(f'Unavailable input with type {x.__class__} and {y.__class__}, '
                            f' both should be int ot float')

    def __add__(self, other: 'Vec2d') -> 'Vec2d':
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        raise TypeError(f'Unavailable operand with type {other.__class__}, '
                        f'should be Vec2d object')

    def __sub__(self, other: 'Vec2d') -> 'Vec2d':
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        raise TypeError(f'Unavailable operand with type {other.__class__}, '
                        f'should be Vec2d object')

    def __mul__(self, k: int or float) -> 'Vec2d':
        if isinstance(k, int) or isinstance(k, float):
            return Vec2d(self.x * k, self.y * k)
        raise TypeError(f'Unavailable operand with type {k.__class__}, '
                        f'should be int or float')

    def __len__(self) -> int:
        return int((self.x * self.x + self.y * self.y)**0.5)

    def int_pair(self) -> tuple:
        return self.x, self.y


class Polyline:
    """
    Class Polyline contains the information about points,
    their speed and line that connects points.
    Able to calculate coordinates and draw points on screen.
    """
    # storage of points in the line contains.
    def __init__(self):
        self.points = []
        self.speeds = []

    # adding point in to the line
    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    # calculation coordinates of base points.
    def set_point(self):
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    # drawing points on screen.
    def draw_points(self, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p.x), int(p.y)), width)


class Knot(Polyline):
    def __init__(self, step, points=None, speeds=None):
        super().__init__()
        self.knots = self.get_knot(steps)
        self.steps = step

    # Initiates calculation of knot of points that smooth the line.
    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.knots = self.get_knot(self.steps)
        print("knots", self.knots)

    def set_points(self):
        super().set_point()
        self.knots = self.get_knot(self.steps)


    @staticmethod
    def _get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha +
                Knot._get_point(points, alpha, deg - 1) * (1 - alpha))

    @staticmethod
    def _get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot._get_point(base_points, i * alpha))
        return res

    # Calculates of knot of points that smooth the line.
    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(Knot._get_points(ptn, count))
        return res

    def draw_points(self, width=3, color=(255, 255, 255)):
        super().draw_points()

        for p_n in range(-1, len(self.knots) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(self.knots[p_n].x),
                              int(self.knots[p_n].y)),
                             (int(self.knots[p_n + 1].x),
                              int(self.knots[p_n + 1].y)),
                             width)
    def restart(self):
        self.speeds = []
        self.points = []
        self.knots = []


def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])
    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
#    import pdb; pdb.set_trace()
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    line = Knot(steps)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_r:
                    line.restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("event positions:", *event.pos)
                line.add_point(
                    Vec2d(*event.pos),
                    Vec2d(random.random() * 2, random.random() * 2)
                )

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        line.draw_points(3, color)

        if not pause:
            line.set_points()

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
