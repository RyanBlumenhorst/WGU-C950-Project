# Ryan Blumenhorst
# Student ID: 002094804
import Packages
import datetime


class Truck:
    # Constructor Method for a Truck object. Capacity is the maximum amount of packages a truck can hold,
    # Speed is the average speed of the truck, Load is the current amount of packages in the truck,
    # packages is a list of all the packages in the truck, curr_address is the index of the current address of
    # the truck, and time keeps track of the time that the truck leaves and the new time after delivering a package.
    def __init__(self, capacity=16, speed=18, load=0, packages=[], curr_address=0, time=[]):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.curr_address = curr_address
        self.time = time

