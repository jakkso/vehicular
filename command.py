"""
Contains CLI argparser implementation
"""
import getpass
import sqlite3

from database import Parser
from dicts import (BOOL_OPTIONS,
                   CAR_SELLER,
                   MOTO_SELLER)
from message import Message
from shell import Shell, help_message

"""
# Get options from user
    # Cities are the real sticking point: there are ~700 valid cities
    # The JS version of CLNotify use a form of autocorrect to get the spelling correct
    # What to do here? I'd like to allow the user to cities.  Perhaps some sort of CLI autocomplete library?
    # Looks like our solution is a custom shell built using the cmd library and gnureadline!  Woohoo!
# convert rec'd options into URL formatted options via dicts
# Combine URL formatted options into single rss feed url
# Add to database, update, refresh, etc, essentially copy from CLNotify

# ex search URL:
# https://denver.craigslist.org/search/mca?format=rss&auto_make_model=street triple
"""


class Run(Shell):
    """
    Final child of shell class hierarchy, implements the methods use to
    build the search URL, as well as storing searches in the database
    """

    def __init__(self):
        super(Run, self).__init__()
        self.seller_abbrev = None
        self.database = Parser()
        self.database.create_database()

    def create_seller_abbrev(self) -> None:
        """
        Checks that self.vehicle_type and self.seller_type have been defined.
        If they have, sets seller_abbrev to proper value.
        :return: None
        """
        if self.seller_type and self.vehicle_type:
            if self.vehicle_type == 'motorcycle':
                self.seller_abbrev = MOTO_SELLER[self.seller_type]
            elif self.vehicle_type == 'cars/trucks':
                self.seller_abbrev = CAR_SELLER[self.seller_type]

    @property
    def search_url(self) -> str or None:
        """
        Creates search url
        :return: search URL string or None
        """
        self.create_seller_abbrev()
        non_options = 'stdin', 'stdout', 'name', 'mode', 'encoding', 'cmdqueue', \
                      'completekey', 'city', 'vehicle_type', 'seller_type', \
                      'seller_abbrev', 'database', 'lastcmd', 'completion_matches'
        options = {key: value for key, value in self.__dict__.items() if key not
                   in non_options and value}
        sel_options = []
        if self.city and self.seller_abbrev and self.make_model:
            base_url = f'{self.CITY_DICT[self.city]}{self.seller_abbrev}?format=rss&'
            for key, value in options.items():
                if key in BOOL_OPTIONS:
                    # In order for toggle functionality to work, its value has to
                    # remain a boolean up until it's added to the selected options list
                    sel_options.append(BOOL_OPTIONS[key])
                else:
                    # All other options are in the completed form
                    sel_options.append(value)
                return base_url + '&'.join(sel_options)
        else:
            msg = 'At a minimum, you must set the city, seller type,' \
                  ' vehicle type and a make_model.'
            print(msg)

    def do_credentials(self, *args) -> None:
        """
        Allows user to set credentials
        :param args:
        :return:
        """
        recipient = input('Recipient address: ')
        sender = input('Sender: ')
        password = getpass.getpass('Sender\'s password: ')
        Parser().set_credentials(sender, password, recipient)

    def help_credentials(self) -> None:
        """
        Displays help message for credentials command
        """
        initial_desc = 'Used to set credentials for sending email messages'
        usage = 'Input the credentials as directed', 'Be sure that they are correct'
        help_message(initial_desc, usage, long_desc=None)

    def do_add_search(self, *args) -> None:
        """
        Adds search URL to database
        :return:
        """
        url = self.search_url
        if url:
            try:
                self.database.add_search(url, name='null')
                Message().run()
                self.reset_search_options()
            except sqlite3.IntegrityError:
                print('Each search must be unique!')

    def do_run_search(self, *args) -> None:
        """
        Run search and send emails.
        :param args:
        :return: None
        """
        Message().run()

    def help_run_search(self) -> None:
        """
        Displays help message for run_message
        """
        initial_desc = 'Used to run search for all URLs in database'
        usage = ' simply run `run_search`',
        help_message(initial_desc, usage, long_desc=None)

    def help_add_search(self) -> None:
        """
        Displays help message for add_search command
        """
        initial_desc = 'Used to add search URL to database'
        usage = 'type `add_search`',
        long_desc = 'Remember, each search must be unique!',
        help_message(initial_desc, usage, long_desc)

    def reset_search_options(self) -> None:
        """
        Sets search values to None
        :return: None
        """
        non_options = 'stdin', 'stdout', 'name', 'mode', 'encoding', 'cmdqueue', \
                      'completekey', 'city', 'vehicle_type', 'seller_type', \
                      'seller_abbrev', 'database', 'lastcmd', 'completion_matches'
        for key in self.__dict__:
            if key not in non_options:
                self.__dict__[key] = None



if __name__ == '__main__':
    Run().cmdloop()
