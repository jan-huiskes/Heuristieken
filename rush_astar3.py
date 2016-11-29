# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration

import sys
import time
import Queue
from matplotlib import animation
import matplotlib.pyplot as plt

size = 6

# Saving every car object of the board
cars_objects = []

class Board(object):
    def __init__(self, width, height):
        """
        Initializes the board with right dimensions and putting the cars in it
        """
        self.height = height
        self.width = width

        # Obtaining a 2d board
        board_configuration = [[0 for x in xrange(size)] for x in xrange(size)]

        # Putting the cars into the board
        count = 1
        for cars in cars_objects:
            if type(cars) is HorCar:
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    board_configuration[size - 1 - y][x + i] = count
            else:
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    board_configuration[size - 1 -(y + i)][x] = count
            count += 1

        # Setting the board into object
        self.board_configuration = board_configuration

    def isPositionOnBoard(self, x, y):
        """
        Determines if a car is still on the board after a move has done
        """
        # Returns True if car on board, False otherwise
        return x < self.width and x >= 0 and y < self.height and y >= 0

    def getboard(self, car, step, board_from_queue):
        """
        Makes a partial copied board of board_from_queue
        """
        # Data of car object
        x = car.startx
        y = car.starty
        length = car.length
        index = car.index

        board_configuration_copied = board_from_queue[:]
        if type(car) is VerCar:

            # Copies all the rows in vertical direction
            for i in xrange(length):
                board_configuration_copied[size -1 -(y + i)] = board_from_queue[size -1 -(y + i)][:]

            # Now index can be altered without altering board_from_queue
            for i in xrange(length):
                board_configuration_copied[size -1 -(y + i)][x] = index

            # If the car moves up, first element should be 0
            if step == 1:
                board_configuration_copied[size -1 - (y - step)] = board_from_queue[size -1 - (y - step)][:]
                board_configuration_copied[size -1 - (y - step)][x] = 0

            # If the car moves down, last element should be 0
            else:
                board_configuration_copied[size -1 - (y + length)] = board_from_queue[size -1 - (y + length)][:]
                board_configuration_copied[size -1 - (y + length)][x] = 0
        else:
            # Copies whole row of the car to be moved
            board_configuration_copied[size -1 - y] = board_from_queue[size -1 - y][:]

            # Now index can be altered without altering board_from_queue
            for i in xrange(length):
                board_configuration_copied[size -1 - y][x + i] = index

            # If the car moves right, first element should be 0
            if step == 1:
                board_configuration_copied[size -1 - y][x - step] = 0

            # If the car moves left, last element should be 0
            else:
                board_configuration_copied[size -1 - y][x + length] = 0

        return board_configuration_copied

    def update_board_horizontal(self, x, y, length, index, step):
        """
        Determines which values of the board should be changed when a car is moved
        """
        # Draws the car in horizontal direction
        for i in xrange(length):
            self.board_configuration[size -1 - y][x + i] = index

        # If the car moves right, first element should be 0
        if step == 1:
            self.board_configuration[size -1 - y][x - step] = 0

        # If the car moves left, last element should be 0
        else:
            self.board_configuration[size -1 - y][x + length] = 0

    def update_board_vertical(self, x, y, length, index, step):
        """
        Determines which values of the board should be changed when a car is moved
        """

        # Draws the car in vertical direction
        for i in xrange(length):
            self.board_configuration[size -1 -(y + i)][x] = index

        # If the car moves up, first element should be 0
        if step == 1:
            self.board_configuration[size -1 - (y - step)][x] = 0

        # If the car moves down, last element should be 0
        else:
            self.board_configuration[size -1 - (y + length)][x] = 0

    def set_board(self, set_configuration):
        """
        Sets board.board_configuration according to set_configuration, also
        the positions of the car objects alter according to set_configuration
        """

        # Alter board object
        for j in xrange(size):
            for i in xrange(size):
                self.board_configuration[j][i] = set_configuration[j][i]

        # Alter the positions inside car objects
        check_lis = []
        for i in xrange(size - 1, -1, -1):
            for j in xrange(size):
                if set_configuration[i][j] > 0 and set_configuration[i][j] not in check_lis:
                    check_lis.append(set_configuration[i][j])
                    cars_objects[set_configuration[i][j] - 1].setCarPosition(j, size - 1 - i)



class Car(object):
    def __init__(self, index, length, color, x, y):

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
        return board.board_configuration[size - 1 - y][x] == 0 or board.board_configuration[size - 1 - y][x] == self.index


class HorCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)

    def updatePosition(self, step):

        new_xstart = self.startx + step
        new_ystart = self.starty

        new_xend = new_xstart + self.length - 1
        new_yend = new_ystart

        if (board.isPositionOnBoard(new_xstart, new_ystart) and
            board.isPositionOnBoard(new_xend, new_yend) and
            self.noCar(new_xstart, new_ystart) and
            self.noCar(new_xend, new_yend)):

            self.setCarPosition(new_xstart, new_ystart)
            board.update_board_horizontal(new_xstart, new_ystart, self.length, self.index, step)
            return True

        return False


class VerCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)

    def updatePosition(self, step):

        new_xstart = self.startx
        new_ystart = self.starty + step

        new_xend = new_xstart
        new_yend = new_ystart + self.length - 1

        if (board.isPositionOnBoard(new_xstart, new_ystart) and
            board.isPositionOnBoard(new_xend, new_yend) and
            self.noCar(new_xstart, new_ystart) and
            self.noCar(new_xend, new_yend)):

            self.setCarPosition(new_xstart, new_ystart)

            board.update_board_vertical(new_xstart, new_ystart, self.length, self.index, step)
            return True

        return False


##############################################################################
# The first 6x6 board configuration
##############################################################################


# cars_objects.append(HorCar(1, 2, 'red', 3, 3))
# cars_objects.append(VerCar(2, 2, 'brown', 0, 0))
# cars_objects.append(HorCar(3, 2, 'blue', 1, 1))
# cars_objects.append(HorCar(4, 2, 'green', 4, 0))
# cars_objects.append(HorCar(5, 2, 'orange', 4, 2))
# cars_objects.append(HorCar(6, 2, 'blue', 3, 5))
# cars_objects.append(VerCar(7, 3, 'yellow', 3, 0))
# cars_objects.append(VerCar(8, 3, 'purple', 2, 3))
# cars_objects.append(VerCar(9, 3, 'brown', 5, 3))


# ##############################################################################
# # The second 6x6 board configuration
# ##############################################################################


# cars_objects.append(HorCar(1, 2, 'red', 2, 3))
# cars_objects.append(VerCar(2, 2, 'brown', 0, 0))
# cars_objects.append(HorCar(3, 2, 'green', 0, 2))
# cars_objects.append(HorCar(4, 2, 'blue', 2, 2))
# cars_objects.append(VerCar(5, 2, 'pink', 3, 0))
# cars_objects.append(HorCar(6, 2, 'orange', 4, 0))
# cars_objects.append(HorCar(7, 2, 'yellow', 4, 1))
# cars_objects.append(VerCar(8, 2, 'purple', 4, 2))
# cars_objects.append(VerCar(9, 3, 'brown', 5, 2))
# cars_objects.append(HorCar(10, 2, 'green', 1, 4))
# cars_objects.append(HorCar(11, 2, 'blue', 3, 4))
# cars_objects.append(HorCar(12, 2, 'yellow', 2, 5))
# cars_objects.append(HorCar(13, 2, 'orange', 4, 5))


##############################################################################
# The third 6x6 board configuration
##############################################################################


cars_objects.append(HorCar(1, 2, 'red', 0, 3))
cars_objects.append(VerCar(2, 2, 'brown', 0, 0))
cars_objects.append(HorCar(3, 2, 'green', 0, 2))
cars_objects.append(VerCar(4, 2, 'blue', 2, 0))
cars_objects.append(VerCar(5, 2, 'pink', 2, 2))
cars_objects.append(HorCar(6, 2, 'purple', 1, 4))
cars_objects.append(HorCar(7, 2, 'blue', 1, 5))
cars_objects.append(HorCar(8, 2, 'purple', 4, 1))
cars_objects.append(HorCar(9, 2, 'orange', 3, 2))
cars_objects.append(VerCar(10, 2, 'pink', 5, 2))
cars_objects.append(VerCar(11, 2, 'yellow', 3, 3))
cars_objects.append(HorCar(12, 2, 'green', 4, 4))
cars_objects.append(HorCar(13, 3, 'orange', 3, 5))


##############################################################################
# The first 9x9 board configuration
##############################################################################

# cars_objects.append(HorCar(1, 2, 'red', 1, 4))
# cars_objects.append(VerCar(2, 2, 'green', 0, 7))
# cars_objects.append(HorCar(3, 3, 'yellow', 1, 8))
# cars_objects.append(VerCar(4, 3, 'gray', 5, 6))
# cars_objects.append(HorCar(5, 3, 'pink', 6, 7))
# cars_objects.append(HorCar(6, 2, 'blue', 0, 5))
# cars_objects.append(VerCar(7, 3, 'orange', 3, 5))
# cars_objects.append(HorCar(8, 3, 'purple', 5, 5))
# cars_objects.append(VerCar(9, 3, 'yellow', 8, 4))
# cars_objects.append(VerCar(10, 2, 'pink', 0, 3))
# cars_objects.append(VerCar(11, 2, 'green', 3, 3))
# cars_objects.append(HorCar(12, 3, 'brown', 5, 3))
# cars_objects.append(VerCar(13, 3, 'orange', 8, 1))
# cars_objects.append(HorCar(14, 2, 'black', 0, 2))
# cars_objects.append(VerCar(15, 2, 'blue', 0, 0))
# cars_objects.append(VerCar(16, 3, 'yellow', 2, 1))
# cars_objects.append(HorCar(17, 3, 'gray', 1, 0))
# cars_objects.append(VerCar(18, 2, 'blue', 3, 1))
# cars_objects.append(VerCar(19, 2, 'black', 4, 0))
# cars_objects.append(HorCar(20, 2, 'brown', 4, 2))
# cars_objects.append(HorCar(21, 2, 'pink', 5, 0))
# cars_objects.append(HorCar(22, 2, 'green', 7, 0))

# ##############################################################################
# # The second 9x9 board configuration
# ##############################################################################

#
# cars_objects.append(HorCar(1, 2, 'red', 6, 4))
# cars_objects.append(VerCar(2, 2, 'pink', 0, 0))
# cars_objects.append(VerCar(3, 2, 'blue', 0, 2))
# cars_objects.append(VerCar(4, 2, 'green', 1, 0))
# cars_objects.append(HorCar(5, 3, 'yellow', 0, 8))
# cars_objects.append(HorCar(6, 2, 'gray', 2, 0))
# cars_objects.append(HorCar(7, 2, 'black', 2, 1))
# cars_objects.append(VerCar(8, 2, 'orange', 4, 0))
# cars_objects.append(HorCar(9, 3, 'gray', 5, 1))
# cars_objects.append(VerCar(10, 2, 'pink', 8, 0))
# cars_objects.append(VerCar(11, 2, 'orange', 2, 2))
# cars_objects.append(HorCar(12, 2, 'brown', 3, 2))
# cars_objects.append(VerCar(13, 3, 'purple', 5, 2))
# cars_objects.append(HorCar(14, 2, 'green', 6, 2))
# cars_objects.append(VerCar(15, 3, 'yellow', 8, 2))
# cars_objects.append(HorCar(16, 3, 'blue', 2, 4))
# cars_objects.append(HorCar(17, 2, 'gray', 4, 5))
# cars_objects.append(VerCar(18, 2, 'pink', 6, 5))
# cars_objects.append(HorCar(19, 2, 'black', 7, 5))
# cars_objects.append(VerCar(20, 3, 'purple', 3, 6))
# cars_objects.append(HorCar(21, 2, 'orange', 4, 6))
# cars_objects.append(VerCar(22, 2, 'green', 5, 7))
# cars_objects.append(VerCar(23, 2, 'blue', 6, 7))
# cars_objects.append(HorCar(24, 2, 'yellow', 7, 7))

#
#
# ##############################################################################
# # The third 9x9 configuration
# ##############################################################################

#
# cars_objects.append(HorCar(1, 2, 'red', 0, 4))
# cars_objects.append(VerCar(2, 3, 'purple', 0, 0))
# cars_objects.append(HorCar(3, 3, 'yellow', 1, 0))
# cars_objects.append(VerCar(4, 3, 'gray', 4, 0))
# cars_objects.append(HorCar(5, 2, 'blue', 2, 1))
# cars_objects.append(HorCar(6, 2, 'green', 5, 1))
# cars_objects.append(VerCar(7, 2, 'orange', 1, 2))
# cars_objects.append(HorCar(8, 2, 'black', 2, 2))
# cars_objects.append(HorCar(9, 3, 'yellow', 5, 2))
# cars_objects.append(VerCar(10, 3, 'yellow', 3, 3))
# cars_objects.append(HorCar(11, 2, 'pink', 4, 3))
# cars_objects.append(HorCar(12, 2, 'brown', 6, 3))
# cars_objects.append(VerCar(13, 2, 'blue', 2, 4))
# cars_objects.append(VerCar(14, 2, 'orange', 4, 5))
# cars_objects.append(VerCar(15, 2, 'pink', 5, 5))
# cars_objects.append(HorCar(16, 3, 'gray', 6, 5))
# cars_objects.append(VerCar(17, 2, 'black', 0, 6))
# cars_objects.append(HorCar(18, 2, 'green', 2, 6))
# cars_objects.append(HorCar(19, 2, 'purple', 7, 6))
# cars_objects.append(HorCar(20, 3, 'yellow', 1, 7))
# cars_objects.append(VerCar(21, 2, 'green', 4, 7))
# cars_objects.append(HorCar(22, 2, 'orange', 5, 7))
# cars_objects.append(VerCar(23, 2, 'blue', 7, 7))
# cars_objects.append(HorCar(24, 2, 'blue', 0, 8))
# cars_objects.append(HorCar(25, 2, 'pink', 2, 8))
# cars_objects.append(VerCar(26, 3, 'purple', 8, 1))

#
# ##############################################################################
# # The 12x12 configuration
# ##############################################################################

#
# cars_objects.append(HorCar(1, 2, 'red', 2, 6))
# cars_objects.append(HorCar(2, 2, 'green', 1, 0))
# cars_objects.append(HorCar(3, 3, 'yellow', 3, 0))
# cars_objects.append(VerCar(4, 3, 'gray', 6, 0))
# cars_objects.append(HorCar(5, 2, 'blue', 7, 0))
# cars_objects.append(VerCar(6, 2, 'pink', 9, 0))
# cars_objects.append(VerCar(7, 3, 'purple', 10, 0))
# cars_objects.append(VerCar(8, 2, 'pink', 11, 0))
# cars_objects.append(VerCar(9, 2, 'blue', 2, 2))
# cars_objects.append(HorCar(10, 3, 'yellow', 3, 2))
# cars_objects.append(HorCar(11, 2, 'green', 8, 2))
# cars_objects.append(VerCar(12, 2, 'black', 11, 2))
# cars_objects.append(HorCar(13, 2, 'orange', 0, 3))
# cars_objects.append(HorCar(14, 3, 'purple', 3, 3))
# cars_objects.append(VerCar(15, 3, 'black', 6, 3))
# cars_objects.append(HorCar(16, 3, 'pink', 7, 3))
# cars_objects.append(HorCar(17, 3, 'yellow', 0, 4))
# cars_objects.append(VerCar(18, 2, 'pink', 3, 4))
# cars_objects.append(HorCar(19, 2, 'green', 4, 4))
# cars_objects.append(VerCar(20, 3, 'blue', 7, 4))
# cars_objects.append(VerCar(21, 2, 'gray', 9, 4))
# cars_objects.append(HorCar(22, 2, 'orange', 10, 4))
# cars_objects.append(HorCar(23, 3, 'brown', 0, 5))
# cars_objects.append(VerCar(24, 2, 'orange', 4, 5))
# cars_objects.append(VerCar(25, 2, 'pink', 5, 5))
# cars_objects.append(HorCar(26, 2, 'green', 10, 5))
# cars_objects.append(VerCar(27, 3, 'purple', 0, 6))
# cars_objects.append(VerCar(28, 3, 'yellow', 1, 6))
# cars_objects.append(HorCar(29, 3, 'brown', 2, 7))
# cars_objects.append(VerCar(30, 2, 'green', 5, 7))
# cars_objects.append(VerCar(31, 3, 'yellow', 6, 7))
# cars_objects.append(HorCar(32, 3, 'purple', 7, 7))
# cars_objects.append(HorCar(33, 2, 'orange', 7, 8))
# cars_objects.append(HorCar(34, 2, 'pink', 9, 8))
# cars_objects.append(HorCar(35, 3, 'gray', 0, 9))
# cars_objects.append(HorCar(36, 2, 'orange', 3, 9))
# cars_objects.append(VerCar(37, 2, 'pink', 5, 9))
# cars_objects.append(HorCar(38, 2, 'green', 7, 9))
# cars_objects.append(VerCar(39, 2, 'orange', 10, 9))
# cars_objects.append(VerCar(40, 2, 'blue', 11, 9))
# cars_objects.append(VerCar(41, 2, 'green', 0, 10))
# cars_objects.append(VerCar(42, 2, 'blue', 6, 10))
# cars_objects.append(HorCar(43, 3, 'purple', 7, 11))
# cars_objects.append(HorCar(44, 2, 'pink', 10, 11))


board = Board(size, size)
def win_row(size):
    """
    Simple function to determine the winning row
    """
    # Counting from 0, so -1
    # Unless board is uneven, because the .5 is disregarded
    if size % 2 == 0:
        return size/2 - 1
    else:
        return size/2

def won(lis):
    """
    Argument is a board configuration
    """
    # Determining winning row
    win = win_row(size)
    row = lis[win]

    index = 0

    for i in xrange(len(row)):
        if row[i] == 1:
            index = i
            break


    return all(row[i] <= 1 for i in range(index, len(row)))


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return False
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return False

def a_star(lis):
    """
    A-star function calculates cost by counting cars in front of red car
    """
    start = size * win_row(size)
    end = size * (win_row(size) + 1)
    row = lis[start:end]

    # determine where red car is placed
    for i in xrange(len(row)):
        if row[i] == 1:
            place_of_red = i
            break

    # determine how many cars are in front of red
    check_amount_cars = 0
    for i in xrange(place_of_red, len(row)):
        if row[i] > 1:
            check_amount_cars += 1

    # cost is simply amount cars in front of red
    return check_amount_cars + 1



archive = {}
queue_priority = Queue.PriorityQueue()
def determine_in_archive_as(board_child, tuple_board_child, tuple_board_from_queue, depth):

    if tuple_board_child not in archive:

        if (won(board_child)):
            board.set_board(board_child)
            archive[tuple_board_from_queue].append(tuple_board_child)
            return True

        archive[tuple_board_from_queue].append(tuple_board_child)
        archive[tuple_board_child] = []
        queue_priority.put((a_star(board_child) + depth, board_child, depth))

    return

def astar_solve():
    # Depth of a board
    depth = 0

    # Tuple consisting of (cost, first board, depth)
    queue_priority.put((0, [[board.board_configuration[j][i] for i in xrange(size)] for j in xrange(size)], depth))

    # Make a tuple for first node and put in archive
    first_node = tuple([board.board_configuration[i][j] for i in xrange(size) for j in xrange(size)])
    archive[first_node] = []

    not_found = True
    while not_found:

        # Get first element for setting board and car objects
        cost, board_from_queue, depth = queue_priority.get()
        board.set_board(board_from_queue)

        # Make tuple of board_from_queue
        tuple_board_from_queue = tuple([board_from_queue[i][j] for i in xrange(size) for j in xrange(size)])

        # Determine which car can be moved
        for car in cars_objects:
            if car.updatePosition(1):
                # Obtain partial copied board and tuple of it
                board_child = board.getboard(car, 1, board_from_queue)
                tuple_board_child = tuple([board_child[i][j] for i in xrange(size) for j in xrange(size)])

                # Determine if al ready in archive or if found final configuration
                if determine_in_archive_as(board_child, tuple_board_child, tuple_board_from_queue, depth + 1):

                    # Return the path when puzzle solved
                    return find_path(archive, first_node, tuple_board_child)

                car.updatePosition(-1)

            if car.updatePosition(-1):
                # Obtain partial copied board and tuple of it
                board_child = board.getboard(car, -1, board_from_queue)
                tuple_board_child = tuple([board_child[i][j] for i in xrange(size) for j in xrange(size)])

                # Determine if al ready in archive or if found final configuration
                if determine_in_archive_as(board_child, tuple_board_child, tuple_board_from_queue, depth + 1):

                    # Return the path when puzzle solved
                    return find_path(archive, first_node, tuple_board_child)

                car.updatePosition(1)
        depth += 1


archive = {}
queue = Queue.Queue()
def determine_in_archive(board_from_queue, tuple_board_from_queue, car, step):

    # Obtain partial copied board and tuple of it
    board_child = board.getboard(car, step, board_from_queue)
    tuple_board_child = tuple([board_child[i][j] for i in xrange(size) for j in xrange(size)])

    if tuple_board_child not in archive:

        if (won(board_child)):
            board.set_board(board_child)
            archive[tuple_board_from_queue].append(tuple_board_child)
            return (True, tuple_board_child)

        archive[tuple_board_from_queue].append(tuple_board_child)
        archive[tuple_board_child] = []
        queue.put(board_child)

    return (False, None)

def breadth_solve():
    # Make a copy for the first node and put in queue
    queue.put([[board.board_configuration[j][i] for i in xrange(size)] for j in xrange(size)])

    # Make a tuple for first node and put in archive
    first_node = tuple([board.board_configuration[i][j] for i in xrange(size) for j in xrange(size)])
    archive[first_node] = []

    not_found = True
    while not_found:

        # Get first element for setting board and car objects
        board_from_queue = queue.get()
        board.set_board(board_from_queue)

        # Make tuple of board_from_queue
        tuple_board_from_queue = tuple([board_from_queue[i][j] for i in xrange(size) for j in xrange(size)])

        # Determine which car can be moved
        for car in cars_objects:

            if car.updatePosition(1):
                # Determine if al ready in archive or if found final configuration
                found, tuple_board_child = determine_in_archive(board_from_queue,
                                                    tuple_board_from_queue, car, 1)
                if found:
                    # Return the path when puzzle solved
                    return find_path(archive, first_node, tuple_board_child)
                car.updatePosition(-1)

            if car.updatePosition(-1):
                # Determine if al ready in archive or if found final configuration
                found, tuple_board_child = determine_in_archive(board_from_queue,
                                                    tuple_board_from_queue, car, -1)
                if found:
                    # Return the path when puzzle solved
                    return find_path(archive, first_node, tuple_board_child)
                car.updatePosition(1)

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, new_value, depth):
        self.stack.append((new_value, depth))
    def pop(self):
        # removing last element (last in first out)
        tmp_element = self.stack[-1]
        del self.stack[-1]
        return tmp_element


archive = {}
stack = Stack()
def id_solve(first_node, first_node_archive):
    # Make a copy for the first node and put in queue
    stack.push(first_node, 0)
    archive[first_node_archive] = []
    check = True
    depth = 1

    while len(stack.stack) and check == True:

        board_from_stack, depth_of_configuration = stack.pop()

        if depth_of_configuration < depth:

            board.set_board(board_from_stack)

            # Make tuple of board_from_stack
            tuple_board_from_stack = tuple([board_from_stack[i][j] for i in xrange(size) for j in xrange(size)])

            for car in cars_objects:
                if car.updatePosition(1):
                    # Obtain partial copied board and tuple of it
                    board_child = board.getboard(car, 1, board_from_stack)
                    tuple_board_child = tuple([board_child[i][j] for i in xrange(size) for j in xrange(size)])

                    if tuple_board_child not in archive:
                        archive[tuple_board_from_stack].append(tuple_board_child)
                        archive[tuple_board_child] = []
                        stack.push(board_child, depth_of_configuration + 1)

                    car.updatePosition(-1)

                if car.updatePosition(-1):
                    # Obtain partial copied board and tuple of it
                    board_child = board.getboard(car, -1, board_from_stack)
                    tuple_board_child = tuple([board_child[i][j] for i in xrange(size) for j in xrange(size)])

                    if tuple_board_child not in archive:
                        archive[tuple_board_from_stack].append(tuple_board_child)
                        archive[tuple_board_child] = []
                        stack.push(board_child, depth_of_configuration + 1)
                    car.updatePosition(1)

        else:
            if (won(board_child)):
                board.set_board(board_child)
                archive[tuple_board_from_stack].append(tuple_board_child)
                return find_path(archive, first_node_archive, tuple_board_child)

        if len(stack.stack) == 0:
            stack.push(first_node, 0)
            archive.clear()

            # Make a tuple for first node and put in archive
            archive[first_node_archive] = []

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
    cars = [plt.plot([], [], 's', c = car.color, ms = 300/size)[0] for car in cars_objects]

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
        car_positions = [([],[]) for _ in range(len(cars_objects))]

        # loops through the animation board and append the car positions of a
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
                           frames=len(animation_list), interval=200, blit=True, repeat = False)

    # Turn off tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.title('Rush hour')
    plt.grid(True)
    plt.show()

# Main function
if __name__ == "__main__":

    # Ensure proper usage
    if len(sys.argv) != 2:
        print "Usage example: python filename.py algorithm"
        sys.exit(2)

    start = time.time()
    print "Solving..."

    if sys.argv[1] == 'astar':
        path = astar_solve()
    elif sys.argv[1] == 'breadth':
        path = breadth_solve()
    elif sys.argv[1] == 'id':
        first_node = [[board.board_configuration[j][i] for i in xrange(size)] for j in xrange(size)]
        first_node_archive = tuple([board.board_configuration[i][j] for i in xrange(size) for j in xrange(size)])
        path = id_solve(first_node, first_node_archive)

    end = time.time()
    print "Time elapsed:", (end - start)
    print "Steps", len(path)
    print "Explored configurations per second", len(archive)*1. / (1.*(end - start))
    print "Total configurations", len(archive)
    rush_hour_animation(path)
