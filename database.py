"""
Contains database connection class
"""
import os
import sqlite3
from time import time


class Database:
    """
    Defines database connection methods
    """

    def __init__(self, database=os.path.join(os.path.dirname(__file__), 'data.db')):
        """
        :param database: sqlite3 database file.  By default it's located in the same directory as this file.
        """
        self._database = database
        self._connection = sqlite3.connect(self._database)
        self.cursor = self._connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO write logger && log exceptions here
        pass

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self._database})>'

    def create_database(self) -> None:
        """
        Used to init database file.
        updated is simply unix time
        :return: None
        """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS searches '
                            '(id INTEGER PRIMARY KEY, '
                            'search_url TEXT, '
                            'updated TEXT)')

    def add_search(self, url: str) -> None:
        """
        Adds search URL to database
        :param url: search URL to store in database
        :return:
        """
        self.cursor.execute('INSERT INTO searches (search_url, updated) VALUES (?,?)',
                            (url, time()))
        self._connection.commit()



