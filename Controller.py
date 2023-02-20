import View
import Model


class Controller:
    player = True
    view = None

    def __init__(self):
        self.field = None
        self.view = View.View(self)
        self.view.run()


    def make_a_move(self, toX, toY):
        if self.field.can_move(toX, toY):
            self.field.move(toX, toY, self.player)
            self.switchPlayer()
            self.field.curr_visited()
            color = self.field.isGoal()
            if color == 'Red':
                self.view.change_screen(2, 'Red')
                print('Red wins')
            elif color == 'Blue':
                self.view.change_screen(2 , 'Blue')
                print('Blue wins')
        else:
            print('Cant move')

    def set_field(self, width, height):
        self.field = Model.Field(width, height)

    def switchPlayer(self):
        ballX = self.field.ball.x
        ballY = self.field.ball.y
        if not self.field.points[ballY][ballX].isVisited:
            if self.player:
                self.player = False
            else:
                self.player = True


if __name__ == '__main__':
    controller = Controller()
