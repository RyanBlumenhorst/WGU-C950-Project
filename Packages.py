# Ryan Blumenhorst
# Student ID: 002094804


class Package:
    # Constructor Method, id is the packages ID number, add is the delivery address, city is delivery city, state is
    # delivery state, zip is delivery Zipcode, dt is time the package needs to be delivered by, weight is the weight of
    # the package, note is any special notes about the package, like must be delivered with other packages or can only
    # be on truck 2, status is the status of the package, either 'At the Hub', 'On the Way', or 'Delivered', and
    # delivered is the time when a package was delivered.
    def __init__(self, id, add, city, state, zip, dt, weight, note, status, delivered):
        self.id = id
        self.add = add
        self.city = city
        self.state = state
        self.zip = zip
        self.dt = dt
        self.weight = weight
        self.note = note
        self.status = status
        self.delivered = delivered

    # Returns a Print statement for a specific package
    def __str__(self):
        return "-------------------------------\nPackage ID: " + str(self.id) + ", Address: " + str(self.add) + ", City: " + str(self.city) + \
                   ", State: " + str(self.state) + ", Zipcode: " + str(self.zip) + '\nDelivery Time: ' + str(self.dt) +\
                   ', Weight: ' + str(self.weight) + ', Notes: ' + str(self.note) + ', Status: ' + str(self.status)

    # Returns the Address of a package
    def getAdd(self):
        return self.add