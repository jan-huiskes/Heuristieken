# Problem Set 6: Simulating robots
# Name: Jan Huiskes
#
# Simulates robots cleaning a room with dirty tiles

import math
import random
import os

class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width

    def isPositionInRoom(self, pos):

        x = pos[0]
        y = pos[1]

        return x < self.width and x >= 0 and y < self.height and y >= 0


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
            return 'Done'

        return 'Invalid move'

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
            return 'Done'

        return 'Invalid move'

size = 6
room = RectangularRoom(size, size)
car1 = VerCar(room, 2, [0, 0])
car2 = HorCar(room, 2, [1, 1])
car3 = VerCar(room, 3, [3, 0])
car4 = HorCar(room, 2, [4, 0])
car5 = VerCar(room, 1, [2, 3])
car6 = HorCar(room, 2, [3, 5])
car7 = VerCar(room, 1, [5, 3])
car8 = HorCar(room, 2, [3, 3])
car9 = HorCar(room, 2, [4, 2])

cars_objects.append(car1)
cars_objects.append(car2)
cars_objects.append(car3)
cars_objects.append(car4)
cars_objects.append(car5)
cars_objects.append(car6)
cars_objects.append(car7)
cars_objects.append(car8)
cars_objects.append(car9)

def won():

    x_red = cars_objects[7].all_positions_of_car[0][0]
    y_red = cars_objects[7].all_positions_of_car[0][1]

    for i in range(x_red + 2, size):
        for car in cars_objects:
            if car != cars_objects[7]:
                if [i, y_red] in car.all_positions_of_car:
                    return False
    return True

def printboard():
    for i in range(5, -1, -1):
        for j in range(6):
            check = True
            for k in range(len(cars_objects)):
                if [j, i] in cars_objects[k].all_positions_of_car:
                    print (k + 1),
                    check = False
            if (check):
                print '_',
        print''

continue_game = True
while (continue_game):
    printboard()
    print ''
    num = int(raw_input('+car_num = up/right, -car_num = down/left: '))
    os.system('cls')
    print ''
    if abs(num) >= 100: # len(cars_objects):
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
