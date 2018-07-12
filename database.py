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
                            'updated INTEGER,'
                            'hits TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS settings '
                            '(id INTEGER PRIMARY KEY, '
                            'sender TEXT, '
                            'password TEXT, '
                            'recipient TEXT)')

    def add_search(self, url: str, name: str) -> None:
        """
        Adds search URL to database
        :param url: search URL to store in database
        :param name: search name
        :return:
        """
        self.cursor.execute('INSERT INTO searches (url, name, updated) VALUES (?,?,?)',
                            (url, name, 0))
        self._connection.commit()

    def remove_search(self, url: str) -> None:
        """
        Removes search & associated search hits
        :param url: search name.
        :return:
        """
        self.cursor.execute('DELETE FROM searches WHERE url = ?', (url,))
        self._connection.commit()

    def _get_urls(self) -> list:
        """
        Returns a list of search urls
        :return:
        """
        self.cursor.execute('SELECT url FROM searches')
        return [url[0] for url in self.cursor.fetchall()]

    def get_urls(self) -> list:
        """
        Returns a list of search urls that need to be updated.  CL only updates the
        RSS feeds once per hour.  This method returns urls that haven't been updated in the last hour
        :return:
        """
        now = time()
        self.cursor.execute('SELECT url FROM searches WHERE ? >= updated + 3600', (now,))
        return [item[0] for item in self.cursor.fetchall()]

    def _get_hits(self, url: str) -> list:
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

    def _update_hits(self, url: str, *hits) -> None:
        """

        :param url: search URL
        :param hits: list of search hit IDs
        :return: None
        """
        previous_hits = self._get_hits(url)
        for hit in hits:
            previous_hits.append(hit)
        self.cursor.execute('UPDATE searches SET hits = ? WHERE url = ?', (','.join(previous_hits), url))
        self._connection.commit()
        self._update_time(url)

    def _update_time(self, url: str) -> None:
        """
        Updates updated to time.time()
        :param url: rss feed URL
        :return: None
        """
        self.cursor.execute('UPDATE searches SET updated = ? WHERE url = ?', (time(), url))

    @property
    def credentials(self) -> tuple:
        """
        Returns tuple of sender email address, password and recipient email address
        :return:
        """
        self.cursor.execute('SELECT sender, password, recipient FROM settings WHERE id = 1')
        return self.cursor.fetchone()

    def set_credentials(self, sender: str, password: str, recipient: str) -> None:
        """
        Sets email credentials
        :param sender:
        :param password:
        :param recipient:
        :return:
        """
        self.cursor.execute('SELECT sender FROM settings')
        res = self.cursor.fetchone()
        if res is None:
            self.cursor.execute('INSERT INTO settings(sender, password, recipient) '
                                'VALUES (?,?,?)', (sender, password, recipient))
        else:
            self.cursor.execute('UPDATE settings set sender = ?, password = ?, recipient = ? '
                                'WHERE id = 1',
                                (sender, password, recipient))
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
        for url in self.get_urls():
            # Extend flattens all list results from each url
            new_hits.extend(self._search_worker(url))
        return new_hits

    def _search_worker(self, url) -> list:
        """
        Gets list of new hits, increments search to current time.time()
        :param url: RSS Feed URL
        :return:
        """
        new_hits = [entry for entry in fp.parse(url).entries
                    if entry['id'] not in self._get_hits(url)]
        for hit in new_hits:
            hit['title'] = hit['title'].replace('&#x0024;', '$')
            self._update_hits(url, hit['id'])
        self._update_time(url)
        return new_hits
