from enum import Enum, auto
import chunks as ch

class Direction(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

def rot_clockwise(direction):
    new_direction = (direction + 1) % 4
    return Direction(new_direction)

def rot_contraclockwise(direction):
    new_direction = (direction - 1) % 4
    return Direction(new_direction)


class Ant:
    def __init__(self, cors, direction):
        self.cors = [*cors]
        self.direction = direction

    def step(self):
        if self.direction == Direction.LEFT:
            self.cors[0] -= 1
        elif self.directions == Direction.UP:
            self.cors[1] += 1
        elif self.directions == Direction.RIGHT:
            self.cors[0] += 1
        elif self.directions == Direction.DOWN:
            self.cors[1] -= 1

    def rotate(self, color):
        if color == 1:
            self.direction = rot_clockwise(self.direction)
        else:
            self.direction = rot_contraclockwise(self.direction)

    def repaint(self, color):
        new_color = 0 if color == 1 else 1
        return new_color

class Game:
    def __init__(self):
        self.field = ch.Field()
        self.ants = []


    def add_ant(self, ant):
        self.ants.append(ant)

    def simulate(self, steps):
        for _ in range(steps):
            for i in range(len(self.ants)):
                color = self.field[self.ants[i].cors]

                self.ants[i].rotate(color)
                self.ants[i].step(color)

                self.field[self.ants[i]] = self.ants[i].repaint(color)


    def _min_ant_dist(self):
        if len(self.ants) <= 1:
            return 10**9

        min_ = Game._manhattan_distance(self.ants[0], self.ants[1])

        for i in range(len(self.ants)):
            for j in range(i, len(self.ants)):
                dist = Game._manhattan_distance(self.ants[i],
                                                self.ants[j])
                if dist < min_:
                    min_ = dist

        return min_

    @classmethod
    def _manhattan_distance(cors1, cors2):
        x1, y1 = cors1
        x2, y2 = cors2

        return abs(x1 - x2) + abs(y1 - y2)
