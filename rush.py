# Problem Set 6: Simulating robots
# Name: Jan Huiskes
#
# Simulates robots cleaning a room with dirty tiles

import math
import random

import workshop3_visualize
import pylab




class RectangularRoom(object):

    def __init__(self, width, height):

        self.height = height
        self.width = width
        self.tiles = []

        for i in range(width):
            for j in range(height):
                self.tiles.append([i, j]])

    def isPositionInRoom(self, pos):

        x = pos[0]
        y = pos[1]
        if x <= self.width and x >= 0 and y <= self.height and y >= 0:
            return True
        else:
            return False

    def winningRow(self):

        winrow = self.height / 2
        return winrow




class Car(object):

    def __init__(self, room, direction, length, startpos):

        self.room = room
        self.direction = direction
        self.pos = []
        self.x = startpos[0]
        self.y = startpos[1]
        self.length = length
        if self.direction == 0:
            for i in range(self.length):
                self.pos.append([self.x + i, self.y])
        else:
            for i in range(self.length):
                self.pos.append([self.x, self.y + i])




    def setRobotPosition(self, position):

        self.position = position


    def updatePositionAndClean(self):

        # For a robot that keeps going in the same direction
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        setRobotPosition(new_pos)
        x = int(new_pos.getX())
        y = int(new_pos.getY())
        # The tile must be dirty in order to clean
        if self.room.isTileCleaned(x, y) == False:
                self.room.cleanTileAtPosition(self.position)



# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import random
# import math
# import time
#
# #define constant iron
# k = 1.381*(10**(-23))
# e = 2.72*k/4
#
# def ronde_flip(veld,kolommen,rijen,T):
#     for u in range(kolommen):
#         j = random.randint(0,rijen-1)
#         i = random.randint(0,kolommen-1)
#         tot_spin = veld[(j+1)%rijen][i] + veld[(j-1)%rijen][i] + veld[j][(i+1)%kolommen] + veld[j][(i-1)%kolommen]
#         delta_u = veld[j][i]*2*tot_spin * e
#
#         if delta_u <= 0:
#             veld[j][i] = - veld[j][i]
#
#         elif delta_u > 0:
#             randomgetal = random.random()
#             kansgetal = math.e**(-delta_u/(k*T))
#             if randomgetal <= kansgetal:
#                 veld[j][i] = -veld[j][i]
#
#
# def veld_simulatie(rijen,kolommen, aantal_stappen,T,T_string):
#     veld = [[0 for i in range(kolommen)] for i in range(rijen)]
#     down_punten = [[],[]]
#     up_punten = [[],[]]
#
#     for j in range(rijen):
#         for i in range(kolommen):
#             kans = random.random()
#             if kans < 0.5:
#                 veld[j][i] = -1
#                 down_punten[0].append(j)
#                 down_punten[1].append(i)
#             else:
#                 veld[j][i] = 1
#                 up_punten[0].append(j)
#                 up_punten[1].append(i)
#
#     plt.figure('Ising model (%s bij %s) en %s'%(rijen,kolommen,T_string))
#     plt.plot(down_punten[0],down_punten[1],'.',color='orange')
#     plt.plot(up_punten[0],up_punten[1],'.',color='blue')
#     for x in range(aantal_stappen*5):
#         plt.clf()
#         ronde_flip(veld,rijen,kolommen,T)
#         down_punten = [[],[]]
#         up_punten = [[],[]]
#         plt.tick_params(
#                 axis='both',
#                 which='both',
#                 bottom='off',
#                 top='off',
#                 labelbottom='off',
#                 labelleft='off')
#         plt.axis([-1, kolommen, -1, rijen])
#
#         for j in range(rijen):
#             for i in range(kolommen):
#                 if veld[j][i] < 0:
#                     down_punten[0].append(j)
#                     down_punten[1].append(i)
#                 else:
#                     up_punten[0].append(j)
#                     up_punten[1].append(i)
#         plt.title("Na %s stappen \n Aantal up = %s, aantal down = %s" % (x *kolommen,len(up_punten[0]),len(down_punten[0])))
#         plt.plot(down_punten[0],down_punten[1],'s',color='orange',markeredgecolor='orange',markeredgewidth=1)
#         plt.plot(up_punten[0],up_punten[1],'s',color='blue',markeredgecolor='blue',markeredgewidth=1)
#         plt.pause(0.01)
#
# veld_simulatie(50,50,100,0.01,'T < Tc')
# veld_simulatie(50,50,20,2.72,'T = Tc')
# veld_simulatie(50,50,20,5,'T > Tc')
