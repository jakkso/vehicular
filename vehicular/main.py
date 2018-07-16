"""
Contains integration of cmd, database and message classes.
"""
import getpass
import sqlite3

from vehicular.config import Config
from vehicular.database import Database, run_search
from vehicular.dicts import (BOOL_OPTIONS,
                             CAR_SELLER,
                             MOTO_SELLER)
from vehicular.message import Message
from vehicular.shell import CarShell, help_message
from vehicular.utilities import credential_validation as cv


class Run(CarShell):
    """
    Final child of shell class hierarchy, implements the methods used to
    build the search URL, as well as CRUD methods for managing searches
    """

    def __init__(self, database: str = Config.database):
        super(Run, self).__init__()
        self.seller_abbrev = None
        self.db_file = database
        self.database = Database(self.db_file)
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
        Allows user to store credentials in the database.  Uses
        utilities.credential_verification to verify that supplied credentials
        actually work.
        :param args:
        :return:
        """
        recipient = input('Recipient address: ')
        sender = input('Sender: ')
        password = getpass.getpass('Sender\'s password: ')
        if cv(user=sender, pw=password):
            self.database.set_credentials(sender, password, recipient)
        else:
            print('Verification failure!  Incorrect username / password?')

    @staticmethod
    def help_credentials() -> None:
        """
        Displays help message for credentials command
        """
        initial_desc = 'Used to set credentials for sending email messages'
        usage = 'Input the credentials as directed', 'Be sure that they are correct'
        help_message(initial_desc, usage, long_desc=None)

    @property
    def credentials(self) -> bool:
        """
        Determines whether or not credentials have been set.  Returns True if they
        have, False otherwise.
        """
        try:
            username, password, recipient = self.database.credentials
            if username and password and recipient:
                return True
        except TypeError:
            return False

    def do_add_search(self, *args) -> None:
        """
        Adds search URL to database
        :return:
        """
        url = self.search_url
        if url:
            try:
                name = self.make_model.split('=')[1].replace('+', ' ')
                print(f'Added {name} search.')
                self.database.add_search(url, name=name)
                self.reset_search_options()
            except sqlite3.IntegrityError:
                print('Each search must be unique!')

    def do_run_search(self, *args) -> None:
        """
        Run search and send email notification
        :param args:
        :return: None
        """
        try:
            user, password, recipient = self.database.credentials
        except TypeError:
            print('Ensure that credentials have been set successfully first.')
            return
        if user and password and recipient:
            hits = run_search(self.db_file)
            if hits:
                print('New hits found!')
                Message(user, password, recipient, hits).send()
            else:
                print('No new search hits.')

    @staticmethod
    def help_run_search() -> None:
        """
        Displays help message for run_message
        """
        initial_desc = 'Used to run search for all URLs in database'
        usage = ' simply run `run_search`',
        help_message(initial_desc, usage, long_desc=None)

    @staticmethod
    def help_add_search() -> None:
        """
        Displays help message for add_search command
        """
        initial_desc = 'Used to add search URL to database'
        usage = 'type `add_search`',
        long_desc = 'Remember, each search must be unique!',
        help_message(initial_desc, usage, long_desc)

    def do_delete_search(self, *args) -> None:
        """
        Draws deletion menu
        """
        # Creates a dictionary with a number corresponding to each search
        url_name = {num: item for num, item in enumerate(self.database.get_url_name())}
        if url_name:
            for key, value in url_name.items():
                # value[0] is the url, value[1] is the name
                print(f'{key}: {value[1]}')
            choice = input('Search to delete: ')
            try:
                choice = int(choice)
                self.database.remove_search(url_name[choice][0])
            except ValueError:
                print('Invalid choice')
            except KeyError:
                print('Invalid choice')
        else:
            print('No active searches')

    @staticmethod
    def help_delete_search() -> None:
        """
        Displays help menu for deletion menu
        """
        initial_desc = 'Used to delete searches from database'
        usage = 'Usage: type `delete_search`', 'Follow the prompts to remove a ' \
                                               'particular search'
        long_desc = 'Type the number listed next to the name to remove a search from ' \
                    'the database',\
                    'This process cannot be undone, so be careful!'
        help_message(initial_desc, usage, long_desc)

    def reset_search_options(self) -> None:
        """
        Sets search values to None
        :return: None
        """
        non_options = 'stdin', 'stdout', 'name', 'mode', 'encoding', 'cmdqueue', \
                      'completekey', 'city', 'vehicle_type', 'seller_type', \
                      'seller_abbrev', 'database', 'lastcmd', 'completion_matches', \
                      'db_file'
        for key in self.__dict__:
            if key not in non_options:
                self.__dict__[key] = None
        # `both` is the default option for seller_type
        self.__dict__['seller_type'] = 'both'

    def do_print_searches(self, *args) -> None:
        """
        Prints out names of all searches in the database
        """
        searches = self.database.get_url_name()
        if searches:
            print('Current searches')
            print('*' * 40)
            for item in searches:
                print(item[1])
            print('*' * 40)
        else:
            print('No active searches.')

    @staticmethod
    def help_print_searches() -> None:
        """
        Prints out help menu for print_searches
        """
        initial = 'Used to print out the current searches'
        usage = 'Usage: type `print_searches`',
        help_message(initial, usage, long_desc=None)
