"""
Contains classes that define database usage methods
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
        if exc_type is not None:
            print(f'Error: {exc_val}\n{exc_tb}')
            self._connection.rollback()
            self._connection.close()
        else:
            self._connection.commit()
            self._connection.close()

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({self._database})>'

    def create_database(self) -> None:
        """
        Used to init database file.

        url - CL RSS feed URL

        name - Name of the make_model search.  Human readable

        updated - simply unix time.  Craigslist only updates RSS feeds once per hour,
            this is used to keep track of when the feed was last parsed and only
            run searches when at least one hour has elapsed since the last search.

        hits - CSV string of search ID's (Which are actually just the URLs for each
            individual CL post).  When fetched, they're split into a list.  Could just
            use foreign keys, but this is (slightly) easier to deal with.  I really
            ought to learn to write better SQL

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
        Adds search URL to database, along with name associated with each search.
        :param url: search URL to store in database
        :param name: search name, human readable name.  Taken from the make_model
        :return:
        """
        self.cursor.execute('INSERT INTO searches (url, name, updated) VALUES (?,?,?)',
                            (url, name, 0))
        self._connection.commit()

    def remove_search(self, url: str) -> None:
        """
        Removes search from database, based on RSS feed url
        :param url: RSS feed url
        :return:
        """
        self.cursor.execute('DELETE FROM searches WHERE url = ?', (url,))
        self._connection.commit()

    def get_url_name(self) -> list:
        """
        Returns list of tuples of search urls and names, like below:

         [('example.rss.feed.url.1.craigslist.org', 'Human readable name 1),
         ('example.rss.feed.url.2.craigslist.org', 'Human readable name 2)]

        """
        self.cursor.execute('SELECT url, name FROM searches')
        return self.cursor.fetchall()

    def get_urls(self) -> list:
        """
        Returns a list of search urls that need to be updated.  CL only updates the
        RSS feeds once per hour.  This method returns urls that haven't been updated in the last hour
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
        # .split() doesn't work on None results
        except AttributeError:
            res = []
        return res

    def _update_hits(self, url: str, *hits) -> None:
        """
        Gets previous hits from database, combines all new hits (Which are CL urls)
        into a single string, which is then stored in the row associated with its
        rss url

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
        Updates updated to current time.time for the specified rss feed url
        :param url: rss feed URL
        :return: None
        """
        self.cursor.execute('UPDATE searches SET updated = ? WHERE url = ?', (time(), url))

    @property
    def credentials(self) -> tuple:
        """
        Returns tuple of sender email address, password and recipient email
        address from the database
        :return: tuple
        """
        self.cursor.execute('SELECT sender, password, recipient FROM settings WHERE id = 1')
        return self.cursor.fetchone()

    def set_credentials(self, sender: str, password: str, recipient: str) -> None:
        """
        Sets email credentials.
        :param sender:
        :param password:
        :param recipient:
        :return: None
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


class FPIntegration(Database):
    """
    Integrates Feedparser into database operations
    """
    def run_search(self) -> list:
        """
        Updates rss feed urls (Remember, Database.get_urls only returns urls
        that haven't been updated in the last hour) and builds a single list of
        FeedParserDicts from feedparser.parse(url).entries.

        These updates are returned by FPIntegration._search_worker

        :return: list of FeedParserDicts
        """
        new_hits = []
        for url in self.get_urls():
            # Extend flattens all list results from each url
            new_hits.extend(self._search_worker(url))
        return new_hits

    def _search_worker(self, url) -> list:
        """
        Gets list of new hits associated with a single RSS feed url, increments
        row's updated value to current value of time.time()

        At a later date, I intend to refactor FPIntegration.run_search and
        FPIntegration._search_worker to use multiprocessing.dummy.Pool.

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
