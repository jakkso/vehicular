import os
import sqlite3
import unittest

from vehicular.database import Database, FPIntegration

DB = 'test_db.db'
URL = 'google.com'
RSS = 'feed:https://denver.craigslist.org/search/cta?auto_make_model=f150&format=rss'
RSS2 = 'feed:https://denver.craigslist.org/search/cta?auto_make_model=dodge%20ram&format=rss'


class TestDatabase(unittest.TestCase):
    """
    Contains tests for Database
    """

    def setUp(self) -> None:
        with Database(DB) as db:
            db.create_database()

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

    def test_get_url_name(self) -> None:
        """
        Tests getting name / URLs from database
        """
        with Database(DB) as db:
            db.add_search(URL, 'test_name')
            db.add_search('youtube', 'asdf')
            db.add_search('4chan', 'cuck')
            res = db.get_url_name()
            self.assertEqual([(URL, 'test_name'),
                              ('youtube', 'asdf'),
                              ('4chan', 'cuck')],
                             res)

    def test_update_time(self) -> None:
        """
        Tests time update incrementation
        """
        with Database(DB) as db:
            db.add_search(URL, 'test_name')
            db.cursor.execute('SELECT updated FROM searches WHERE url = ?', (URL,))
            time_1 = db.cursor.fetchone()[0]
            db.update_time(URL)
            db.cursor.execute('SELECT updated FROM searches WHERE url = ?', (URL,))
            time_2 = db.cursor.fetchone()[0]
            self.assertGreater(time_2, time_1)

    def test_get_urls_time_limited(self)-> None:
        """
        Database.get_urls() is time limited to only return URLs that have been not been updated
        in the last hour, this is testing that functionality
        :return:
        """
        with Database(DB) as db:
            db.add_search(URL, 'test_name')
            db.add_search('yahoo', 'name2')
            db.add_search('msn.com', 'name3')
            urls = db.get_urls()
            self.assertEqual([URL, 'yahoo', 'msn.com'], urls)
            db.update_time(URL)
            urls = db.get_urls()
            self.assertEqual(['yahoo', 'msn.com'], urls)
            db.update_time('msn.com')
            urls = db.get_urls()
            self.assertEqual(['yahoo'], urls)
            db.update_time('yahoo')
            urls = db.get_urls()
            self.assertEqual([], urls)

    def test_get_credentials(self):
        """
        Tests credential property method as well as set_credentials
        """
        with Database(DB) as db:
            db.set_credentials('a.potts.bot', 'sample_password', 'mellandru')
            self.assertEqual(('a.potts.bot', 'sample_password', 'mellandru'), db.credentials)
            db.set_credentials('a', 'b', 'c')
            self.assertEqual(('a', 'b', 'c'), db.credentials)


class TestParser(TestDatabase):

    def test_search_worker(self):
        with FPIntegration(DB) as par:
            par.add_search(RSS, 'bob')
            par.add_search(RSS2, 'bob2')
            orig_hits = par.run_search()
            self.assertGreater(len(orig_hits), 0)
            # Change time to ensure that the search is actually run again.  Otherwise,
            # since the time has been updated, Parser.get_urls will return no URLs
            par.cursor.execute('UPDATE searches SET updated = 0 WHERE url = ?', (RSS,))
            second_run = par.run_search()
            self.assertEqual([], second_run)


if __name__ == '__main__':
    unittest.main()
