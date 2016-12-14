# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration

import sys
import time
import Queue
from matplotlib import animation
import matplotlib.pyplot as plt
import pickle

# Contains every car-object of the board
car_objects = []

class Board(object):
    def __init__(self, width, height):
        """
        Initializes the board with right dimensions and putting the cars in it
        """
        self.height = height
        self.width = width

        # Obtaining a 2D board
        config = [[0 for x in xrange(size)] for x in xrange(size)]

        # Setting the cars onto the board
        count = 1
        for cars in car_objects:
            if type(cars) is HorCar:
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    config[size - 1 - y][x + i] = count
            else:
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    config[size - 1 -(y + i)][x] = count
            count += 1

        # Setting the board into object
        self.config = config

    def isPositionOnBoard(self, x, y):
        """
        Determines if a car is still on the board after a move has done
        """
        # Returns True if car on board, False otherwise
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def getboard(self, car, step, qboard):
        """
        Makes a partial copied board of qboard
        """
        # Data of car object
        x = car.startx
        y = car.starty
        length = car.length
        index = car.index

        config_copy = qboard[:]
        if type(car) is VerCar:

            # Copies all the rows in vertical direction
            for i in xrange(length):
                config_copy[size -1 -(y + i)] = qboard[size -1 -(y + i)][:]

            # Now index can be altered without altering qboard
            for i in xrange(length):
                config_copy[size -1 -(y + i)][x] = index

            # If the car moves up, first element should be 0
            if step == 1:
                config_copy[size -1 - (y - step)] = qboard[size -1 - (y - step)][:]
                config_copy[size -1 - (y - step)][x] = 0

            # If the car moves down, last element should be 0
            else:
                config_copy[size -1 - (y + length)] = qboard[size -1 - (y + length)][:]
                config_copy[size -1 - (y + length)][x] = 0
        else:
            # Copies whole row of the car to be moved
            config_copy[size -1 - y] = qboard[size -1 - y][:]

            # Now index can be altered without altering qboard
            for i in xrange(length):
                config_copy[size -1 - y][x + i] = index

            # If the car moves right, first element should be 0
            if step == 1:
                config_copy[size -1 - y][x - step] = 0

            # If the car moves left, last element should be 0
            else:
                config_copy[size -1 - y][x + length] = 0

        return config_copy

    def update_hor(self, car, x, y, step):
        """
        Determines which values of the board should be changed when a car is
        moved
        """
        # Draws the car in horizontal direction
        for i in xrange(car.length):
            self.config[size -1 - y][x + i] = car.index

        # If the car moves right, first element should be 0
        if step == 1:
            self.config[size -1 - y][x - step] = 0

        # If the car moves left, last element should be 0
        else:
            self.config[size -1 - y][x + car.length] = 0

    def update_ver(self, car, x, y, step):
        """
        Determines which values of the board should be changed when a car is
        moved
        """
        # Draws the car in vertical direction
        for i in xrange(car.length):
            self.config[size -1 -(y + i)][x] = car.index

        # If the car moves up, first element should be 0
        if step == 1:
            self.config[size -1 - (y - step)][x] = 0

        # If the car moves down, last element should be 0
        else:
            self.config[size -1 - (y + car.length)][x] = 0

    def set_board(self, set_config):
        """
        Sets board.config according to set_config, also
        the positions of the car objects alter according to set_config
        """
        # Alter board object
        for j in xrange(size):
            for i in xrange(size):
                self.config[j][i] = set_config[j][i]

        # Alter the positions inside car objects
        check_lis = []
        for i in xrange(size - 1, -1, -1):
            for j in xrange(size):
                if set_config[i][j] > 0 and set_config[i][j] not in check_lis:
                    check_lis.append(set_config[i][j])
                    car_objects[set_config[i][j] - 1].setCarPosition(j,
                                                                size - 1 - i)

class Car(object):
    def __init__(self, index, length, color, x, y):
        """
        Initializes a car with the right values
        """
        self.index = index
        self.length = length
        self.color = color
        self.startx = x
        self.starty = y

    def setCarPosition(self, x, y):
        self.startx = x
        self.starty = y

    def noCar(self, x, y):
        """
        Determine if there is no car blocked in front of the car to be moved
        """
        # Return True if car can be moved, False otherwise
        return board.config[size - 1 - y][x] == 0 or board.config[size - 1 - y][x] == self.index


class HorCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)
        """
        Inherits car class to obtain a horizontal car object
        """

    def updatePosition(self, step):
        """
        Determines if this specific car object can be moved
        """
        new_xstart = self.startx + step
        new_ystart = self.starty

        new_xend = new_xstart + self.length - 1
        new_yend = new_ystart

        if (board.isPositionOnBoard(new_xstart, new_ystart) and
            board.isPositionOnBoard(new_xend, new_yend) and
            self.noCar(new_xstart, new_ystart) and
            self.noCar(new_xend, new_yend)):

            self.setCarPosition(new_xstart, new_ystart)
            board.update_hor(self, new_xstart, new_ystart, step)
            return True

        return False


class VerCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)
        """
        Inherits car class to obtain a vertical car object
        """
    def updatePosition(self, step):
        """
        Determines if this specific car object can be moved
        """
        new_xstart = self.startx
        new_ystart = self.starty + step

        new_xend = new_xstart
        new_yend = new_ystart + self.length - 1

        if (board.isPositionOnBoard(new_xstart, new_ystart) and
            board.isPositionOnBoard(new_xend, new_yend) and
            self.noCar(new_xstart, new_ystart) and
            self.noCar(new_xend, new_yend)):

            self.setCarPosition(new_xstart, new_ystart)

            board.update_ver(self, new_xstart, new_ystart, step)
            return True

        return False

###############################################################################
# Below are all the board configurations to be solved. The first three
# board-functions represents the 6x6 boards, the next three boards represents
# the 9x9 boards and the last function represent the 12x12 board.
# All functions contains car-objects which are appended to car_objects list.
# The arguments of the car-objects are: (index, length, color, x, y)
###############################################################################
def board1():
    car_objects.append(HorCar(1, 2, 'red', 3, 3))
    car_objects.append(VerCar(2, 2, 'brown', 0, 0))
    car_objects.append(HorCar(3, 2, 'blue', 1, 1))
    car_objects.append(HorCar(4, 2, 'green', 4, 0))
    car_objects.append(HorCar(5, 2, 'orange', 4, 2))
    car_objects.append(HorCar(6, 2, 'blue', 3, 5))
    car_objects.append(VerCar(7, 3, 'yellow', 3, 0))
    car_objects.append(VerCar(8, 3, 'purple', 2, 3))
    car_objects.append(VerCar(9, 3, 'brown', 5, 3))

def board2():
    car_objects.append(HorCar(1, 2, 'red', 2, 3))
    car_objects.append(VerCar(2, 2, 'brown', 0, 0))
    car_objects.append(HorCar(3, 2, 'green', 0, 2))
    car_objects.append(HorCar(4, 2, 'blue', 2, 2))
    car_objects.append(VerCar(5, 2, 'pink', 3, 0))
    car_objects.append(HorCar(6, 2, 'orange', 4, 0))
    car_objects.append(HorCar(7, 2, 'yellow', 4, 1))
    car_objects.append(VerCar(8, 2, 'purple', 4, 2))
    car_objects.append(VerCar(9, 3, 'brown', 5, 2))
    car_objects.append(HorCar(10, 2, 'green', 1, 4))
    car_objects.append(HorCar(11, 2, 'blue', 3, 4))
    car_objects.append(HorCar(12, 2, 'yellow', 2, 5))
    car_objects.append(HorCar(13, 2, 'orange', 4, 5))

def board3():
    car_objects.append(HorCar(1, 2, 'red', 0, 3))
    car_objects.append(VerCar(2, 2, 'brown', 0, 0))
    car_objects.append(HorCar(3, 2, 'green', 0, 2))
    car_objects.append(VerCar(4, 2, 'blue', 2, 0))
    car_objects.append(VerCar(5, 2, 'pink', 2, 2))
    car_objects.append(HorCar(6, 2, 'purple', 1, 4))
    car_objects.append(HorCar(7, 2, 'blue', 1, 5))
    car_objects.append(HorCar(8, 2, 'purple', 4, 1))
    car_objects.append(HorCar(9, 2, 'orange', 3, 2))
    car_objects.append(VerCar(10, 2, 'pink', 5, 2))
    car_objects.append(VerCar(11, 2, 'yellow', 3, 3))
    car_objects.append(HorCar(12, 2, 'green', 4, 4))
    car_objects.append(HorCar(13, 3, 'orange', 3, 5))

def board4():
    car_objects.append(HorCar(1, 2, 'red', 1, 4))
    car_objects.append(VerCar(2, 2, 'green', 0, 7))
    car_objects.append(HorCar(3, 3, 'yellow', 1, 8))
    car_objects.append(VerCar(4, 3, 'gray', 5, 6))
    car_objects.append(HorCar(5, 3, 'pink', 6, 7))
    car_objects.append(HorCar(6, 2, 'blue', 0, 5))
    car_objects.append(VerCar(7, 3, 'orange', 3, 5))
    car_objects.append(HorCar(8, 3, 'purple', 5, 5))
    car_objects.append(VerCar(9, 3, 'yellow', 8, 4))
    car_objects.append(VerCar(10, 2, 'pink', 0, 3))
    car_objects.append(VerCar(11, 2, 'green', 3, 3))
    car_objects.append(HorCar(12, 3, 'brown', 5, 3))
    car_objects.append(VerCar(13, 3, 'orange', 8, 1))
    car_objects.append(HorCar(14, 2, 'black', 0, 2))
    car_objects.append(VerCar(15, 2, 'blue', 0, 0))
    car_objects.append(VerCar(16, 3, 'yellow', 2, 1))
    car_objects.append(HorCar(17, 3, 'gray', 1, 0))
    car_objects.append(VerCar(18, 2, 'blue', 3, 1))
    car_objects.append(VerCar(19, 2, 'black', 4, 0))
    car_objects.append(HorCar(20, 2, 'brown', 4, 2))
    car_objects.append(HorCar(21, 2, 'pink', 5, 0))
    car_objects.append(HorCar(22, 2, 'green', 7, 0))

def board5():
    car_objects.append(HorCar(1, 2, 'red', 6, 4))
    car_objects.append(VerCar(2, 2, 'pink', 0, 0))
    car_objects.append(VerCar(3, 2, 'blue', 0, 2))
    car_objects.append(VerCar(4, 2, 'green', 1, 0))
    car_objects.append(HorCar(5, 3, 'yellow', 0, 8))
    car_objects.append(HorCar(6, 2, 'gray', 2, 0))
    car_objects.append(HorCar(7, 2, 'black', 2, 1))
    car_objects.append(VerCar(8, 2, 'orange', 4, 0))
    car_objects.append(HorCar(9, 3, 'gray', 5, 1))
    car_objects.append(VerCar(10, 2, 'pink', 8, 0))
    car_objects.append(VerCar(11, 2, 'orange', 2, 2))
    car_objects.append(HorCar(12, 2, 'brown', 3, 2))
    car_objects.append(VerCar(13, 3, 'purple', 5, 2))
    car_objects.append(HorCar(14, 2, 'green', 6, 2))
    car_objects.append(VerCar(15, 3, 'yellow', 8, 2))
    car_objects.append(HorCar(16, 3, 'blue', 2, 4))
    car_objects.append(HorCar(17, 2, 'gray', 4, 5))
    car_objects.append(VerCar(18, 2, 'pink', 6, 5))
    car_objects.append(HorCar(19, 2, 'black', 7, 5))
    car_objects.append(VerCar(20, 3, 'purple', 3, 6))
    car_objects.append(HorCar(21, 2, 'orange', 4, 6))
    car_objects.append(VerCar(22, 2, 'green', 5, 7))
    car_objects.append(VerCar(23, 2, 'blue', 6, 7))
    car_objects.append(HorCar(24, 2, 'yellow', 7, 7))

def board6():
    car_objects.append(HorCar(1, 2, 'red', 0, 4))
    car_objects.append(VerCar(2, 3, 'purple', 0, 0))
    car_objects.append(HorCar(3, 3, 'yellow', 1, 0))
    car_objects.append(VerCar(4, 3, 'gray', 4, 0))
    car_objects.append(HorCar(5, 2, 'blue', 2, 1))
    car_objects.append(HorCar(6, 2, 'green', 5, 1))
    car_objects.append(VerCar(7, 2, 'orange', 1, 2))
    car_objects.append(HorCar(8, 2, 'black', 2, 2))
    car_objects.append(HorCar(9, 3, 'yellow', 5, 2))
    car_objects.append(VerCar(10, 3, 'yellow', 3, 3))
    car_objects.append(HorCar(11, 2, 'pink', 4, 3))
    car_objects.append(HorCar(12, 2, 'brown', 6, 3))
    car_objects.append(VerCar(13, 2, 'blue', 2, 4))
    car_objects.append(VerCar(14, 2, 'orange', 4, 5))
    car_objects.append(VerCar(15, 2, 'pink', 5, 5))
    car_objects.append(HorCar(16, 3, 'gray', 6, 5))
    car_objects.append(VerCar(17, 2, 'black', 0, 6))
    car_objects.append(HorCar(18, 2, 'green', 2, 6))
    car_objects.append(HorCar(19, 2, 'purple', 7, 6))
    car_objects.append(HorCar(20, 3, 'yellow', 1, 7))
    car_objects.append(VerCar(21, 2, 'green', 4, 7))
    car_objects.append(HorCar(22, 2, 'orange', 5, 7))
    car_objects.append(VerCar(23, 2, 'blue', 7, 7))
    car_objects.append(HorCar(24, 2, 'blue', 0, 8))
    car_objects.append(HorCar(25, 2, 'pink', 2, 8))
    car_objects.append(VerCar(26, 3, 'purple', 8, 1))

def board7():
    car_objects.append(HorCar(1, 2, 'red', 2, 6))
    car_objects.append(HorCar(2, 2, 'green', 1, 0))
    car_objects.append(HorCar(3, 3, 'yellow', 3, 0))
    car_objects.append(VerCar(4, 3, 'gray', 6, 0))
    car_objects.append(VerCar(5, 2, 'blue', 2, 2))
    car_objects.append(HorCar(6, 3, 'yellow', 3, 2))
    car_objects.append(HorCar(7, 2, 'orange', 0, 3))
    car_objects.append(HorCar(8, 3, 'purple', 3, 3))
    car_objects.append(VerCar(9, 3, 'black', 6, 3))
    car_objects.append(HorCar(10, 3, 'yellow', 0, 4))
    car_objects.append(VerCar(11, 2, 'pink', 3, 4))
    car_objects.append(HorCar(12, 2, 'green', 4, 4))
    car_objects.append(HorCar(13, 3, 'brown', 0, 5))
    car_objects.append(VerCar(14, 2, 'orange', 4, 5))
    car_objects.append(VerCar(15, 2, 'pink', 5, 5))
    car_objects.append(VerCar(16, 3, 'purple', 0, 6))
    car_objects.append(VerCar(17, 3, 'yellow', 1, 6))
    car_objects.append(HorCar(18, 3, 'brown', 2, 7))
    car_objects.append(VerCar(19, 2, 'green', 5, 7))
    car_objects.append(VerCar(20, 3, 'yellow', 6, 7))
    car_objects.append(HorCar(21, 3, 'purple', 7, 7))
    car_objects.append(HorCar(22, 2, 'orange', 7, 8))
    car_objects.append(HorCar(23, 2, 'pink', 9, 8))
    car_objects.append(HorCar(24, 3, 'gray', 0, 9))
    car_objects.append(HorCar(25, 2, 'orange', 3, 9))
    car_objects.append(VerCar(26, 2, 'pink', 5, 9))
    car_objects.append(HorCar(27, 2, 'green', 7, 9))
    car_objects.append(VerCar(28, 2, 'orange', 10, 9))
    car_objects.append(VerCar(29, 2, 'blue', 11, 9))
    car_objects.append(VerCar(30, 2, 'green', 0, 10))
    car_objects.append(VerCar(31, 2, 'blue', 6, 10))
    car_objects.append(HorCar(32, 3, 'purple', 7, 11))
    car_objects.append(HorCar(33, 2, 'pink', 10, 11))
    # From here right corner
    car_objects.append(HorCar(34, 2, 'blue', 7, 0))
    car_objects.append(VerCar(35, 2, 'pink', 9, 0))
    car_objects.append(VerCar(36, 3, 'purple', 10, 0))
    car_objects.append(VerCar(37, 2, 'pink', 11, 0))
    car_objects.append(HorCar(38, 2, 'green', 8, 2))
    car_objects.append(VerCar(39, 2, 'black', 11, 2))
    car_objects.append(HorCar(40, 3, 'pink', 7, 3))
    car_objects.append(VerCar(41, 3, 'blue', 7, 4))
    car_objects.append(VerCar(42, 2, 'gray', 9, 4))
    car_objects.append(HorCar(43, 2, 'orange', 10, 4))
    car_objects.append(HorCar(44, 2, 'green', 10, 5))

def win_row(size):
    """
    Simple function to determine the winning row
    """
    # Counting from 0, so -1
    # Unless board is uneven, because the .5 is disregarded
    return size/2 - 1 if size % 2 == 0 else size/2

def won(board):
    """
    Determines if board is the winning configuration
    """
    # Determines winning row
    win = win_row(size)
    row = board[win]

    # Determines position of the red car
    index = 0
    for i in xrange(len(row)):
        if row[i] == 1:
            index = i
            break

    # If there are no cars in front of red -> return True
    return all(row[i] <= 1 for i in range(index, len(row)))

def find_path(graph, end, start, path=[]):
    """
    Finds path to the solution in the archive using recursion
    """
    # Elements are two d lists, the animation function is made for tuples
    if type(start) == list:
        start = tuple([start[i][j] for i in xrange(size) for j in xrange(size)])
    path = [start] + path
    if str(start) == str(end):
        return path
    if not graph.has_key(str(start)):
        return False
    node = graph[str(start)]
    newpath = find_path(graph, end, node, path)
    if newpath:
        return newpath

    return False

def a_star(board):
    """
    A-star function calculates cost by counting cars in front of red car
    and the cars on the blocking cars
    """
    # Obtain the row of red car
    row = board[win_row(size)]

    # Determines position of red car
    for i in xrange(len(row)):
        if row[i] == 1:
            place_of_red = i
            break

    # Count cars in front of red and how many in front of those
    amountCars = 0
    for i in xrange(place_of_red, len(row)):
        if row[i] > 1:

        #    amountCars +=1

            # Difference between start car and winning row
            diff = win_row(size) - car_objects[row[i] - 1].starty
            length = car_objects[row[i] - 1].length
            # Car in front of red
            amountCars += 1
            row_up = board[win_row(size) - length + diff]
            row_down = board[win_row(size) + 1 + diff]
            # Check if car is on top of blocking car
            if win_row(size) - length + diff >= 0 and row_up[i] > 1:
                amountCars += 1
            # Check if car is down on blocking car
            if row_down[i] > 1:
                amountCars += 1

    return amountCars

# List of direction car steps
moves = [-1, 1]

archive = {}
queue_priority = Queue.PriorityQueue()
def archived_as(qboard, car, depth, step):
    """
    Determines if board should be added to archive
    """
    # Get partial copied board
    child = board.getboard(car, step, qboard)

    # Make tuple and string of it to reduce memory size
    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

    if str(tuple_child) not in archive:
        archive[str(tuple_child)] = qboard
        if (won(child)):
            board.set_board(child)
            return (True, child)

        queue_priority.put((a_star(child) + depth, child, depth))
        #queue_priority.put((a_star(child), child, depth))

    return (False, None)

def astar_solve():
    """
    Solves a board using a_star-function listed above
    """
    # Depth of a board
    depth = 0

    # Root is a 2d list, put in queue
    root = [[board.config[j][i] for i in xrange(size)] for j in xrange(size)]
    queue_priority.put((0, root, depth))

    # Make a tuple for first node and put in archive
    root_str = str(tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)]))
    archive[root_str] = root

    while queue_priority.qsize():
        # Get first element for setting board and car objects
        cost, qboard, depth = queue_priority.get()
        board.set_board(qboard)

        # Determine which car can be moved
        for car in car_objects:
            if car.index < 34:
                for move in moves:
                    if car.updatePosition(move):
                        # Determines if child of qboard is in the archive
                        found, child = archived_as(qboard, car, depth + 1, move)
                        # If not, then board is winning config
                        if found:
                            # Return the path when puzzle solved
                            return find_path(archive, root_str, child)

                        car.updatePosition(-move)

archive = {}
queue = Queue.Queue()
def archived(qboard, car, step):
    """
    Determines if board should be added to archive
    """
    # Get partial copied board
    child = board.getboard(car, step, qboard)

    # Make tuple and string of it to reduce memory size
    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

    if str(tuple_child) not in archive:
        archive[str(tuple_child)] = qboard
        if (won(child)):
            board.set_board(child)
            return (True, child)

        queue.put(child)

    return (False, None)

def breadth_solve():
    """
    Solves a board using breadth first
    """
    # Make a copy for the first node and put in queue
    root = [[board.config[j][i] for i in xrange(size)] for j in xrange(size)]
    queue.put(root)

    # Make a tuple for first node and put in archive
    root_str = str(tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)]))
    archive[root_str] = root

    while queue.qsize():
        # Get first element for setting board and car objects
        qboard = queue.get()
        board.set_board(qboard)

        # Determine which car can be moved
        for car in car_objects:
            for move in moves:
                if car.updatePosition(move):
                    # Determines if child of qboard is in the archive
                    found, child = archived(qboard, car, move)
                    # If not, then board is winning config
                    if found:
                        # Return the path when puzzle solved
                        return find_path(archive, root_str, child)

                    car.updatePosition(-move)

def find_path_id(graph, end, start, path=[]):
    """
    Finds path to the solution in the archive using recursion (this function
    is only for iterative deepenings)
    """
    # Elements are two-d list, make tuples of it so we can find the str of tuple
    if type(start) == list:
        start = tuple([start[i][j] for i in xrange(size) for j in xrange(size)])
    path = [start] + path
    if str(start) == str(end):
        return path
    if not graph.has_key(str(start)):
        return False
    node = graph[str(start)][1]
    newpath = find_path_id(graph, end, node, path)
    if newpath:
        return newpath

    return False

archive = {}
stack = []
def archived_id(stackboard, car, step, config_depth):
    """
    Determines if board should be added to archive
    """
    # Get partial copied board
    child = board.getboard(car, step, stackboard)

    # Make tuple and string of it to reduce memory size
    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

    if str(tuple_child) not in archive or archive[str(tuple_child)][0] > config_depth + 1:
        archive[str(tuple_child)] = [config_depth + 1, stackboard]
        if (won(child)):
            board.set_board(child)
            return (True, child)

        stack.append((child, config_depth + 1))

    return (False, None)

def id_solve():
    """
    Solves a board using iterative deepening
    """
    # Make a copy for the first node and put in the  stack
    root = [[board.config[j][i] for i in xrange(size)] for j in xrange(size)]
    root_str = str(tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)]))
    stack.append((root, 0))
    archive[root_str] = [0, root]
    depth = 1

    while len(stack):
        # Get last element for setting board and car objects
        stackboard, config_depth = stack.pop()

        if config_depth <= depth:
            board.set_board(stackboard)
            # Determine which car can be moved
            for car in car_objects:
                for move in moves:
                    if car.updatePosition(move):
                        # Determines if child of qboard is in the archive
                        found, child = archived_id(stackboard, car, move, config_depth)
                        # If not, then board is winning config
                        if found:
                            # Return the path when puzzle solved
                            return find_path_id(archive, root_str, child)
                        car.updatePosition(-move)
        # If the depth is reached, start all over
        if len(stack) == 0:
            stack.append((root, 0))
            archive.clear()
            archive[root_str] = [0, root]
            depth += 1

def rush_hour_animation(animation_list):
    """
    Plot the animation of found path
    """
    # Declare figure, gridlines, and dimensions of axes
    fig = plt.figure(1, facecolor='white')
    plt.rc('grid', linestyle="-", linewidth=1, color='black')
    ax = plt.axes(xlim=(0, size), ylim=(0, size))

    # Append the draw objects with color attribute from car objects
    cars = [plt.plot([], [], 's', c = car.color, ms = 300/size)[0]
                                                        for car in car_objects]

    # Initializes the canvas
    def init():
        for car in cars:
            car.set_data([], [])
        return cars

    # i_time is a variable that increments automatically
    def animate(i_time):

        # Obtain 1d board
        board_1d = animation_list[i_time]

        # Make from 1d board a 2d board
        board = [board_1d[i : i + size] for i in range(0, size*size, size)]

        # This is for maintaining the car positions
        car_positions = [([],[]) for _ in range(len(car_objects))]

        # Loops through the animation board and append the car positions of a
        # specific car to the car_positions list
        for i in range(size):
            for j in range(size):
                car_number = board[i][j]
                if car_number > 0:
                    x, y = car_positions[car_number - 1]
                    x.append(j + 0.5)
                    y.append(size - 1 -i + 0.5)

        # Every car has all his positions which can be set to canvas
        for i in range(len(car_positions)):
            x, y = car_positions[i]
            cars[i].set_data(x, y)

        return cars

    # Calling the main animation function
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                           frames=(len(animation_list)), interval=200,
                           blit=True, repeat = False)

    # Turn off tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.title('Rush hour')
    plt.grid(True)
    plt.show()

# Main function
if __name__ == "__main__":

    # Ensure proper usage
    if len(sys.argv) != 3:
        print ("Usage examples: \n python rush_hour.py breadth board1 \n \
python rush_hour.py astar board2 \n python rush_hour.py id board3 \n \
python rush_hour.py animation board1")
        sys.exit(2)

    start = time.time()
    print "Solving..."

    # Decides which board to solve
    if sys.argv[2] == 'board1':
        size = 6
        board1()
    elif sys.argv[2] == 'board2':
        size = 6
        board2()
    elif sys.argv[2] == 'board3':
        size = 6
        board3()
    elif sys.argv[2] == 'board4':
        size = 9
        board4()
    elif sys.argv[2] == 'board5':
        size = 9
        board5()
    elif sys.argv[2] == 'board6':
        size = 9
        board6()
    elif sys.argv[2] == 'board7':
        size = 12
        board7()

    # Initialize board object
    board = Board(size, size)

    # Decides which algorithm to run
    if sys.argv[1] == 'astar':
        path = astar_solve()
    elif sys.argv[1] == 'breadth':
        path = breadth_solve()
    elif sys.argv[1] == 'id':
        path = id_solve()

    # Just obtain a solution path for animation
    elif sys.argv[1] == 'animation':
        with open('Boards/' + sys.argv[2] + '.txt', 'rb') as f:
            path = pickle.load(f)

    end = time.time()
    print "Time elapsed:", (end - start)
    print "Steps", len(path)
    print "Total configurations", len(archive)

    # comment this out for writing to a file
    # with open('board7.txt', 'wb') as f:
    #      pickle.dump(path, f)
    rush_hour_animation(path)
