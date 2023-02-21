from enum import Enum


class Point:
    def __init__(self, x, y, color='White'):
        self.x = x
        self.y = y
        self.isVisited = False
        self.isGoal = False
        self.color = color


class Field:
    def __init__(self, width, height, goal_size=3):
        self.width = width
        self.height = height
        self.goal_size = goal_size
        self.points = [[Point(x, y) for x in range(width)] for y in range(height)]
        self.wall_lines = []  # (Point, Point)
        self.red_lines = []
        self.blue_lines = []
        self.ball = Point(width // 2, height // 2)
        self.points[self.ball.y][self.ball.x].isVisited = True
        self.set_walls()

        self.set_goals()

    def isGoal(self):
        return self.points[self.ball.y][self.ball.x].color

    def can_move(self, toX, toY):
        free_neighbours = self.point_free_neighbours(self.points[self.ball.y][self.ball.x])
        if self.points[toY][toX] in free_neighbours:
            return True
        return False

    def point_free_neighbours(self, point):
        neighbours = []
        if point.x - 1 >= 0 and point.y - 1 >= 0 and self.check_lines(point, self.points[point.y - 1][point.x - 1]):
            neighbours.append(self.points[point.y - 1][point.x - 1])
        if point.y - 1 >= 0 and self.check_lines(point, self.points[point.y - 1][point.x]):
            neighbours.append(self.points[point.y - 1][point.x])
        if point.x + 1 < self.width and point.y - 1 >= 0 and self.check_lines(point,
                                                                              self.points[point.y - 1][point.x + 1]):
            neighbours.append(self.points[point.y - 1][point.x + 1])
        if point.x - 1 >= 0 and self.check_lines(point, self.points[point.y][point.x - 1]):
            neighbours.append(self.points[point.y][point.x - 1])
        if point.x + 1 < self.width and self.check_lines(point, self.points[point.y][point.x + 1]):
            neighbours.append(self.points[point.y][point.x + 1])
        if point.x - 1 >= 0 and point.y + 1 < self.height and self.check_lines(point,
                                                                               self.points[point.y + 1][point.x - 1]):
            neighbours.append(self.points[point.y + 1][point.x - 1])
        if point.y + 1 < self.height and self.check_lines(point, self.points[point.y + 1][point.x]):
            neighbours.append(self.points[point.y + 1][point.x])
        if point.x + 1 < self.width and point.y + 1 < self.height and self.check_lines(point, self.points[point.y + 1][
            point.x + 1]):
            neighbours.append(self.points[point.y + 1][point.x + 1])

        return neighbours

    def curr_visited(self):
        self.points[self.ball.y][self.ball.x].isVisited = True

    def isNear(self, x, y):
        neighbours = self.point_free_neighbours(self.points[self.ball.y][self.ball.x])
        return self.points[y][x] in neighbours
    def move(self, toX, toY, player):
        if player:
            self.red_lines.append((self.points[self.ball.y][self.ball.x], self.points[toY][toX]))
        else:
            self.blue_lines.append((self.points[self.ball.y][self.ball.x], self.points[toY][toX]))
        self.ball.x = toX
        self.ball.y = toY

    def no_moves(self):
        return len(self.point_free_neighbours(self.points[self.ball.y][self.ball.x])) == 0

    def set_walls(self):
        for line in self.points:
            for point in line:
                if point.x == 0 or point.x == self.width - 1 or point.y == 0 or point.y == self.height - 1:
                    point.isVisited = True
                    if (point.x == 0 or point.x == self.width - 1) and point.y < self.height - 1:  # drawing walls
                        self.wall_lines.append((point, self.points[point.y + 1][point.x]))
                    if (point.y == 0 or point.y == self.height - 1) and point.x < self.width - 1:
                        self.wall_lines.append((point, self.points[point.y][point.x + 1]))

        not_goal = (self.width - self.goal_size) // 2
        for x in range(1, not_goal + 1):
            self.points[1][x].isVisited = True
            self.points[self.height - 2][x].isVisited = True
            self.points[1][x + not_goal + self.goal_size - 2].isVisited = True
            self.points[self.height - 2][x + not_goal + self.goal_size - 2].isVisited = True
            self.wall_lines.append((self.points[1][x - 1], self.points[1][x]))
            self.wall_lines.append((self.points[self.height - 2][x - 1], self.points[self.height - 2][x]))

            self.wall_lines.append(
                (self.points[1][x + not_goal + self.goal_size - 1], self.points[1][x + not_goal + self.goal_size - 2]))
            self.wall_lines.append((self.points[self.height - 2][x + not_goal + self.goal_size - 1],
                                    self.points[self.height - 2][x + not_goal + self.goal_size - 2]))

            self.wall_lines.append((self.points[1][x], self.points[0][x - 1]))
            self.wall_lines.append((self.points[1][x - 1], self.points[0][x]))
            self.wall_lines.append((self.points[1][x], self.points[0][x]))

            self.wall_lines.append(
                (self.points[1][x + not_goal + self.goal_size - 1],
                 self.points[0][x + not_goal + self.goal_size - 2]))
            self.wall_lines.append(
                (self.points[1][x + not_goal + self.goal_size - 2],
                 self.points[0][x + not_goal + self.goal_size - 1]))
            self.wall_lines.append(
                (self.points[1][x + not_goal + self.goal_size - 2],
                 self.points[0][x + not_goal + self.goal_size - 2]))

            self.wall_lines.append((self.points[self.height - 2][x], self.points[self.height - 1][x - 1]))
            self.wall_lines.append((self.points[self.height - 2][x - 1], self.points[self.height - 1][x]))
            self.wall_lines.append((self.points[self.height - 2][x], self.points[self.height - 1][x]))

            self.wall_lines.append(
                (self.points[self.height - 2][x + not_goal + self.goal_size - 1],
                 self.points[self.height - 1][x + not_goal + self.goal_size - 2]))
            self.wall_lines.append(
                (self.points[self.height - 2][x + not_goal + self.goal_size - 2],
                 self.points[self.height - 1][x + not_goal + self.goal_size - 1]))
            self.wall_lines.append(
                (self.points[self.height - 2][x + not_goal + self.goal_size - 2],
                 self.points[self.height - 1][x + not_goal + self.goal_size - 2]))

            for x in range(self.goal_size - 1):
                self.red_lines.append((self.points[0][x + not_goal], self.points[0][x + not_goal + 1]))
                self.blue_lines.append(
                    (self.points[self.height - 1][x + not_goal], self.points[self.height - 1][x + not_goal + 1]))

    def check_lines(self, fromPoint, toPoint):
        inWalls = (fromPoint, toPoint) in self.wall_lines or (toPoint, fromPoint) in self.wall_lines
        inRed = (fromPoint, toPoint) in self.red_lines or (toPoint, fromPoint) in self.red_lines
        inBlue = (fromPoint, toPoint) in self.blue_lines or (toPoint, fromPoint) in self.blue_lines
        return not (inWalls or inBlue or inRed)

    def set_goals(self):
        not_goal = (self.width - self.goal_size) // 2
        for x in range(self.goal_size):
            self.points[0][x + not_goal].isGoal = True
            self.points[0][x + not_goal].color = 'Red'
            self.points[self.height - 1][x + not_goal].isGoal = True
            self.points[self.height - 1][x + not_goal].color = 'Blue'
