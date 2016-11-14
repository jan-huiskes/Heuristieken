# Heuristic: Rush hour
# Contributors: Jan Huiskes, Boris Wolvers, Saar Hoek
#
# Solving any Rush Hour configuration


import os
import time
import Queue
import matplotlib.pyplot as plt


"""
Snelste tijd tot nu toe: 0.95 seconden (op mijn laptop)
Veranderingen:
    - Room object is aparte object
    - Bij vorige code steeds opnieuw een room aanmaken, nu alleen elementen aanpassen als auto wordt verplaatst

"""
# saving every car object of the board
cars_objects = []


class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width

        board_configuration = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

        count = 1
        for cars in cars_objects:
            if cars.direction == 'h':
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    board_configuration[5 - y][x + i] = count

            else:
                x = cars.startx
                y = cars.starty
                for i in xrange(cars.length):
                    board_configuration[5 -(y + i)][x] = count
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

        return [self.board_configuration[i][j] for i in xrange(6) for j in xrange(6)]


    def update_board_horizontal(self, x, y, length, index, step):

        for i in xrange(length):
            self.board_configuration[5 - y][x + i] = index

        if step == 1:
            self.board_configuration[5 - y][x - step] = 0
        else:
            self.board_configuration[5 - y][x + length] = 0

    def update_board_vertical(self, x, y, length, index, step):

        for i in xrange(length):
            self.board_configuration[5 -(y + i)][x] = index

        if step == 1:
            self.board_configuration[5 - (y - step)][x] = 0
        else:
            self.board_configuration[5 - (y + length)][x] = 0

    def set_board(self, set_configuration):

        lijstjes = [set_configuration[0:6], set_configuration[6:12], set_configuration[12:18], set_configuration[18:24], set_configuration[24:30], set_configuration[30:36] ]

        for j in xrange(6):
            for i in xrange(6):
                self.board_configuration[j][i] = lijstjes[j][i]

        check_lis = []
        for i in xrange(size - 1, -1, -1):
            for j in xrange(size):
                if lijstjes[i][j] > 0 and lijstjes[i][j] not in check_lis:
                    check_lis.append(lijstjes[i][j])
                    cars_objects[lijstjes[i][j] - 1].setCarPosition(j, size - 1 - i)



class Car(object):
    def __init__(self, index, length, color):

        self.index = index
        self.length = length
        self.color = color

class HorCar(Car):
    def __init__(self, index, length, color, x, y):
        Car.__init__(self, index, length, color)
        self.direction = 'h'
        self.startx = x
        self.starty = y


    def setCarPosition(self, x, y):
        self.startx = x
        self.starty = y

    def noCar(self, x, y):


        return room.board_configuration[5 - y][x] == 0 or room.board_configuration[5 - y][x] == self.index



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
        Car.__init__(self, index, length, color)
        self.direction = 'v'
        self.startx = x
        self.starty = y

    def setCarPosition(self, x, y):
        self.startx = x
        self.starty = y

    def noCar(self, x, y):

        return room.board_configuration[5 - y][x] == 0 or room.board_configuration[5 - y][x] == self.index


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


# first configuration
## Comment this whole block out for testing the first configuration
## You have to probably wait a few weeks though
###############################################################################
car1 = HorCar(1, 2, 'red', 3, 3)
car2 = VerCar(2, 2, 'brown', 0, 0)
car3 = HorCar(3, 2, 'blue', 1, 1)
car4 = HorCar(4, 2, 'green', 4, 0)
car5 = HorCar(5, 2, 'orange', 4, 2)
car6 = HorCar(6, 2, 'blue', 3, 5)
car7 = VerCar(7, 3, 'yellow', 3, 0)
car8 = VerCar(8, 3, 'purple', 2, 3)
car9 = VerCar(9, 3, 'brown', 5, 3)

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

size = 6
room = RectangularRoom(size, size)
def won(lis):
    """
    Argument is a board configuration
    """
    #row = lis[int(round(room.height / 2 - 1))]

    # Have to do this because lis is now a 1d array
    row = lis[12:18]

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


def solve():
    archive = {}
    q1 = Queue.Queue()

    # returns a 1d list of the board, I thought this would be faster
    one_d_list = room.board()


    q1.put(one_d_list)
    check = True
    starter = tuple(one_d_list)

    archive[starter] = []

    while check:



        # if q1.qsize() == 0:
        #     return False
        #     break
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

                #tmp_list = [lis[i][j] for i in xrange(6) for j in xrange(6)]

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
                car.updatePosition(1)



    return True

def printboard():
    os.system('cls')
    for i in range(6):
        for j in range(6):
            print room.board_configuration[i][j],
        print "\n"
   



if __name__ == "__main__":
    while (1):
        one_d_list = room.board()

        if won(one_d_list):
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
            lijst = solve()
            end = time.time()
            print "Time elapsed:", (end - start)
            print "Amount steps:", len(lijst)

            print "winning configuration"
            for item in lijst:
                x = item
                room.set_board(x)
                printboard()
                time.sleep(1)
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
