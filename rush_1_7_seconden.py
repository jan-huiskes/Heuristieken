# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration

import math
import random
import os
import time
import Queue
import hashlib

"""
Snelste tijd tot nu toe: 1.7 seconden (op mijn laptop)
Veranderingen:
    - archive is een dictionary
    - Queue is geimporteerd
    - board-functie stukken sneller
    - hier aan daar heb ik geprobeerd zo min mogelijk elementen uit lijsten te halen, dus gwn in 1 keer element doorgeven aan functies


Notities:
De functie board() deed er aanvankelijk heel langzaam over omdat ie eerst
alle posities uit de autos haalde en dan het bord vulde. De nieuwe board-functie pakt
nu gwn de startposities van de autos en vult dan deze aan in het zelfde
board-functie afhankelijk van de orientatie van de auto, alle autos hebben nu
ook een orientatie attribuut: 'h' of 'v', (horizontaal of verticaal).

Als je cProfile uitvoert dan merk je op dat er nog veel tijdwinst te boeken
valt in de updatePosition en setCarPosition van zowel de horizontale autos
als de verticale autos. Ik dacht er zelf aan om in de klasse RectangularRoom een
board aan te maken op de zelfde manier als de board-functie, dus dat je werkt
met startposities. Dan kunnen updatePosition en setCarPosition ook korter omdat
je dan alleen hoeft te werken met startposities en dan hoef je niet alle posities van
een auto bij te houden in dat auto object zelf. En voor de noCar functie hoef je dan
alleen een if statement te plaatsen van: if board[newstart_y][newstart_x] == 0: return True.

En misschien is het niet nodig om elke auto dat volledige room object mee te geven.
Dat moet er eigenlijk los van af staan. Om onder die 1.7 seconden te komen zal
structuur van de code gwn anders moeten vrees ik :( (niet drastisch hoor)
"""


class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width

    def isPositionInRoom(self, x, y):

        return x < self.width and x >= 0 and y < self.height and y >= 0

# saving every car object of the board
cars_objects = []

class Car(object):
    def __init__(self, room, length):
        self.room = room
        self.length = length

class HorCar(Car):
    def __init__(self, room, length, x, y):
        Car.__init__(self, room, length)
        self.direction = 'h'
        #x = startpos[0]
    #    y = startpos[1]

        self.all_positions_of_car = []

        for i in xrange(self.length):
            self.all_positions_of_car.append([x + i, y])

    def setCarPosition(self, x, y):
        for i in xrange(self.length):
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

        new_xend = new_xstart + self.length - 1
        new_yend = new_ystart

        new_end = [new_xend, new_yend]

        if self.room.isPositionInRoom(new_xstart, new_ystart):
            if self.room.isPositionInRoom(new_xend, new_yend):
                if self.noCar(new_start):
                    if self.noCar(new_end):
                        self.setCarPosition(new_xstart, new_ystart)
                        return True

        return False

class VerCar(Car):
    def __init__(self, room, length, x, y):
        Car.__init__(self, room, length)
        self.direction = 'v'

    #    x = startpos[0]
    #    y = startpos[1]

        self.all_positions_of_car = []

        for i in xrange(self.length):
            self.all_positions_of_car.append([x, y + i])

    def setCarPosition(self, x, y):
        for i in xrange(self.length):
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

        new_xend = new_xstart
        new_yend = new_ystart + self.length - 1

        new_end = [new_xend, new_yend]

        if self.room.isPositionInRoom(new_xstart, new_ystart):
            if self.room.isPositionInRoom(new_xend, new_yend):
                if self.noCar(new_start):
                    if self.noCar(new_end):
                        self.setCarPosition(new_xstart, new_ystart)
                        return True

        return False


size = 6
room = RectangularRoom(size, size)


# first configuration
## Comment this whole block out for testing the first configuration
## You have to probably wait a few weeks though
###############################################################################
car1 = HorCar(room, 2, 3, 3)
car2 = VerCar(room, 2, 0, 0)
car3 = HorCar(room, 2, 1, 1)
car4 = HorCar(room, 2, 4, 0)
car5 = HorCar(room, 2, 4, 2)
car6 = HorCar(room, 2, 3, 5)
car7 = VerCar(room, 3, 3, 0)
car8 = VerCar(room, 3, 2, 3)
car9 = VerCar(room, 3, 5, 3)

cars_objects.append(car1)
cars_objects.append(car2)
cars_objects.append(car3)
cars_objects.append(car4)
cars_objects.append(car5)
cars_objects.append(car6)
cars_objects.append(car7)
cars_objects.append(car8)
cars_objects.append(car9)
###############################################################################

## This is a simple test case, configuration are easy solvable
# car1 = HorCar(room, 2, [0, 3])
# car2 = VerCar(room, 2, [1, 1])
# car3 = VerCar(room, 3, [3, 3])
# car4 = VerCar(room, 3, [5, 3])
# car5 = HorCar(room, 3, [3, 2])
#
# cars_objects.append(car1)
# cars_objects.append(car2)
# cars_objects.append(car3)
# cars_objects.append(car4)
# cars_objects.append(car5)


def won(lis):
    """
    Argument is a board configuration
    """
    row = lis[int(round(room.height / 2 - 1))]

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



def board():
    # makes matrix

    # hieronder met comprehensive listing is mooier kwa design, maar...
    #board = [[0 for x in xrange(size)] for x in xrange(size)]

    # ...hardcoding is sneller
    board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

    count = 1
    for cars in cars_objects:
        if cars.direction == 'h':
            x = cars.all_positions_of_car[0][0]
            y = cars.all_positions_of_car[0][1]
            for i in xrange(cars.length):
                board[y][x + i] = count

        else:
            x = cars.all_positions_of_car[0][0]
            y = cars.all_positions_of_car[0][1]
            for i in xrange(cars.length):
                board[y + i][x] = count
        count += 1

    return board

def makeBoard(lis):
    check_lis = []
    for i in xrange(size - 1, -1, -1):
        for j in xrange(size):
            if lis[i][j] > 0 and lis[i][j] not in check_lis:
                check_lis.append(lis[i][j])
                cars_objects[lis[i][j] - 1].setCarPosition(j, size - 1 - i)


winning_config = []
def solve():
    archive = {}

    q1 = Queue.Queue()
    lis = board()
    q1.put(lis)
    check = True

    # size = 6, but now hardcoded
    tmp_list = [lis[i][j] for i in xrange(6) for j in xrange(6)]

    archive[tuple(tmp_list)] = 1

    while check:

        config = q1.get()

        makeBoard(config)


        for car in cars_objects:

            if car.updatePosition(1) and check:
                lis = board()


                tmp_list = [lis[i][j] for i in xrange(6) for j in xrange(6)]


                tupletje = tuple(tmp_list)
                if tupletje not in archive:

                    if (won(lis)):
                        winning_config.append(lis)
                        check = False
                        break

                    archive[tupletje] = None
                    q1.put(lis)
                car.updatePosition(-1)
            if car.updatePosition(-1) and check:
                lis = board()

                tmp_list = [lis[i][j] for i in xrange(6) for j in xrange(6)]

                tupletje = tuple(tmp_list)
                if tupletje not in archive:

                    if (won(lis)):
                        winning_config.append(lis)
                        check = False
                        break

                    q1.put(lis)
                    archive[tupletje] = None
                car.updatePosition(1)

    return True

def printboard():
    all_positions = []
    for cars in cars_objects:
        all_positions.append(cars.all_positions_of_car)

    for j in xrange(size - 1, -1, -1):
        for i in xrange(size):
            check = True
            for k in xrange(len(all_positions)):
                if [i, j] in all_positions[k]:
                    print (k + 1),
                    check = False
                    break
            if check:
                print '_',
        print ''

if __name__ == "__main__":
    while (1):
        lis = board()

        if won(lis):
            break

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
            boolie = solve()
            if boolie == True:
                end = time.time()
                print "Time elapsed:", (end - start)
                print "Amount cars:", len(cars_objects)

                win = winning_config[0]
                for i in win:
                    print i, "\n"
            else:
                print 'No solution'
            break


        elif abs(num) > len(cars_objects):
            print 'Invalid move'
        else:
            if num > 0:
                cars_objects[num - 1].updatePosition(1)
            if num < 0:
                cars_objects[num * -1 - 1].updatePosition(-1)

        print''

    print "You win !!!!!!!!!!!!!!!"
