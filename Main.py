# Ryan Blumenhorst
# Student ID: 002094804

import Packages
import HashMap
import Truck
import csv
import datetime


# Loads the information from the package file and then assigns the packages to trucks based on special notes.
# Complexity is O(N)
def loadPackageData(filename, returntype):
    # Create Hash Table
    packageTable = HashMap.CreateHashMap(40)
    t1 = []     # Truck 1 package list
    t2 = []     # Truck 2 package list
    t3 = []     # Truck 3 package list

    # Open file
    file = open(filename)
    csvreader = csv.reader(file, delimiter=',')
    # Store headers of the file that we don't need
    headers = []
    headers = next(csvreader)
    # Create package objects from the package file
    for row in csvreader:
        id = int(row[0])
        add = row[1]
        city = row[2]
        state = row[3]
        zip = row[4]
        dt = row[5]
        weight = row[6]
        note = row[7]
        status = 'At Hub'
        delivered = datetime.timedelta(hours=0, minutes=0, seconds=0)

        value = Packages.Package(id, add, city, state, zip, dt, weight, note, status, delivered)
        if value not in packageTable.table:
            packageTable.insert(id, value)

        # Load Trucks based on special notes
        if value.id not in t1 and value.id not in t2 and value.id not in t3:
            # Package with wrong address, fixes address, then assigns it to truck 3, which won't leave until after the
            # address is fixed.
            if value.id == 9:
                value.add = '410 S State St'
                value.zip = '84111'
                t3.append(value)
            # Packages that must be delivered together all get assigned to truck 1.
            elif value.id == 13 or value.id == 14 or value.id == 15 or value.id == 16 or value.id == 19 or \
                    value.id == 20:
                t1.append(value)
            # Packages that are delayed or can only be on truck 2 are assigned to truck 2.
            elif 'Can only be' in value.note or 'Delayed' in value.note:
                t2.append(value)
            # Packages that have a specific delivery time are also assigned to truck 1.
            elif value.dt != 'EOD':
                t1.append(value)
            else:
                # Packages that don't have any special notes are assigned based on the current load of the trucks
                if '' in value.note:
                    if len(t1) < len(t2):
                        t1.append(value)
                    elif len(t2) < len(t3):
                        t2.append(value)
                    else:
                        t3.append(value)

    file.close()
    # Return type determines what is returned, the hash table or information on a truck's package list
    if returntype == "Hash":
        return packageTable
    if returntype == "t1":
        return t1
    if returntype == "t2":
        return t2
    if returntype == "t3":
        return t3


# Reads the distance information (below) and determines the distance from one address to the next.
# Complexity is O(1)
def distanceBetween(distanceData, add1, add2):
    if distanceData[add1][add2] is None:
        return distanceData[add2][add1]
    else:
        return distanceData[add1][add2]


# This is the main Greedy Algorithm to determine the shortest route for a truck to take.
# The parameters are the following:
#
#       1. distanceData is the distance information from below to determine distance from one address to the next.
#       2. addressData is the list of addresses and the indexes of the addresses based on the distance data.
#       3. truck is the current truck that the algorithm is working with.
#       4. totalMiles is the total count of the miles traveled for that truck, used to make the final count of
#       miles traveled.
#       5. packages is the list of packages associated with the truck that we are working with.
#
#    First, the algorithm checks to make sure that the list of packages has packages in it, if not it returns the empty
# list. If the list isn't empty, then we get the current address of the truck and save it to add1. then we go through
# all the packages in the package list and check the distance from the trucks current position to the address listed
# on the package. The algorithm will choose the shortest distance for the truck and set the address as the packages
# address, then remove the package(s) from the truck. Then, I update the package data to show the time that the package
# was delivered. Finally, I call the algorithm again with the shorter list and repeat the process, keeping track of the
# current time and miles traveled, until the list is empty.
#
# The complexity of the algorithm is O(N^2)
def minDistanceBetween(distanceData, addressData, truck, totalMiles, packages):
    if len(packages) == 0:
        return packages
    else:
        add1 = truck.curr_address
        add2 = 0
        minn = 50.0
        for p in packages:
            if float(distanceBetween(distanceData, add1, addressData.index([p.add]))) <= minn:
                minn = distanceBetween(distanceData, add1, addressData.index([p.add]))
                add2 = addressData.index([p.add])
                package = p

            totalMiles += minn

        truck.curr_address = add2
        totalMiles = totalMiles + minn
        # Calculate Time
        calc_time(truck, minn)
        # Update Package Hash Table
        delivery(truck, package)
        # Remove package from Truck
        packages.remove(package)
        # Run Minimum Distance with new Truck Address
        minDistanceBetween(distanceData, addressData, truck, totalMiles, packages)
        return totalMiles


# Updates the package hash table to show when the package was delivered
# Complexity is O(1)
def delivery(truck, package):
    p = packageHashTable.search(package.id)
    p.status = "Delivered at " + str(truck.time)
    p.delivered = truck.time


# Used to keep track of the current time after traveling to the new address. Takes the trucks average speed to find the
# amount of minutes traveled, then adds the minute to the trucks leaving time.
# Complexity is O(N)
def calc_time(truck, minn):
    truckTimes = []
    timeTraveled = minn / 18
    timeTraveled_minutes = '{0:02.0f}:{1:02.0f}'.format(*divmod(timeTraveled * 60, 60))
    final_time = timeTraveled_minutes + ':00'
    (h, m, s) = truck.time.split(':')
    curr_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    truckTimes.append(final_time)
    total = datetime.timedelta()
    for i in truckTimes:
        (h, m, s) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        total += d
    curr_time += total
    truck.time = str(curr_time)


# Main Program
packageDataFile = 'Data/WGUPS Package File.csv'     # CSV File of package information
# All the distance data from the WGUPS Distance file
distanceData = [
    [0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None],
    [7.2, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None],
    [3.8, 7.1, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None],
    [11, 6.4, 9.2, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [2.2, 6, 4.4, 5.6, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [3.5, 4.8, 2.8, 6.9, 1.9, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [10.9, 1.6, 8.6, 8.6, 7.9, 6.3, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [8.6, 2.8, 6.3, 4.0, 5.1, 4.3, 4, 0.0, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None],
    [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0.0, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [2.8, 6.3, 1.6, 7.3, 2.6, 1.5, 8.0, 9.3, 4.8, 0.0, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None],
    [6.4, 7.3, 10.4, 1.0, 6.5, 8.7, 8.6, 4.6, 11.9, 9.4, 0.0, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None],
    [3.2, 5.3, 3, 6.4, 1.5, 0.8, 6.9, 4.8, 4.7, 1.1, 7.3, 0, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None],
    [7.6, 4.8, 5.3, 11.1, 7.5, 4.5, 4.2, 7.7, 0.6, 5.1, 12, 4.7, 0, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None],
    [5.2, 3, 6.5, 3.9, 3.2, 3.9, 4.2, 1.6, 7.6, 4.6, 4.9, 3.5, 7.3, 0, None, None, None, None, None, None, None, None,
     None, None, None, None, None],
    [4.4, 4.6, 5.6, 4.3, 2.4, 3, 8, 3.3, 7.8, 3.7, 5.2, 2.6, 7.8, 1.3, 0, None, None, None, None, None, None, None,
     None, None, None, None, None],
    [3.7, 4.5, 5.8, 4.4, 2.7, 3.8, 5.8, 3.4, 6.6, 4, 5.4, 2.9, 6.6, 1.5, 0.6, 0, None, None, None, None, None, None,
     None, None, None, None, None],
    [7.6, 7.4, 5.7, 7.2, 1.4, 5.7, 7.2, 3.1, 7.2, 6.7, 8.1, 6.3, 7.2, 4, 6.4, 5.6, 0, None, None, None, None, None,
     None, None, None, None, None],
    [2, 6, 4.1, 5.3, 0.5, 1.9, 7.7, 5.1, 5.9, 2.3, 6.2, 1.2, 5.9, 3.2, 2.4, 1.6, 7.1, 0, None, None, None, None, None,
     None, None, None, None],
    [3.6, 5, 3.6, 6, 1.7, 1.1, 6.6, 4.6, 5.4, 1.8, 6.9, 1, 5.4, 3, 2.2, 1.7, 6.1, 1.6, 0, None, None, None, None, None,
     None, None, None],
    [6.5, 4.8, 4.3, 10.6, 6.5, 3.5, 3.2, 6.7, 1, 4.1, 11.5, 3.7, 1, 6.9, 6.8, 6.4, 7.2, 4.9, 4.4, 0, None, None, None,
     None, None, None, None],
    [1.9, 9.5, 3.3, 5.9, 3.2, 4.9, 11.2, 8.1, 8.5, 3.8, 6.9, 4.1, 8.5, 6.2, 5.3, 4.9, 10.6, 3, 4.6, 7.5, 0, None, None,
     None, None, None, None],
    [3.4, 10.9, 5, 7.4, 5.2, 6.9, 12.7, 10.4, 10.3, 5.8, 8.3, 6.2, 10.3, 8.2, 7.4, 6.9, 12, 5, 6.6, 9.3, 2, 0, None,
     None, None, None, None],
    [2.4, 8.3, 6.1, 4.7, 2.5, 4.2, 10, 7.8, 7.8, 4.3, 4.1, 3.4, 7.8, 5.5, 4.6, 4.2, 9.4, 2.3, 3.9, 6.8, 2.9, 4.4, 0,
     None, None, None, None],
    [6.4, 6.9, 9.7, 0.6, 6, 9, 8.2, 4.2, 11.5, 7.8, 0.4, 6.9, 11.5, 4.4, 4.8, 5.6, 7.5, 5.5, 6.5, 11.4, 6.4, 7.9, 4.5,
     0, None, None, None],
    [2.4, 10, 6.1, 6.4, 4.2, 5.9, 11.7, 9.5, 9.5, 4.8, 4.9, 5.2, 9.5, 7.2, 6.3, 5.9, 11.1, 4, 5.6, 8.5, 2.8, 3.4, 1.7,
     5.4, 0, None, None],
    [5, 4.4, 2.8, 10.1, 5.4, 3.5, 5.1, 6.2, 2.8, 3.2, 11, 3.7, 2.8, 6.4, 6.5, 5.7, 6.2, 5.1, 4.3, 1.8, 6, 7.9, 6.8,
     10.6, 7, 0, None],
    [3.6, 13, 7.4, 10.1, 5.5, 7.2, 14.2, 10.7, 14.1, 6, 6.8, 6.4, 14.1, 10.5, 8.8, 8.4, 13.6, 5.2, 6.9, 13.1, 4.1, 4.7,
     3.1, 7.8, 1.3, 8.3, 0]]
# All the addresses listed in order of the indexes of the distance data
addressData = [['4001 South 700 East'],
               ['1060 Dalton Ave S'],
               ['1330 2100 S'],
               ['1488 4800 S'],
               ['177 W Price Ave'],
               ['195 W Oakland Ave'],
               ['2010 W 500 S'],
               ['2300 Parkway Blvd'],
               ['233 Canyon Rd'],
               ['2530 S 500 E'],
               ['2600 Taylorsville Blvd'],
               ['2835 Main St'],
               ['300 State St'],
               ['3060 Lester St'],
               ['3148 S 1100 W'],
               ['3365 S 900 W'],
               ['3575 W Valley Central Station bus Loop'],
               ['3595 Main St'],
               ['380 W 2880 S'],
               ['410 S State St'],
               ['4300 S 1300 E'],
               ['4580 S 2300 E'],
               ['5025 State St'],
               ['5100 South 2700 West'],
               ['5383 South 900 East #104'],
               ['600 E 900 South'],
               ['6351 South 900 East']]
# Create the package hash table and load it with the information from the package CSV file
packageHashTable = HashMap.CreateHashMap()
packageHashTable = loadPackageData(packageDataFile, "Hash")
# Load all three trucks with their packages
t1 = Truck.Truck(16, 18, 0, loadPackageData(packageDataFile, "t1"), 0, "8:00:00")
t2 = Truck.Truck(16, 18, 0, loadPackageData(packageDataFile, "t2"), 0, "9:05:00")
t3 = Truck.Truck(16, 18, 0, loadPackageData(packageDataFile, "t3"), 0, "10:20:00")

# Total Distance Calculation
t1Distance = minDistanceBetween(distanceData, addressData, t1, 0, t1.packages)  # Distance for truck 1
t2Distance = minDistanceBetween(distanceData, addressData, t2, 0, t2.packages)  # Distance for truck 2
t3Distance = minDistanceBetween(distanceData, addressData, t3, 0, t3.packages)  # Distance for truck 3

totalMiles = t1Distance + t2Distance + t3Distance   # Total distance for all three trucks

# GUI
print('----------------------------')
print('Welcome to the WGUPS System!')
print('----------------------------')
print('Current Route Completed in ' + str(round(totalMiles, 2)) + ' Miles')
running = True
while running:
    userInput = input('-------------------------------\nPlease select one of the following option numbers, then press '
                      'enter:\n'
                      '     1: Details on All Packages at a Certain Time\n'
                      '     2: Details on a Specific Package at a Certain Time\n'
                      '     3: Exit the Program\n')
    if userInput == '3':    # Exit the Program
        print('Goodbye!')
        running = False
        exit()
    elif userInput == '1':  # Details on all packages at a certain time
        userInput = input('Please enter a time in HH:MM:SS Format: ')
        (h, m, s) = userInput.split(':')
        userTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        for p in range(len(packageHashTable.table)):
            package = packageHashTable.search(p + 1)
            (h, m, s) = package.delivered.split(':')
            packageTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            if userTime < packageTime:
                package.status = 'At the Hub'
            print(packageHashTable.search(p + 1))
    elif userInput == '2':  # Details on a specific package at a certain time
        userInput = input('Please type the Package ID: ')
        userTime = input('Please enter a time in HH:MM:SS Format: ')
        (h, m, s) = userTime.split(':')
        compareTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        package = packageHashTable.search(int(userInput))
        (h, m, s) = package.delivered.split(':')
        packageTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        if compareTime < packageTime:
            package.status = 'At the Hub'
        print(package)
