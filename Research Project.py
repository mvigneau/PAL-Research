from graphics import *


class Robot:

    def init(sel, win):
        pt = Point(125,125)
        robot = Circle(pt,5)
        robot.setFill("black")
        robot.draw(win)


def ColonySpace():

    height = 8
    length = 8

    space = [0] * (length * height)

    print(space)

ColonySpace()

def DrawColonySpace(win):

    return 0


def main():

    win = GraphWin("Research Project", 800, 800)

    Colony = Rectangle(Point(100,100), Point(700,700))
    Colony.setFill("lightblue")
    Colony.draw(win)

    height = 8
    length = 8
    
    for i in range(length+1):
        line = Rectangle(Point(100+(600/length*(i)),100), Point(100+(600/length*(i)),700))
        line.draw(win)

    for j in range(height+1):
        line = Rectangle(Point(100, 100+(600/height*(j))), Point(700, 100+(600/height*(j))))
        line.draw(win)

    robot = Robot()
    robot.init(win)

main()
