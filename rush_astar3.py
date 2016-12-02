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

size = 6

# Saving every car object of the board
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
        Determines which values of the board should be changed when a car is moved
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
        Determines which values of the board should be changed when a car is moved
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
                    car_objects[set_config[i][j] - 1].setCarPosition(j, size - 1 - i)



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
        return board.config[size - 1 - y][x] == 0 or board.config[size - 1 - y][x] == self.index


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
            board.update_hor(self, new_xstart, new_ystart, step)
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

            board.update_ver(self, new_xstart, new_ystart, step)
            return True

        return False


##############################################################################
# The first 6x6 board configuration
##############################################################################


<<<<<<< HEAD
cars_objects.append(HorCar(1, 2, 'red', 3, 3))
cars_objects.append(VerCar(2, 2, 'brown', 0, 0))
cars_objects.append(HorCar(3, 2, 'blue', 1, 1))
cars_objects.append(HorCar(4, 2, 'green', 4, 0))
cars_objects.append(HorCar(5, 2, 'orange', 4, 2))
cars_objects.append(HorCar(6, 2, 'blue', 3, 5))
cars_objects.append(VerCar(7, 3, 'yellow', 3, 0))
cars_objects.append(VerCar(8, 3, 'purple', 2, 3))
cars_objects.append(VerCar(9, 3, 'brown', 5, 3))
=======
# car_objects.append(HorCar(1, 2, 'red', 3, 3))
# car_objects.append(VerCar(2, 2, 'brown', 0, 0))
# car_objects.append(HorCar(3, 2, 'blue', 1, 1))
# car_objects.append(HorCar(4, 2, 'green', 4, 0))
# car_objects.append(HorCar(5, 2, 'orange', 4, 2))
# car_objects.append(HorCar(6, 2, 'blue', 3, 5))
# car_objects.append(VerCar(7, 3, 'yellow', 3, 0))
# car_objects.append(VerCar(8, 3, 'purple', 2, 3))
# car_objects.append(VerCar(9, 3, 'brown', 5, 3))
>>>>>>> 1116ab1b692d1e487040e238f44af5688ee86c4b


# ##############################################################################
# # The second 6x6 board configuration
# ##############################################################################


# car_objects.append(HorCar(1, 2, 'red', 2, 3))
# car_objects.append(VerCar(2, 2, 'brown', 0, 0))
# car_objects.append(HorCar(3, 2, 'green', 0, 2))
# car_objects.append(HorCar(4, 2, 'blue', 2, 2))
# car_objects.append(VerCar(5, 2, 'pink', 3, 0))
# car_objects.append(HorCar(6, 2, 'orange', 4, 0))
# car_objects.append(HorCar(7, 2, 'yellow', 4, 1))
# car_objects.append(VerCar(8, 2, 'purple', 4, 2))
# car_objects.append(VerCar(9, 3, 'brown', 5, 2))
# car_objects.append(HorCar(10, 2, 'green', 1, 4))
# car_objects.append(HorCar(11, 2, 'blue', 3, 4))
# car_objects.append(HorCar(12, 2, 'yellow', 2, 5))
# car_objects.append(HorCar(13, 2, 'orange', 4, 5))


# ############################################################################
# The third 6x6 board configuration
# ############################################################################


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


# ############################################################################
# The first 9x9 board configuration
# ############################################################################


# car_objects.append(HorCar(1, 2, 'red', 1, 4))
# car_objects.append(VerCar(2, 2, 'green', 0, 7))
# car_objects.append(HorCar(3, 3, 'yellow', 1, 8))
# car_objects.append(VerCar(4, 3, 'gray', 5, 6))
# car_objects.append(HorCar(5, 3, 'pink', 6, 7))
# car_objects.append(HorCar(6, 2, 'blue', 0, 5))
# car_objects.append(VerCar(7, 3, 'orange', 3, 5))
# car_objects.append(HorCar(8, 3, 'purple', 5, 5))
# car_objects.append(VerCar(9, 3, 'yellow', 8, 4))
# car_objects.append(VerCar(10, 2, 'pink', 0, 3))
# car_objects.append(VerCar(11, 2, 'green', 3, 3))
# car_objects.append(HorCar(12, 3, 'brown', 5, 3))
# car_objects.append(VerCar(13, 3, 'orange', 8, 1))
# car_objects.append(HorCar(14, 2, 'black', 0, 2))
# car_objects.append(VerCar(15, 2, 'blue', 0, 0))
# car_objects.append(VerCar(16, 3, 'yellow', 2, 1))
# car_objects.append(HorCar(17, 3, 'gray', 1, 0))
# car_objects.append(VerCar(18, 2, 'blue', 3, 1))
# car_objects.append(VerCar(19, 2, 'black', 4, 0))
# car_objects.append(HorCar(20, 2, 'brown', 4, 2))
# car_objects.append(HorCar(21, 2, 'pink', 5, 0))
# car_objects.append(HorCar(22, 2, 'green', 7, 0))


# ##############################################################################
# The second 9x9 board configuration
# ##############################################################################


# car_objects.append(HorCar(1, 2, 'red', 6, 4))
# car_objects.append(VerCar(2, 2, 'pink', 0, 0))
# car_objects.append(VerCar(3, 2, 'blue', 0, 2))
# car_objects.append(VerCar(4, 2, 'green', 1, 0))
# car_objects.append(HorCar(5, 3, 'yellow', 0, 8))
# car_objects.append(HorCar(6, 2, 'gray', 2, 0))
# car_objects.append(HorCar(7, 2, 'black', 2, 1))
# car_objects.append(VerCar(8, 2, 'orange', 4, 0))
# car_objects.append(HorCar(9, 3, 'gray', 5, 1))
# car_objects.append(VerCar(10, 2, 'pink', 8, 0))
# car_objects.append(VerCar(11, 2, 'orange', 2, 2))
# car_objects.append(HorCar(12, 2, 'brown', 3, 2))
# car_objects.append(VerCar(13, 3, 'purple', 5, 2))
# car_objects.append(HorCar(14, 2, 'green', 6, 2))
# car_objects.append(VerCar(15, 3, 'yellow', 8, 2))
# car_objects.append(HorCar(16, 3, 'blue', 2, 4))
# car_objects.append(HorCar(17, 2, 'gray', 4, 5))
# car_objects.append(VerCar(18, 2, 'pink', 6, 5))
# car_objects.append(HorCar(19, 2, 'black', 7, 5))
# car_objects.append(VerCar(20, 3, 'purple', 3, 6))
# car_objects.append(HorCar(21, 2, 'orange', 4, 6))
# car_objects.append(VerCar(22, 2, 'green', 5, 7))
# car_objects.append(VerCar(23, 2, 'blue', 6, 7))
# car_objects.append(HorCar(24, 2, 'yellow', 7, 7))


# ##############################################################################
# The third 9x9 board configuration
# ##############################################################################

<<<<<<< HEAD
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
=======
>>>>>>> 1116ab1b692d1e487040e238f44af5688ee86c4b

# car_objects.append(HorCar(1, 2, 'red', 0, 4))
# car_objects.append(VerCar(2, 3, 'purple', 0, 0))
# car_objects.append(HorCar(3, 3, 'yellow', 1, 0))
# car_objects.append(VerCar(4, 3, 'gray', 4, 0))
# car_objects.append(HorCar(5, 2, 'blue', 2, 1))
# car_objects.append(HorCar(6, 2, 'green', 5, 1))
# car_objects.append(VerCar(7, 2, 'orange', 1, 2))
# car_objects.append(HorCar(8, 2, 'black', 2, 2))
# car_objects.append(HorCar(9, 3, 'yellow', 5, 2))
# car_objects.append(VerCar(10, 3, 'yellow', 3, 3))
# car_objects.append(HorCar(11, 2, 'pink', 4, 3))
# car_objects.append(HorCar(12, 2, 'brown', 6, 3))
# car_objects.append(VerCar(13, 2, 'blue', 2, 4))
# car_objects.append(VerCar(14, 2, 'orange', 4, 5))
# car_objects.append(VerCar(15, 2, 'pink', 5, 5))
# car_objects.append(HorCar(16, 3, 'gray', 6, 5))
# car_objects.append(VerCar(17, 2, 'black', 0, 6))
# car_objects.append(HorCar(18, 2, 'green', 2, 6))
# car_objects.append(HorCar(19, 2, 'purple', 7, 6))
# car_objects.append(HorCar(20, 3, 'yellow', 1, 7))
# car_objects.append(VerCar(21, 2, 'green', 4, 7))
# car_objects.append(HorCar(22, 2, 'orange', 5, 7))
# car_objects.append(VerCar(23, 2, 'blue', 7, 7))
# car_objects.append(HorCar(24, 2, 'blue', 0, 8))
# car_objects.append(HorCar(25, 2, 'pink', 2, 8))
# car_objects.append(VerCar(26, 3, 'purple', 8, 1))


# ##############################################################################
# # The 12x12 board configuration
# ##############################################################################

#
<<<<<<< HEAD
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
#
=======
# car_objects.append(HorCar(1, 2, 'red', 2, 6))
# car_objects.append(HorCar(2, 2, 'green', 1, 0))
# car_objects.append(HorCar(3, 3, 'yellow', 3, 0))
# car_objects.append(VerCar(4, 3, 'gray', 6, 0))
# car_objects.append(HorCar(5, 2, 'blue', 7, 0))
# car_objects.append(VerCar(6, 2, 'pink', 9, 0))
# car_objects.append(VerCar(7, 3, 'purple', 10, 0))
# car_objects.append(VerCar(8, 2, 'pink', 11, 0))
# car_objects.append(VerCar(9, 2, 'blue', 2, 2))
# car_objects.append(HorCar(10, 3, 'yellow', 3, 2))
# car_objects.append(HorCar(11, 2, 'green', 8, 2))
# car_objects.append(VerCar(12, 2, 'black', 11, 2))
# car_objects.append(HorCar(13, 2, 'orange', 0, 3))
# car_objects.append(HorCar(14, 3, 'purple', 3, 3))
# car_objects.append(VerCar(15, 3, 'black', 6, 3))
# car_objects.append(HorCar(16, 3, 'pink', 7, 3))
# car_objects.append(HorCar(17, 3, 'yellow', 0, 4))
# car_objects.append(VerCar(18, 2, 'pink', 3, 4))
# car_objects.append(HorCar(19, 2, 'green', 4, 4))
# car_objects.append(VerCar(20, 3, 'blue', 7, 4))
# car_objects.append(VerCar(21, 2, 'gray', 9, 4))
# car_objects.append(HorCar(22, 2, 'orange', 10, 4))
# car_objects.append(HorCar(23, 3, 'brown', 0, 5))
# car_objects.append(VerCar(24, 2, 'orange', 4, 5))
# car_objects.append(VerCar(25, 2, 'pink', 5, 5))
# car_objects.append(HorCar(26, 2, 'green', 10, 5))
# car_objects.append(VerCar(27, 3, 'purple', 0, 6))
# car_objects.append(VerCar(28, 3, 'yellow', 1, 6))
# car_objects.append(HorCar(29, 3, 'brown', 2, 7))
# car_objects.append(VerCar(30, 2, 'green', 5, 7))
# car_objects.append(VerCar(31, 3, 'yellow', 6, 7))
# car_objects.append(HorCar(32, 3, 'purple', 7, 7))
# car_objects.append(HorCar(33, 2, 'orange', 7, 8))
# car_objects.append(HorCar(34, 2, 'pink', 9, 8))
# car_objects.append(HorCar(35, 3, 'gray', 0, 9))
# car_objects.append(HorCar(36, 2, 'orange', 3, 9))
# car_objects.append(VerCar(37, 2, 'pink', 5, 9))
# car_objects.append(HorCar(38, 2, 'green', 7, 9))
# car_objects.append(VerCar(39, 2, 'orange', 10, 9))
# car_objects.append(VerCar(40, 2, 'blue', 11, 9))
# car_objects.append(VerCar(41, 2, 'green', 0, 10))
# car_objects.append(VerCar(42, 2, 'blue', 6, 10))
# car_objects.append(HorCar(43, 3, 'purple', 7, 11))
# car_objects.append(HorCar(44, 2, 'pink', 10, 11))

>>>>>>> 1116ab1b692d1e487040e238f44af5688ee86c4b

board = Board(size, size)
def win_row(size):
    """
    Simple function to determine the winning row
    """
    # Counting from 0, so -1
    # Unless board is uneven, because the .5 is disregarded
    return size/2 - 1 if size % 2 == 0 else size/2

def won(board):
    """
    Argument is a board configuration
    """
    # Determining winning row
    win = win_row(size)
    row = board[win]

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
    row = lis[win_row(size)]

    # determine where red car is placed
    for i in xrange(len(row)):
        if row[i] == 1:
            place_of_red = i
            break
    # determine how many cars are in front of red and how many in front of those
    carcheck = 0
    for i in xrange(place_of_red, len(row)):
        if row[i] > 1:
            diff = win_row(size) - car_objects[row[i] - 1].starty
            length = car_objects[row[i] - 1].length
            carcheck += 1
            if win_row(size) - length + diff >= 0:
                row_up = lis[win_row(size) - length + diff]
                if row_up[i] > 1:
                    carcheck += 1
            row_down = lis[win_row(size) + 1 + diff]
            if row_down[i] > 1:
                carcheck += 1

    # cost is simply amount cars in front of red
    return carcheck



archive = {}
queue_priority = Queue.PriorityQueue()
def archived_as(child, tuple_child, tuple_qboard, depth):

    if tuple_child not in archive:

        if (won(child)):
            board.set_board(child)
            archive[tuple_qboard].append(tuple_child)
            return True

        archive[tuple_qboard].append(tuple_child)
        archive[tuple_child] = []
        queue_priority.put((a_star(child) + depth, child, depth))

    return

def astar_solve():
    # Depth of a board
    depth = 0

    # Tuple consisting of (cost, first board, depth)
    queue_priority.put((0, [[board.config[j][i] for i in xrange(size)] for j in xrange(size)], depth))

    # Make a tuple for first node and put in archive
    root = tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)])
    archive[root] = []

    not_found = True
    while not_found:

        # Get first element for setting board and car objects
        cost, qboard, depth = queue_priority.get()
        board.set_board(qboard)

        # Make tuple of qboard
        tuple_qboard = tuple([qboard[i][j] for i in xrange(size) for j in xrange(size)])

        # Determine which car can be moved
        for car in car_objects:
            if car.updatePosition(1):
                # Obtain partial copied board and tuple of it
                child = board.getboard(car, 1, qboard)
                tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

                # Determine if al ready in archive or if found final configuration
                if archived_as(child, tuple_child, tuple_qboard, depth + 1):

                    # Return the path when puzzle solved
                    return find_path(archive, root, tuple_child)

                car.updatePosition(-1)

            if car.updatePosition(-1):
                # Obtain partial copied board and tuple of it
                child = board.getboard(car, -1, qboard)
                tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

                # Determine if al ready in archive or if found final configuration
                if archived_as(child, tuple_child, tuple_qboard, depth + 1):

                    # Return the path when puzzle solved
                    return find_path(archive, root, tuple_child)

                car.updatePosition(1)
        depth += 1


archive = {}
queue = Queue.Queue()
def archived(qboard, tuple_qboard, car, step):

    # Obtain partial copied board and tuple of it
    child = board.getboard(car, step, qboard)
    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

    if tuple_child not in archive:

        if (won(child)):
            board.set_board(child)
            archive[tuple_qboard].append(tuple_child)
            return (True, tuple_child)

        archive[tuple_qboard].append(tuple_child)
        archive[tuple_child] = []
        queue.put(child)

    return (False, None)

def breadth_solve():
    # Make a copy for the first node and put in queue
    queue.put([[board.config[j][i] for i in xrange(size)] for j in xrange(size)])

    # Make a tuple for first node and put in archive
    root = tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)])
    archive[root] = []

    not_found = True
    while not_found:

        # Get first element for setting board and car objects
        qboard = queue.get()
        board.set_board(qboard)

        # Make tuple of qboard
        tuple_qboard = tuple([qboard[i][j] for i in xrange(size) for j in xrange(size)])

        # Determine which car can be moved
        for car in car_objects:

            if car.updatePosition(1):
                # Determine if al ready in archive or if found final configuration
                found, tuple_child = archived(qboard, tuple_qboard, car, 1)
                if found:
                    # Return the path when puzzle solved
                    return find_path(archive, root, tuple_child)
                car.updatePosition(-1)

            if car.updatePosition(-1):
                # Determine if al ready in archive or if found final configuration
                found, tuple_child = archived(qboard, tuple_qboard, car, -1)
                if found:
                    # Return the path when puzzle solved
                    return find_path(archive, root, tuple_child)
                car.updatePosition(1)

archive = {}
stack = Queue.LifoQueue()
def id_solve(root, root_arch):
    # Make a copy for the first node and put in queue
    stack.put((root, 0))
    archive[root_arch] = []
    check = True
    depth = 1

    while stack.qsize() and check == True:

        stackboard, config_depth = stack.get()

        if config_depth < depth:

            board.set_board(stackboard)

            # Make tuple of stackboard
            tuple_stackboard = tuple([stackboard[i][j] for i in xrange(size) for j in xrange(size)])

            for car in car_objects:
                if car.updatePosition(1):
                    # Obtain partial copied board and tuple of it
                    child = board.getboard(car, 1, stackboard)
                    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

                    if tuple_child not in archive:
                        archive[tuple_stackboard].append(tuple_child)
                        archive[tuple_child] = []
                        stack.put((child, config_depth + 1))

                    car.updatePosition(-1)

                if car.updatePosition(-1):
                    # Obtain partial copied board and tuple of it
                    child = board.getboard(car, -1, stackboard)
                    tuple_child = tuple([child[i][j] for i in xrange(size) for j in xrange(size)])

                    if tuple_child not in archive:
                        archive[tuple_stackboard].append(tuple_child)
                        archive[tuple_child] = []
                        stack.put((child, config_depth + 1))
                    car.updatePosition(1)

        else:
            if (won(child)):
                board.set_board(child)
                archive[tuple_stackboard].append(tuple_child)
                return find_path(archive, root_arch, tuple_child)

        if stack.qsize() == 0:
            stack.put((root, 0))
            archive.clear()

            # Make a tuple for first node and put in archive
            archive[root_arch] = []

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
    cars = [plt.plot([], [], 's', c = car.color, ms = 300/size)[0] for car in car_objects]

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
        root = [[board.config[j][i] for i in xrange(size)] for j in xrange(size)]
        root_arch = tuple([board.config[i][j] for i in xrange(size) for j in xrange(size)])
        path = id_solve(root, root_arch)

    elif sys.argv[1] == 'first_6x6':
        with open('first_6x6.txt', 'rb') as f:
            path = pickle.load(f)

    elif sys.argv[1] == 'second_6x6':
        with open('second_6x6.txt', 'rb') as f:
            path = pickle.load(f)

    elif sys.argv[1] == 'third_6x6':
        with open('third_6x6.txt', 'rb') as f:
            path = pickle.load(f)

    elif sys.argv[1] == 'first_9x9':
        with open('first_9x9.txt', 'rb') as f:
            path = pickle.load(f)

    end = time.time()
    print "Time elapsed:", (end - start)
    print "Steps", len(path)
    print "Explored configurations per second", len(archive)*1. / (1.*(end - start))
    print "Total configurations", len(archive)

    # comment this out for writing to a file
    # with open('the_12x12.txt', 'wb') as f:
    #     pickle.dump(path, f)
    rush_hour_animation(path)
