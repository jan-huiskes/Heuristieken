# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration


import os
import time
import Queue
import matplotlib.pyplot as plt
import numpy as np
size = 9

"""
Snelste tijd tot nu toe voor 9x9: 11.5 seconden
Veranderingen:
    - 9x9 bord van Saartje erin gedaan
    - simpele a star met priorityqueue
    - zover het kon de 6 (vd 6x6 board) ge-unhardcoded
    
    - Alle borden ingevoegd! Erboven kunnnen we snelste tijd aangeven (lijkt me net)
"""
# saving every car object of the board
cars_objects = []


class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width

        #board_configuration = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        board_configuration = [[0 for x in xrange(size)] for x in xrange(size)]

        count = 1
        for cars in cars_objects:
            if cars.direction == 'h':
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

        self.board_configuration = board_configuration


    def isPositionInRoom(self, x, y):

        return x < self.width and x >= 0 and y < self.height and y >= 0

    def board(self):

        """
        first I worked with 2d array, over copying everything in board_configuration
        """
        #board_configuration = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    #    for i in range(6):
    #        for j in range(6):
    #            board_configuration[i][j] = self.board_configuration[i][j]

        #return board_configuration


        """
        Now working with 1d array, perhaps faster. The self.board_configuration is still a 2d array however!
        """

        return [self.board_configuration[i][j] for i in xrange(size) for j in xrange(size)]


    def update_board_horizontal(self, x, y, length, index, step):
        """
        Determines which values of the board should be changed when a car is moved
        """

        # first fill the row with a car_index from the starting position (now the car length in the board is longer than actual car length!)
        for i in xrange(length):
            self.board_configuration[size -1 - y][x + i] = index

        # if the car moves to the right in horizontal direction, the first element of the total car length in the board should be 0
        if step == 1:
            self.board_configuration[size -1 - y][x - step] = 0

        # if the car moves to the left in the horizontal direction, the last element of the total car length in the board should be 0
        else:
            self.board_configuration[size -1 - y][x + length] = 0

    def update_board_vertical(self, x, y, length, index, step):
        """
        Determines which values of the board should be changed when a car is moved
        """

        # first fill the column with a car_index from the starting position (now the car length in the board is longer than actual car length!)
        for i in xrange(length):
            self.board_configuration[size -1 -(y + i)][x] = index

        # if the car moves up in vertical direction, the first element of the total car length in the board should be 0
        if step == 1:
            self.board_configuration[size -1 - (y - step)][x] = 0

        # if the car moves down in vertical direction, the last element of the total car length in the board should be 0
        else:
            self.board_configuration[size -1 - (y + length)][x] = 0

    def set_board(self, set_configuration):

        if size == 6:
            lijstjes = [set_configuration[0:6], set_configuration[6:12], set_configuration[12:18], set_configuration[18:24], set_configuration[24:30], set_configuration[30:36]]

        elif size == 9:
            lijstjes = [set_configuration[0:9], set_configuration[9:18], set_configuration[18:27], set_configuration[27:36], set_configuration[36:45], set_configuration[45:54], set_configuration[54:63], set_configuration[63:72], set_configuration[72:81]]

        for j in xrange(size):
            for i in xrange(size):
                self.board_configuration[j][i] = lijstjes[j][i]

        check_lis = []
        for i in xrange(size - 1, -1, -1):
            for j in xrange(size):
                if lijstjes[i][j] > 0 and lijstjes[i][j] not in check_lis:
                    check_lis.append(lijstjes[i][j])
                    cars_objects[lijstjes[i][j] - 1].setCarPosition(j, size - 1 - i)



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

        # if the next tile of the board is empty or the next tile has same index as the car to be moved -> car can be moved
        return room.board_configuration[size - 1 - y][x] == 0 or room.board_configuration[size - 1 - y][x] == self.index


class HorCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)
        self.direction = 'h'


    def updatePosition(self, step):

        new_xstart = self.startx + step
        new_ystart = self.starty

        new_xend = new_xstart + self.length - 1
        new_yend = new_ystart

        if room.isPositionInRoom(new_xstart, new_ystart):
            if room.isPositionInRoom(new_xend, new_yend):
                if self.noCar(new_xstart, new_ystart):
                    if self.noCar(new_xend, new_yend):
                        self.setCarPosition(new_xstart, new_ystart)
                        room.update_board_horizontal(new_xstart, new_ystart, self.length, self.index, step)

                        return True

        return False


class VerCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color, x, y)
        self.direction = 'v'

    def updatePosition(self, step):

        new_xstart = self.startx
        new_ystart = self.starty + step

        new_xend = new_xstart
        new_yend = new_ystart + self.length - 1


        if room.isPositionInRoom(new_xstart, new_ystart):
            if room.isPositionInRoom(new_xend, new_yend):
                if self.noCar(new_xstart, new_ystart):
                    if self.noCar(new_xend, new_yend):
                        self.setCarPosition(new_xstart, new_ystart)

                        room.update_board_vertical(new_xstart, new_ystart, self.length, self.index, step)

                        return True

        return False


##############################################################################
# The first 6x6 board configuration
# Fastest time so far: 0.3 sec
##############################################################################
# car1 = HorCar(1, 2, 'red', 3, 3)
# car2 = VerCar(2, 2, 'brown', 0, 0)
# car3 = HorCar(3, 2, 'blue', 1, 1)
# car4 = HorCar(4, 2, 'green', 4, 0)
# car5 = HorCar(5, 2, 'orange', 4, 2)
# car6 = HorCar(6, 2, 'blue', 3, 5)
# car7 = VerCar(7, 3, 'yellow', 3, 0)
# car8 = VerCar(8, 3, 'purple', 2, 3)
# car9 = VerCar(9, 3, 'brown', 5, 3)
#
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)

##############################################################################
# The second 6x6 board configuration
# Fastest time so far: 0.3 sec
##############################################################################
# car1 = HorCar(1, 2, 'red', 2, 3)
# car2 = VerCar(2, 2, 'brown', 0, 0)
# car3 = HorCar(3, 2, 'green', 0, 2)
# car4 = HorCar(4, 2, 'blue', 2, 2)
# car5 = VerCar(5, 2, 'pink', 3, 0)
# car6 = HorCar(6, 2, 'orange', 4, 0)
# car7 = HorCar(7, 2, 'yellow', 4, 1)
# car8 = VerCar(8, 2, 'purple', 4, 2)
# car9 = VerCar(9, 3, 'brown', 5, 2)
# car10 = HorCar(10, 2, 'green', 1, 4)
# car11 = HorCar(11, 2, 'blue', 3, 4)
# car12 = HorCar(12, 2, 'yellow', 2, 5)
# car13 = HorCar(13, 2, 'orange', 4, 5)
#
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)
# cars_objects.append(car10)
# cars_objects.append(car11)
# cars_objects.append(car12)
# cars_objects.append(car13)

##############################################################################
# The third 6x6 board configuration
# Fastest time so far: 0.07 sec
##############################################################################
# car1 = HorCar(1, 2, 'red', 0, 3)
# car2 = VerCar(2, 2, 'brown', 0, 0)
# car3 = HorCar(3, 2, 'green', 0, 2)
# car4 = VerCar(4, 2, 'blue', 2, 0)
# car5 = VerCar(5, 2, 'pink', 2, 2)
# car6 = HorCar(6, 2, 'purple', 1, 4)
# car7 = HorCar(7, 2, 'blue', 1, 5)
# car8 = HorCar(8, 2, 'purple', 4, 1)
# car9 = HorCar(9, 2, 'orange', 3, 2)
# car10 = VerCar(10, 2, 'pink', 5, 2)
# car11 = VerCar(11, 2, 'yellow', 3, 3)
# car12 = HorCar(12, 2, 'green', 4, 4)
# car13 = HorCar(13, 3, 'orange', 3, 5)
#
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)
# cars_objects.append(car10)
# cars_objects.append(car11)
# cars_objects.append(car12)
# cars_objects.append(car13)

##############################################################################
# The first 9x9 board configuration
# Fastest time so far: 11 sec
##############################################################################
# car1 = HorCar(1, 2, 'red', 1, 4)
# car2 = VerCar(2, 2, 'green', 0, 7)
# car3 = HorCar(3, 3, 'yellow', 1, 8)
# car4 = VerCar(4, 3, 'gray', 5, 6)
# car5 = HorCar(5, 3, 'pink', 6, 7)
# car6 = HorCar(6, 2, 'blue', 0, 5)
# car7 = VerCar(7, 3, 'orange', 3, 5)
# car8 = HorCar(8, 3, 'purple', 5, 5)
# car9 = VerCar(9, 3, 'yellow', 8, 4)
# car10 = VerCar(10, 2, 'pink', 0, 3)
# car11 = VerCar(11, 2, 'green', 3, 3)
# car12 = HorCar(12, 3, 'brown', 5, 3)
# car13 = VerCar(13, 3, 'orange', 8, 1)
# car14 = HorCar(14, 2, 'black', 0, 2)
# car15 = VerCar(15, 2, 'blue', 0, 0)
# car16 = VerCar(16, 3, 'yellow', 2, 1)
# car17 = HorCar(17, 3, 'gray', 1, 0)
# car18 = VerCar(18, 2, 'blue', 3, 1)
# car19 = VerCar(19, 2, 'black', 4, 0)
# car20 = HorCar(20, 2, 'brown', 4, 2)
# car21 = HorCar(21, 2, 'pink', 5, 0)
# car22 = HorCar(22, 2, 'green', 7, 0)
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)
# cars_objects.append(car10)
# cars_objects.append(car11)
# cars_objects.append(car12)
# cars_objects.append(car13)
# cars_objects.append(car14)
# cars_objects.append(car15)
# cars_objects.append(car16)
# cars_objects.append(car17)
# cars_objects.append(car18)
# cars_objects.append(car19)
# cars_objects.append(car20)
# cars_objects.append(car21)
# cars_objects.append(car22)

##############################################################################
# The second 9x9 board configuration
# Fastest time so far: 
##############################################################################
car1 = HorCar(1, 2, 'red', 6, 4)
car2 = VerCar(2, 2, 'pink', 0, 0)
car3 = VerCar(3, 2, 'blue', 0, 2)
car4 = VerCar(4, 2, 'green', 1, 0)
car5 = HorCar(5, 3, 'yellow', 0, 8)
car6 = HorCar(6, 2, 'gray', 2, 0)
car7 = HorCar(7, 2, 'black', 2, 1)
car8 = VerCar(8, 2, 'orange', 4, 0)
car9 = HorCar(9, 3, 'gray', 5, 1)
car10 = VerCar(10, 2, 'pink', 8, 0)
car11 = VerCar(11, 2, 'orange', 2, 2)
car12 = HorCar(12, 2, 'brown', 3, 2)
car13 = VerCar(13, 3, 'purple', 5, 2)
car14 = HorCar(14, 2, 'green', 6, 2)
car15 = VerCar(15, 3, 'yellow', 8, 2)
car16 = HorCar(16, 3, 'blue', 2, 4)
car17 = HorCar(17, 2, 'gray', 4, 5)
car18 = VerCar(18, 2, 'pink', 6, 5)
car19 = HorCar(19, 2, 'black', 7, 5)
car20 = VerCar(20, 3, 'purple', 3, 6)
car21 = HorCar(21, 2, 'orange', 4, 6)
car22 = VerCar(22, 2, 'green', 5, 7)
car23 = VerCar(23, 2, 'blue', 6, 7)
car24 = HorCar(24, 2, 'yellow', 7, 7)
cars_objects.append(car1)
cars_objects.append(car2)
cars_objects.append(car3)
cars_objects.append(car4)
cars_objects.append(car5)
cars_objects.append(car6)
cars_objects.append(car7)
cars_objects.append(car8)
cars_objects.append(car9)
cars_objects.append(car10)
cars_objects.append(car11)
cars_objects.append(car12)
cars_objects.append(car13)
cars_objects.append(car14)
cars_objects.append(car15)
cars_objects.append(car16)
cars_objects.append(car17)
cars_objects.append(car18)
cars_objects.append(car19)
cars_objects.append(car20)
cars_objects.append(car21)
cars_objects.append(car22)
cars_objects.append(car23)
cars_objects.append(car24)

##############################################################################
# The third 9x9 configuration
# Fastest time so far:
##############################################################################
# car1 = HorCar(1, 2, 'red', 0, 4)
# car2 = VerCar(2, 3, 'purple', 0, 0)
# car3 = HorCar(3, 3, 'yellow', 1, 0)
# car4 = VerCar(4, 3, 'gray', 4, 0)
# car5 = HorCar(5, 2, 'blue', 2, 1)
# car6 = HorCar(6, 2, 'green', 5, 1)
# car7 = VerCar(7, 2, 'orange', 1, 2)
# car8 = HorCar(8, 2, 'black', 2, 2)
# car9 = HorCar(9, 3, 'yellow', 5, 2)
# car10 = VerCar(10, 3, 'yellow', 3, 3)
# car11 = HorCar(11, 2, 'pink', 4, 3)
# car12 = HorCar(12, 2, 'brown', 6, 3)
# car13 = VerCar(13, 2, 'blue', 2, 4)
# car14 = VerCar(14, 2, 'orange', 4, 5)
# car15 = VerCar(15, 2, 'pink', 5, 5)
# car16 = HorCar(16, 3, 'gray', 6, 5)
# car17 = VerCar(17, 2, 'black', 0, 6)
# car18 = HorCar(18, 2, 'green', 2, 6)
# car19 = HorCar(19, 2, 'purple', 7, 6)
# car20 = HorCar(20, 3, 'yellow', 1, 7)
# car21 = VerCar(21, 2, 'green', 4, 7)
# car22 = HorCar(22, 2, 'orange', 5, 7)
# car23 = VerCar(23, 2, 'blue', 7, 7)
# car24 = HorCar(24, 2, 'blue', 0, 8)
# car25 = HorCar(25, 2, 'pink', 2, 8)
# car26 = VerCar(26, 3, 'purple', 8, 1)
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)
# cars_objects.append(car10)
# cars_objects.append(car11)
# cars_objects.append(car12)
# cars_objects.append(car13)
# cars_objects.append(car14)
# cars_objects.append(car15)
# cars_objects.append(car16)
# cars_objects.append(car17)
# cars_objects.append(car18)
# cars_objects.append(car19)
# cars_objects.append(car20)
# cars_objects.append(car21)
# cars_objects.append(car22)
# cars_objects.append(car23)
# cars_objects.append(car24)
# cars_objects.append(car25)
# cars_objects.append(car26)

##############################################################################
# The 12x12 configuration
# Fastest time so far:
##############################################################################
# car1 = HorCar(1, 2, 'red', 2, 6)
# car2 = HorCar(2, 2, 'green', 1, 0)
# car3 = HorCar(3, 3, 'yellow', 3, 0)
# car4 = VerCar(4, 3, 'gray', 6, 0)
# car5 = HorCar(5, 2, 'blue', 7, 0)
# car6 = VerCar(6, 2, 'pink', 9, 0)
# car7 = VerCar(7, 3, 'purple', 10, 0)
# car8 = VerCar(8, 2, 'pink', 11, 0)
# car9 = VerCar(9, 2, 'blue', 2, 2)
# car10 = HorCar(10, 3, 'yellow', 3, 2)
# car11 = HorCar(11, 2, 'green', 8, 2)
# car12 = VerCar(12, 2, 'black', 11, 2)
# car13 = HorCar(13, 2, 'orange', 0, 3)
# car14 = HorCar(14, 3, 'purple', 3, 3)
# car15 = VerCar(15, 3, 'black', 6, 3)
# car16 = HorCar(16, 3, 'pink', 7, 3)
# car17 = HorCar(17, 3, 'yellow', 0, 4)
# car18 = VerCar(18, 2, 'pink', 3, 4)
# car19 = HorCar(19, 2, 'green', 4, 4)
# car20 = VerCar(20, 3, 'blue', 7, 4)
# car21 = VerCar(21, 2, 'gray', 9, 4)
# car22 = HorCar(22, 2, 'orange', 10, 4)
# car23 = HorCar(23, 3, 'brown', 0, 5)
# car24 = VerCar(24, 2, 'orange', 4, 5)
# car25 = VerCar(25, 2, 'pink', 5, 5)
# car26 = HorCar(26, 2, 'green', 10, 5)
# car27 = VerCar(27, 3, 'purple', 0, 6)
# car28 = VerCar(28, 3, 'yellow', 1, 6)
# car29 = HorCar(29, 3, 'brown', 2, 7)
# car30 = VerCar(30, 2, 'green', 5, 7)
# car31 = VerCar(31, 3, 'yellow', 6, 7)
# car32 = HorCar(32, 3, 'purple', 7, 7)
# car33 = HorCar(33, 2, 'orange', 7, 8)
# car34 = HorCar(34, 2, 'pink', 9, 8)
# car35 = HorCar(35, 3, 'gray', 0, 9)
# car36 = HorCar(36, 2, 'orange', 3, 9)
# car37 = VerCar(37, 2, 'pink', 5, 9)
# car38 = HorCar(38, 2, 'green', 7, 9)
# car39 = VerCar(39, 2, 'orange', 10, 9)
# car40 = VerCar(40, 2, 'blue', 11, 9)
# car41 = VerCar(41, 2, 'green', 0, 10)
# car42 = VerCar(42, 2, 'blue', 6, 10)
# car43 = HorCar(43, 3, 'purple', 7, 11)
# car44 = HorCar(44, 2, 'pink', 10, 11)
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)
# cars_objects.append(car6)
# cars_objects.append(car7)
# cars_objects.append(car8)
# cars_objects.append(car9)
# cars_objects.append(car10)
# cars_objects.append(car11)
# cars_objects.append(car12)
# cars_objects.append(car13)
# cars_objects.append(car14)
# cars_objects.append(car15)
# cars_objects.append(car16)
# cars_objects.append(car17)
# cars_objects.append(car18)
# cars_objects.append(car19)
# cars_objects.append(car20)
# cars_objects.append(car21)
# cars_objects.append(car22)
# cars_objects.append(car23)
# cars_objects.append(car24)
# cars_objects.append(car25)
# cars_objects.append(car26)
# cars_objects.append(car27)
# cars_objects.append(car28)
# cars_objects.append(car29)
# cars_objects.append(car30)
# cars_objects.append(car31)
# cars_objects.append(car32)
# cars_objects.append(car33)
# cars_objects.append(car34)
# cars_objects.append(car35)
# cars_objects.append(car36)
# cars_objects.append(car37)
# cars_objects.append(car38)
# cars_objects.append(car39)
# cars_objects.append(car40)
# cars_objects.append(car41)
# cars_objects.append(car42)
# cars_objects.append(car43)
# cars_objects.append(car44)

##############################################################################
# Our first simple test case
# Configuration is easily solvable
##############################################################################
# car1 = HorCar(1, 2, 0, 3)
# car2 = VerCar(2, 2, 1, 1)
# car3 = VerCar(3, 3, 3, 3)
# car4 = VerCar(4, 3, 5, 3)
# car5 = HorCar(5, 3, 3, 2)
#
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)


room = RectangularRoom(size, size)
def won(lis):
    """
    Argument is a board configuration
    """

    if size == 6:
        row = lis[12:18]
    elif size == 9:
        row = lis[36:45]

    boolie = True
    index = 0

    for i in xrange(len(row)):
        if row[i] == 1:
            index = i
            break

    for i in xrange(index, len(row)):
        if row[i] > 1:
            boolie = False
            break


    return boolie


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
    Very simple A-Star function. Cost is a value calculated by the amount of cars in front
    of the red one. If there are no cars in front of the red car, cost = 0.
    If there is one car in front of red, cost = 1, etc.
    """
    if size == 6:
        row = lis[12:18]
    elif size == 9:
        row = lis[36:45]
    place_of_red = 0

    # determine where red car is placed
    for i in xrange(len(row)):
        if row[i] == 1:
            place_of_red = i
            break

    # determine how many cars are in front of red
    check_lis = []
    for i in xrange(place_of_red, len(row)):
        if row[i] > 1:
            if row[i] not in check_lis:
                check_lis.append(row[i])

    # cost is simply amount cars in front of red
    cost = len(check_lis)

    return cost

def astar_solve():
    archive = {}

    # creating a PriorityQueue
    q1 = Queue.PriorityQueue()

    # returns a 1d list of the board, I thought this would be faster
    one_d_list = room.board()

    # In the PriorityQueue a tuple would be placed, first element of this tuple is the cost(calculated by a_star),
    # second element is the configuration, for the first configuration I just gave it a cost of 0
    q1.put((0, one_d_list))
    check = True
    starter = tuple(one_d_list)

    archive[starter] = []

    while check:
        if q1.qsize() == 0:
            return False
            break

        # unpack the queue, it is a tuple, because it is a PriorityQueue it gets an element with lowest cost first
        cost, config_1d = q1.get()

        room.set_board(config_1d)

        for car in cars_objects:

            if car.updatePosition(1) and check:

                one_d_list = room.board()

                tupletje = tuple(one_d_list)
                if tupletje not in archive:

                    if (won(one_d_list)):
                        room.set_board(one_d_list)
                        archive[tuple(config_1d)].append(tupletje)
                        ender = tupletje
                        return find_path(archive, starter, ender)
                        check = False
                        break

                    archive[tuple(config_1d)].append(tupletje)
                    archive[tupletje] = []

                    # put the tuple element in the queue, wehere first element is the cost of the configuration
                    q1.put((a_star(one_d_list), one_d_list))


                car.updatePosition(-1)
            if car.updatePosition(-1) and check:
                one_d_list = room.board()

                tupletje = tuple(one_d_list)
                if tupletje not in archive:

                    if (won(one_d_list)):
                        room.set_board(one_d_list)
                        archive[tuple(config_1d)].append(tupletje)
                        ender = tupletje
                        return find_path(archive, starter, ender)
                        check = False
                        break

                    archive[tuple(config_1d)].append(tupletje)
                    archive[tupletje] = []

                    # put the tuple element in the queue, wehere first element is the cost of the configuration
                    q1.put((a_star(one_d_list), one_d_list))
                car.updatePosition(1)
    return True


def breadth_solve():
    archive = {}
    q1 = Queue.Queue()
    one_d_list = room.board()
    q1.put(one_d_list)
    check = True
    starter = tuple(one_d_list)
    archive[starter] = []

    while check:


        config_1d = q1.get()

        room.set_board(config_1d)

        for car in cars_objects:

            if car.updatePosition(1) and check:

                one_d_list = room.board()

                tupletje = tuple(one_d_list)

                if tupletje not in archive:

                    if (won(one_d_list)):
                        room.set_board(one_d_list)
                        archive[tuple(config_1d)].append(tupletje)
                        ender = tupletje
                        return find_path(archive, starter, ender)
                        check = False
                        break

                    archive[tuple(config_1d)].append(tupletje)
                    archive[tupletje] = []
                    q1.put(one_d_list)
                car.updatePosition(-1)

            if car.updatePosition(-1) and check:
                one_d_list = room.board()

                tupletje = tuple(one_d_list)
                if tupletje not in archive:

                    if (won(one_d_list)):
                        room.set_board(one_d_list)
                        archive[tuple(config_1d)].append(tupletje)
                        ender = tupletje
                        return find_path(archive, starter, ender)
                        check = False
                        break

                    q1.put(one_d_list)
                    archive[tuple(config_1d)].append(tupletje)
                    archive[tupletje] = []
                car.updatePosition(1)
    return True

def printboard():
    # os.system('cls')
    # for i in range(size):
    #     for j in range(size):
    #         print room.board_configuration[i][j],
    #     print "\n"
    fig = plt.figure('Rush Hour')
    plotboard = [[], []]
    for i in range(size + 1):
        plotboard[0].append([i] * (size + 1))
        plotboard[1].append(i)
    for i in range(size):
        plt.plot(plotboard[0][i],plotboard[1],  color='black')
        plt.plot(plotboard[1], plotboard[0][i], color='black')
    for i in range(size):
        for j in range(size):
            num = room.board_configuration[i][j]
            if num > 0:
                plt.plot(j + 0.5, size - 1 - i + 0.5, 's',color=cars_objects[num - 1].color, markersize = 300/size)


if __name__ == "__main__":
    printboard()
    plt.show()
    while (1):
        print ''
        num = raw_input('code: ')
        os.system('cls')
        print ''

        # if user types in God for auto solver
        if num == 'astar':
            # start timer (wall clock time)
            start = time.time()
            print "Solving..."
            lijst = astar_solve()
            end = time.time()
            print "Time elapsed:", (end - start)
            print "Amount steps:", len(lijst)

            print "Winning Configuration"
            for k in range(len(lijst)):
                x = lijst[k]
                room.set_board(x)
                printboard()
                plt.draw()
                plt.pause(0.01)
                plt.clf()
            break

        elif num == 'breadth':
            # start timer (wall clock time)
            start = time.time()
            print "Solving..."
            lijst = breadth_solve()
            end = time.time()
            print "Time elapsed:", (end - start)
            print "Amount steps:", len(lijst)

            print "Winning Configuration"
            for k in range(len(lijst)):
                x = lijst[k]
                room.set_board(x)
                printboard()
                plt.draw()
                plt.pause(0.01)
                plt.clf()
            break
        print''

    printboard()
    plt.show()
