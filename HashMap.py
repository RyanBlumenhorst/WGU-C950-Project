# Ryan Blumenhorst
# Student ID: 002094804
import Packages


class CreateHashMap:

    # Constructor Method, assigns all buckets with an empty list
    def __init__(self, capacity=40):
        # Create an empty hash table
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Inserts a new item into the Hash Table
    def insert(self, key, value):
        index = hash(key) % len(self.table)
        index_list = self.table[index]

        for kv in index_list:
            if kv[0] == key:
                kv[1] = value
                return True

        key_value = [key, value]
        # Inserts the item to the end of the list
        index_list.append(key_value)
        return True

    # Removes an item with matching key from the hash table
    def remove(self, key):
        index = hash(key) % len(self.table)
        index_list = self.table[index]

        if key in index_list:
            index_list.remove(key)

    # Searches for an item with matching key in hash table.
    def search(self, key):
        index = hash(key) % len(self.table)
        index_list = self.table[index]
        for pair in index_list:
            if pair[0] == key:
                return pair[1]
        return None

    # Function to return the Address of a package in the table
    def getAdd(self, key):
        index = hash(key) % len(self.table)
        index_list = self.table[index]
        for pair in index_list:
            if pair[0] == key:
                return Packages.Package.getAdd(pair[1])