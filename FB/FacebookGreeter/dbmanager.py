__author__ = 'dgraziotin'

"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""
"""
Module that holds the class responsible for object persistency
"""
import pickle

DATABASE_NAME = 'database.pk'

class DBManager(object):
    """
    Database manager class. It encapsulates operations over the pickle module and utility methods over the
    actual user. The objects are saved in a hash-map like data structure
    """
    def database(self):
        """
        returns the database representation
        """
        try:
            database_file = open(DATABASE_NAME, 'rb')
            database = pickle.load(database_file)
        except IOError:
            database_file = open('database.pk', 'wb')
            database = dict()
            pickle.dump(database, database_file)
            database_file.close()
            database_file = open(DATABASE_NAME, 'rb')
            database = pickle.load(database_file)
        return database

    def save(self, name, value):
        """
        Saves an object under a particular name
        """
        database = self.database()
        database[name] = value
        database_file = open('database.pk', 'wb')
        pickle.dump(database, database_file)
        database_file.close()

    def get(self, name):
        """
        Retrieves and returns an object stored under the name 'name'
        """
        database = self.database()
        try:
            return database[name]
        except KeyError:
            return None