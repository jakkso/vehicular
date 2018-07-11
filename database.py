"""
Contains database connection class
"""
from multiprocessing.dummy import Pool as ThreadPool
import os
import sqlite3
from time import time

import feedparser as fp


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
        self._connection.execute('PRAGMA foreign_keys=ON')
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
        updated is simply unix time.  Craigslist only updates RSS feeds once per hour,
        this is used to keep track of when the feed was last parsed
        cl_id is the craigslist post id.  Don't need repeats, after all.
        :return: None
        """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS searches '
                            '(url TEXT UNIQUE, '
                            'name TEXT, '
                            'updated TEXT,'
                            'hits TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS settings '
                            '(id INTEGER, sender TEXT, password TEXT, recipient TEXT)')

    def add_search(self, url: str, name: str) -> None:
        """
        Adds search URL to database
        :param url: search URL to store in database
        :param name: search name
        :return:
        """
        self.cursor.execute('INSERT INTO searches (url, name, updated) VALUES (?,?,?)',
                            (url, name, time()))
        self._connection.commit()

    def remove_search(self, url: str) -> None:
        """
        Removes search & associated search hits
        :param url: search name.
        :return:
        """
        self.cursor.execute('DELETE FROM searches WHERE url = ?', (url,))
        self._connection.commit()

    def get_searches(self) -> list:
        """
        Returns a list of search urls
        :return:
        """
        self.cursor.execute('SELECT url FROM searches')
        return [url[0] for url in self.cursor.fetchall()]

    def get_hits(self, url: str) -> list:
        """
        Returns list of search hits associated with a rss search
        :param url: rss search url
        """
        self.cursor.execute('SELECT hits FROM searches WHERE url = ?', (url,))
        try:
            res = self.cursor.fetchone()[0].split(',')
        except AttributeError:
            res = []
        return res

    def update_hits(self, url: str, *hits) -> None:
        """

        :param url: search URL
        :param hits: list of search hit IDs
        :return: None
        """
        previous_hits = self.get_hits(url)
        for hit in hits:
            previous_hits.append(hit)
        self.cursor.execute('UPDATE searches SET hits = ? WHERE url = ?', (','.join(previous_hits), url))
        self._connection.commit()


class Parser(Database):
    """
    Integrates Feedparser into database operations
    """
    def run_search(self) -> list:
        """

        :return:
        """
        new_hits = []
        for url in self.get_searches():
            # Extend flattens all
            new_hits.extend(self.search_worker(url))
        return new_hits

    def search_worker(self, url) -> list:
        """
        :param url: RSS Feed URL
        :return:
        """
        new_hits = [entry for entry in fp.parse(url).entries
                    if entry['id'] not in self.get_hits(url)]
        for hit in new_hits:
            self.update_hits(url, hit['id'])
        return new_hits







