# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration

import math
import random
import os
import time

# Note for improvement:
# Maybe, just maybe it takes so long because I may check same steps more than
# once, not sure though, and of course I am taking many unnecessary steps because
# it is brute force

class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width

    def isPositionInRoom(self, pos):

        x = pos[0]
        y = pos[1]

        return x < self.width and x >= 0 and y < self.height and y >= 0

# saving every car object of the board
cars_objects = []

class Car(object):
    def __init__(self, room, length):
        self.room = room
        self.length = length

class HorCar(Car):
    def __init__(self, room, length, startpos):
        Car.__init__(self, room, length)
        x = startpos[0]
        y = startpos[1]

        self.all_positions_of_car = []

        for i in range(self.length):
            self.all_positions_of_car.append([x + i, y])

    def setCarPosition(self, position):
        x = position[0]
        y = position[1]
        for i in range(self.length):
            self.all_positions_of_car[i][0] = x + i
            self.all_positions_of_car[i][1] = y

    def noCar(self, new_start_or_end_position):

        for car in cars_objects:
            if car != self:
                if new_start_or_end_position in car.all_positions_of_car:
                    return False

        return True

    def updatePosition(self, step):

        new_xstart = self.all_positions_of_car[0][0] + step
        new_ystart = self.all_positions_of_car[0][1]

        new_start = [new_xstart, new_ystart]

        new_xend = self.all_positions_of_car[-1][0] + step
        new_yend = self.all_positions_of_car[-1][1]

        new_end = [new_xend, new_yend]

        if self.room.isPositionInRoom(new_start) and self.room.isPositionInRoom(new_end) and self.noCar(new_start) and self.noCar(new_end):
            self.setCarPosition(new_start)
            return True

        return False

class VerCar(Car):
    def __init__(self, room, length, startpos):
        Car.__init__(self, room, length)

        x = startpos[0]
        y = startpos[1]

        self.all_positions_of_car = []

        for i in range(self.length):
            self.all_positions_of_car.append([x, y + i])

    def setCarPosition(self, position):
        x = position[0]
        y = position[1]
        for i in range(self.length):
            self.all_positions_of_car[i][0] = x
            self.all_positions_of_car[i][1] = y + i

    def noCar(self, new_start_or_end_position):
        for car in cars_objects:
            if car != self:
                if new_start_or_end_position in car.all_positions_of_car:
                    return False
        return True

    def updatePosition(self, step):

        new_xstart = self.all_positions_of_car[0][0]
        new_ystart = self.all_positions_of_car[0][1] + step

        new_start = [new_xstart, new_ystart]

        new_xend = self.all_positions_of_car[-1][0]
        new_yend = self.all_positions_of_car[-1][1] + step

        new_end = [new_xend, new_yend]

        if self.room.isPositionInRoom(new_start) and self.room.isPositionInRoom(new_end) and self.noCar(new_start) and self.noCar(new_end):
            self.setCarPosition(new_start)
            return True

        return False

size = 6
room = RectangularRoom(size, size)


# first configuration
## Comment this whole block out for testing the first configuration
## You have to probably wait a few weeks though
###############################################################################
# car1 = HorCar(room, 2, [3, 3])
# car2 = VerCar(room, 2, [0, 0])
# car3 = HorCar(room, 2, [1, 1])
# car4 = HorCar(room, 2, [4, 0])
# car5 = HorCar(room, 2, [4, 2])
# car6 = HorCar(room, 2, [3, 5])
# car7 = VerCar(room, 3, [3, 0])
# car8 = VerCar(room, 3, [2, 3])
# car9 = VerCar(room, 3, [5, 3])
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
###############################################################################

## This is the test case for iterative_deepening, this works well, but
# configuration are easy solvable
car1 = HorCar(room, 2, [0, 3])
car2 = VerCar(room, 2, [1, 1])
car3 = VerCar(room, 3, [3, 3])
car4 = VerCar(room, 3, [5, 3])
car5 = HorCar(room, 3, [3, 2])

cars_objects.append(car1)
cars_objects.append(car2)
cars_objects.append(car3)
cars_objects.append(car4)
cars_objects.append(car5)


def won():
    """
    Different won function than Jan's.
    """

    # x_red and y_red are determined by which index you put the red car into
    # cars_objects list
    x_red = cars_objects[0].all_positions_of_car[0][0]
    y_red = cars_objects[0].all_positions_of_car[0][1]

    for i in range(x_red + 2, size):
        for car in cars_objects:
            if car != cars_objects[0]:
                if [i, y_red] in car.all_positions_of_car:
                    return False
    return True

def iterative_deepening():
    continue_different_function = False
    # from literature, hardest 6x6 puzzle configurarion can be solved in 93 steps
    for i in range(1, 94):

        if recursive(1, i):
            continue_different_function = True
            print "Amount steps:", i

            break

    return continue_different_function

# the last configurarion of a solvable configuration
last_config_list = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

def recursive(index, depth):
    continue_game_iterative = False
    no_more = False
    for car in cars_objects:
        if car.updatePosition(1) and no_more == False:

            if index == depth:
                if won():

                    # allright this is ugly, but purpose of this whole block
                    # is to append the last configuration list for printing
                    # purposes, you can skip this if you just wanna comprehend
                    # the iterative_deepening method
                    ##########################################################
                    all_positions = []
                    for cars in cars_objects:
                        all_positions.append(cars.all_positions_of_car)

                    for j in range(size - 1, -1, -1):
                        for i in range(size):

                            for k in range(len(all_positions)):
                                if [i, j] in all_positions[k]:
                                    last_config_list[size - 1 - j][i] = (k + 1)

                                    break
                    ##########################################################
                    continue_game_iterative = True
                    no_more = True
                    break
            else:
                if recursive(index + 1, depth):
                    continue_game_iterative = True
                    no_more = True

            car.updatePosition(-1)

        if car.updatePosition(-1) and no_more == False:

            if index == depth:
                if won():

                    # skip this block if you just wanna comprehend the iterative_deepening
                    # method
                    ##########################################################
                    all_positions = []
                    for cars in cars_objects:
                        all_positions.append(cars.all_positions_of_car)

                    for j in range(size - 1, -1, -1):
                        for i in range(size):

                            for k in range(len(all_positions)):
                                if [i, j] in all_positions[k]:
                                    last_config_list[size - 1 - j][i] = (k + 1)

                                    break
                    #########################################################
                    continue_game_iterative = True
                    no_more = True
                    break
            else:
                if recursive(index + 1, depth):
                    no_more = True
                    continue_game_iterative = True

            car.updatePosition(1)
    return continue_game_iterative


def printboard():
    all_positions = []
    for cars in cars_objects:
        all_positions.append(cars.all_positions_of_car)

    for j in range(size - 1, -1, -1):
        for i in range(size):
            check = True
            for k in range(len(all_positions)):
                if [i, j] in all_positions[k]:
                    print (k + 1),
                    check = False
                    break
            if check:
                print '_',
        print ''


continue_game = True
while (continue_game):
    printboard()
    print ''
    num = raw_input('+car_num = up/right, -car_num = down/left: ')
    os.system('cls')
    print ''

    # GOD has three characters..so I was assuming everything else is a number
    if len(num) < 3:
        num = int(num)
    # if user types in God for auto solver
    if num == 'GOD':
        # start timer (wall clock time)
        start = time.time()
        print "Solving..."
        boolie = iterative_deepening()
        if boolie == True:
            end = time.time()
            print "Time elapsed:", (end - start)
            print "Amount cars:", len(cars_objects)

        # printing the last configuration (the solved one)
        for i in last_config_list:
            print i, '\n'

        continue_game = False


    elif abs(num) > len(cars_objects):
        print 'Invalid move'
    else:
        if num > 0:
            print cars_objects[num -1].updatePosition(1)
            if won():
                continue_game = False
        if num < 0:
            print cars_objects[num*-1 - 1].updatePosition(-1)
            if won():
                continue_game = False

    print''

print "You win !!!!!!!!!!!!!!!"
