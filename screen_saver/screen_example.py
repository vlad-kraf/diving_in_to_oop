#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


# =======================================================================================
# Class Vector2D can be a vector and a point
# =======================================================================================


class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x,
                            self.y - other.y)
        raise ValueError('No subtraction for', other.__class__)

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x,
                            self.y + other.y)
        raise ValueError('No addition for', other.__class__)

    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self.x * other, self.y * other)
        raise ValueError('No multiplication for', other.__class__)

    def int_pair(self, other):
        if isinstance(other, Vector2D):
            return other - self
        raise ValueError('No int_pair for', other.__class__)

    def __str__(self):
        return str((self.x, self.y))


# =======================================================================================
# Polyline class
# =======================================================================================


class NotFindingPoint(ValueError):
    pass


class Polyline:

    def __init__(self, points=None, speeds=None, general_speed=1.):
        self.points = points or []
        self.speeds = speeds or []
        self.general_speed = general_speed

    def add_point(self, new_point, new_speed):
        self.points.append(new_point)
        self.speeds.append(new_speed)

    def set_point(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p] * self.general_speed
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vector2D(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vector2D(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color,
                               (int(p.x), int(p.y)), width)


class Knot(Polyline):

    def __init__(self, step, points=None, speeds=None, general_speed=1.):
        super().__init__(points, speeds, general_speed)
        self.steps = step
        self.knots = self.get_knot(step)

    def draw_points(self, width=3, color=(255, 255, 255)):
        super().draw_points()

        for p_n in range(-1, len(self.knots) - 1):
            pygame.draw.line(gameDisplay, color,
                             (int(self.knots[p_n].x),
                              int(self.knots[p_n].y)),
                             (int(self.knots[p_n + 1].x),
                              int(self.knots[p_n + 1].y)),
                             width)

    def set_point(self):
        super().set_point()
        self.knots = self.get_knot(self.steps)

    def add_point(self, new_point, new_speed):
        super().add_point(new_point, new_speed)
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

    def clear(self):
        self.speeds = []
        self.points = []
        self.knots = []

    def _find_point(self, x, y):
        tolerance = 4
        for i in range(len(self.points)):
            if abs(self.points[i].x - x) < tolerance and \
                    abs(self.points[i].y - y) < tolerance:
                return i
        raise NotFindingPoint

    def delete_point(self, x, y):
        try:
            index = self._find_point(x, y)
            self.points.pop(index)
            self.speeds.pop(index)
            self.knots = self.get_knot(self.steps)
        except NotFindingPoint:
            pass


# =======================================================================================
# Ð¤ÑƒÐ½ÐºÑ†Ð¸Ð¸ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸
# =======================================================================================

def draw_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["D", "Delete mode"])
    data.append(["N", "Normal mode"])
    data.append(["1", "Less points (I don't have numpad :( )"])
    data.append(["2", "More points (I don't have numpad :( )"])
    data.append(["3", "Decrease speed"])
    data.append(["4", "Increase speed"])
    data.append(["", ""])
    data.append([str(line.general_speed), "Current speed"])
    data.append([str(line.steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# ÐžÑÐ½Ð¾Ð²Ð½Ð°Ñ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ð°
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyWindow")

    steps = 35
    working = True
    show_help = False
    pause = True
    delete_mod = False

    line = Knot(steps)

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line.clear()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_2:
                    line.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_1:
                    line.steps -= 1 if line.steps > 1 else 0
                if event.key == pygame.K_n:
                    delete_mod = False
                if event.key == pygame.K_d:
                    delete_mod = True
                if event.key == pygame.K_3:
                    line.general_speed -= 5 if line.general_speed >= 5 else 0
                if event.key == pygame.K_4:
                    line.general_speed += 5 if line.general_speed <= 190 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if delete_mod:
                    line.delete_point(*event.pos)
                else:
                    line.add_point(
                        Vector2D(*event.pos),
                        Vector2D(random.random() * 2, random.random() * 2)
                    )

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        line.draw_points(3, color)

        if not pause:
            line.set_point()

        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)