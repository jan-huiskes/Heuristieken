# Problem Set 6: Simulating robots
# Name: Jan Huiskes
#
# Simulates robots cleaning a room with dirty tiles

import math
import random

import workshop3_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, stepsx, stepsy):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY())
        # Add that to the existing position
        new_x = old_x + stepsx
        new_y = old_y + stepsy
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0

        dictionary with the tiles. 1 is for dirty and 0 for clean
        """
        self.height = height
        self.width = width
        self.tiles = []

        # For loop to add the coordinates (in a list) to the list of dirty tiles
        for i in range(width):
            for j in range(height):
                self.tiles.append([i, j]])

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        # Conditions for being in the room
        if x <= self.width and x >= 0 and y <= self.height and y >= 0:
            return True
        else:
            return False

    def winningRow(self):
        winrow = self.height / 2 + 1
        return winrow




class Car(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """

        self.room = room
        # Make integer from float
        x = int(self.position.getX())
        y = int(self.position.getY())
        # For multiple robots that start on the same tile, the tile must be dirty in order to clean
        if self.room.isTileCleaned(x, y) == False:
                self.room.cleanTileAtPosition(self.position)


    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position


    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position


    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # For a robot that keeps going in the same direction
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        setRobotPosition(new_pos)
        x = int(new_pos.getX())
        y = int(new_pos.getY())
        # The tile must be dirty in order to clean
        if self.room.isTileCleaned(x, y) == False:
                self.room.cleanTileAtPosition(self.position)



# === Problem 2
class Truck(Car):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        # Checks if new position in room else go a different direction
        if self.room.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
            x = int(new_pos.getX())
            y = int(new_pos.getY())
            # The tile must be dirty in order to clean
            if self.room.isTileCleaned(x, y) == False:
                    self.room.cleanTileAtPosition(self.position)
        else:
            self.setRobotDirection((random.random() * 360))

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    room = RectangularRoom(width, height)
    robots = []
    # Put the number of robots in the list
    for i in range(num_robots):
        robots.append(robot_type(room, speed))
    # Total timesteps to clean
    count = 0
    anim = workshop3_visualize.RobotVisualization(num_robots, width, height, 0.2)
    # Loops over the number of trials. Count +1 if the min_coverage isn't reach and break if done
    for i in range(num_trials):
        anim.update(room, robots)
        if (float(room.getNumCleanedTiles()) / room.getNumTiles()) < min_coverage:
            count += 1
        else:
            count += 1
            break
        # Loops over all robots, so they will update and clean
        for j in range(len(robots)):
            robots[j].updatePositionAndClean()
    anim.done()
    return count

# === Problem 4

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        # Same as StandardRobot
        new_pos = self.position.getNewPosition(self.direction, self.speed)
        if self.room.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
            x = int(new_pos.getX())
            y = int(new_pos.getY())
            if self.room.isTileCleaned(x, y) == False:
                self.room.cleanTileAtPosition(self.position)
        else:
            self.setRobotDirection((random.random() * 360))
        # Change direction random
        self.setRobotDirection((random.random() * 360))

avg1 = runSimulation(5, 1.0, 10, 10, 0.8, 200, StandardRobot)
print avg1
avg2 = runSimulation(5, 1.0, 10, 10, 0.8, 200, RandomWalkRobot)
print avg2
