import os
import sqlite3
import unittest

from database import Database, Parser

DB = 'test_db.db'
URL = 'google.com'
RSS = 'feed:https://denver.craigslist.org/search/cta?auto_make_model=f150&format=rss'


class TestDatabase(unittest.TestCase):
    """
    Contains tests for Database
    """

    def setUp(self) -> None:
        with Database(DB) as _db:
            _db.create_database()

    def tearDown(self) -> None:
        os.remove(DB)

    def test_add_search(self) -> None:
        """
        Tests adding search to database
        """
        with Database(DB) as db:
            db.add_search('google.com', 'test_name')
            with self.assertRaises(sqlite3.IntegrityError):
                db.add_search('google.com', 'test_name')
            db.cursor.execute('SELECT url, name FROM searches')
            url, name = db.cursor.fetchone()
        self.assertEqual('google.com', url)
        self.assertEqual('test_name', name)

    def test_remove_search(self) -> None:
        """
        Tests removing searches
        """
        with Database(DB) as db:
            db.add_search('google.com', 'test_name')
            db.add_search('yahoo.com', 'second_test')
            db.add_search('yahoo1.com', 'second_test')
            db.remove_search('google.com')
            db.cursor.execute('SELECT * from searches')
            self.assertEqual(2, len(db.cursor.fetchall()))

    def test_get_hits(self) -> None:
        """
        Confirms that the fetch searches method works as expected
        """
        with Database(DB) as db:
            db.add_search('google.com', 'test_name')
            self.assertEqual([], db.get_hits('google.com'))
            db.cursor.execute('UPDATE searches SET hits = ? WHERE url = ?', ('hello,friend', 'google.com'))
            self.assertEqual(['hello', 'friend'], db.get_hits('google.com'))

    def test_update_hits(self) -> None:
        """
        Tests that updating hits works properly
        """
        with Database(DB) as db:
            db.add_search(URL, 'test_name')
            db.update_hits(URL, '123', '456', '789')
            db.cursor.execute('SELECT hits FROM searches WHERE url = ?', (URL,))
            self.assertEqual('123,456,789', db.cursor.fetchone()[0])
            db.update_hits(URL, '10', '11', '12')
            db.cursor.execute('SELECT hits FROM searches WHERE url = ?', (URL,))
            self.assertEqual('123,456,789,10,11,12', db.cursor.fetchone()[0])

    def test_get_searches(self) -> None:
        """
        Tests that search fetching works properly
        """
        with Database(DB) as db:
            db.add_search(URL, 'test_name')
            db.update_hits(URL, '123', '456', '789')
            db.add_search('yahoo.com', 'name_2')
            db.update_hits('yahoo.com', '1', '2', '3')
            self.assertEqual([URL, 'yahoo.com'],
                             db.get_searches())


class TestParser(TestDatabase):

    def test_search_worker(self):
        with Parser(DB) as par:
            par.add_search(RSS, 'bob')
            par.run_search()


if __name__ == '__main__':
    unittest.main()
