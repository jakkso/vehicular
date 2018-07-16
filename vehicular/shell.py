"""
Contains classes that extend cmd.Cmd shell, implementing various search options
storage and autocompletion of said options.
"""

try:
    import gnureadline
except ImportError:
    import readline
    gnureadline = readline
import cmd
from os import path
import sys
from typing import List

from vehicular.dicts import (CAR_SIZE,
                             CAR_TYPE,
                             CITIES,
                             COLORS,
                             CONDITION,
                             CYLINDER_COUNT,
                             DRIVETRAIN,
                             FUEL_TYPES,
                             TITLE_STATUS,
                             TRANSMISSION)


sys.modules['readline'] = gnureadline
PICKLE_FILE = path.join(path.dirname(__file__), 'cities.p')


class BaseShell(cmd.Cmd):
    """
    Creates shell environment

    For cmd.Cmd subclasses, there are several special methods that come in the
    form of do_XXX, complete_XXX and help_XXX.

    do_XXX: Inside the shell created by running cmd.Cmd().cmdloop(), when the user types
        command `XXX` and presses enter, do_XXX is called, passing whatever argument
        follows command `XXX`.

    complete_XXX: This is used to enable bash-style auto-completion upon pressing tab.
        It takes 4 parameters:
            text: the text after the command
            line: the entire line
            start_index: start index of `text`
            end_index: end index of `text`
        The way it's implemented is that if `text` is empty, then the entire list
        of potential options is returned. Otherwise, a list of items that start with
        `text` is returned.

        The user types the command followed by a partial option, presses tab.  If the
        partial option is close to a single option, that option replaces the partial
        option. Otherwise, the system bell sounds.  If there are no matches, successive
        tab key presses just ring the system bell.  If there are multiple matches,
        pressing tab prints the partial matches.

    help_XXX: Is called when user types help XXX.
    """

    CITY_DICT = CITIES
    CITIES = [city for city in CITY_DICT]
    VEHICLE_TYPES = 'motorcycle', 'cars/trucks'
    SELLER_TYPES = 'dealer', 'owner', 'both'

    def __init__(self):
        super(BaseShell, self).__init__()
        #  Required args
        self.city = None
        self.vehicle_type = None
        self.make_model = None
        self.seller_type = 'both'
        #  Boolean options
        self.has_images = False
        self.posted_today = False
        self.crypto_okay = False
        self.nearby_areas = False
        self.titles_only = False
        #  Open ended, numerical options
        self.postal = None
        self.distance_from_postal = None
        self.min_miles = None
        self.max_miles = None
        self.min_price = None
        self.max_price = None
        self.min_year = None
        self.max_year = None
        #  Options with specific possible values
        self.title_status = None
        self.condition = None
        self.fuel = None
        self.color = None
        self.transmission = None
        #  These options are only valid for cars / trucks, not motorcycles
        self.cylinders = None
        self.drive_train = None
        self.cage_type = None
        self.cage_size = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def do_EOF(self, *args) -> True:
        """
        Allows user to exit shell upon using the standard `ctrl + d`
        :param args:
        :return:
        """
        print('Exiting...')
        return True

    @staticmethod
    def help_EOF() -> None:
        """
        Prints help for EOF
        """
        initial_desc = 'Used to gracefully exit the shell'
        usage = 'Invoked via the standard shortcut of ctrl + d',
        help_message(initial_desc, usage, long_desc=None)

    def do_city(self, city) -> None:
        """
        Sets self.city to city
        :param city
        :return:
        """
        if city in self.CITIES:
            self.city = city
            print(f'City set to {city}.')
        else:
            print(f'Invalid city: `{city}`.  Be sure to enter exactly what is '
                  f'suggested')

    def complete_city(self,
                      text: str,
                      line: str,
                      start_index: int,
                      end_index: int) -> List[str]:
        """
        Sets up auto completion for cities
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.CITIES[:]
        else:
            completions = [city for city in self.CITIES if city.startswith(text)]
        return completions

    @staticmethod
    def help_city() -> None:
        """
        Prints help for city command
        """
        initial_desc = 'Used to select the city to search'
        usage = 'Usage: `city <city>`', 'ex: `city san_diego` selects San Diego, CA.'
        long_desc = ['Pressing <tab> autocompletes available cities based on what has been typed.',
                     'Typing `city san` and pressing tab twice displays all cities that start with ',
                     '`san`.  Use this to help find a specific city, as if the name does not match ',
                     'what is in the list, it will be rejected.']
        help_message(initial_desc, usage, long_desc)

    def do_vehicle_type(self, vehicle_type) -> None:
        """

        :param vehicle_type:
        :return:
        """
        if vehicle_type in self.VEHICLE_TYPES:
            if vehicle_type == 'motorcycle':
                # These search options aren't valid for motorcycle searches
                self.cylinders = None
                self.drive_train = None
                self.cage_type = None
            self.vehicle_type = vehicle_type
            print(f'Vehicle type set to {self.vehicle_type}.')
        else:
            print(f'Invalid vehicle type: `{vehicle_type}`.')
            self.help_vehicle_type()

    def complete_vehicle_type(self,
                              text: str,
                              line: str,
                              start_index: int,
                              end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.VEHICLE_TYPES[:]
        else:
            completions = [type_ for type_ in self.VEHICLE_TYPES if
                           type_.startswith(text)]
        return completions

    @staticmethod
    def help_vehicle_type() -> None:
        """
        Prints help for using vehicle_type command
        """
        initial_desc = 'Used to select the vehicle type'
        usage = 'Usage: `vehicle_type <vehicle_type>`', 'ex: `vehicle_type motorcycle`'
        long_desc = 'Valid options are `cars/trucks` or `motorcycle`',
        help_message(initial_desc, usage, long_desc)

    def do_seller_type(self, seller_type: str) -> None:
        """
        :param seller_type:
        :return:
        """
        if seller_type in self.SELLER_TYPES:
            self.seller_type = seller_type
            print(f'Set seller type to {seller_type}.')
        else:
            print(f'Invalid seller type `{seller_type}`')

    def complete_seller_type(self,
                             text: str,
                             line: str,
                             start_index: int,
                             end_index: int) -> List[str]:
        """

        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.SELLER_TYPES[:]
        else:
            completions = [option for option in self.SELLER_TYPES if
                           option.startswith(text)]
        return completions

    @staticmethod
    def help_seller_type() -> None:
        """
        Prints help for using seller_type command
        :return:
        """
        initial_desc = 'Used to select seller type'
        usage = 'Usage: `seller_type <seller_type>`', 'ex: `seller_type dealer`'
        long_desc = 'Valid options are `dealer`, `owner`, or `both`',
        help_message(initial_desc, usage, long_desc)


class BoolShell(BaseShell):
    """
    This class extends BaseShell and adds methods to manage boolean options for the
    search.
    """
    def do_has_images(self, *args) -> None:
        """
        Toggles self.has_images
        """
        self.has_images = not self.has_images
        print(f'Posts must have images: {self.has_images}.')

    @staticmethod
    def help_has_images() -> None:
        """
        Prints has_images help message
        """
        initial_desc = 'Used to toggle has_images option'
        usage = 'Type `has_images` and press enter.',\
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_posted_today(self, *args) -> None:
        """
        Toggles self.posted_today
        """
        self.posted_today = not self.posted_today
        print(f'Posts must have been posted today: {self.posted_today}.')

    @staticmethod
    def help_posted_today() -> None:
        """
        Prints posted_today help message
        """
        initial_desc = 'Used to toggle posted_today option'
        usage = 'Type `posted_today` and press enter.', \
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_crypto(self, *args) -> None:
        """
        Toggles self.crypto
        """
        self.crypto_okay = not self.crypto_okay
        print(f'Posts must accept payment in cryptocurrency: {self.crypto_okay}.')

    @staticmethod
    def help_crypto() -> None:
        """
        Prints crypto help message
        """
        initial_desc = 'Used to toggle cryptocurrency option'
        usage = 'Type `crypto` and press enter.', \
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_titles_only(self, *args) -> None:
        """
        Toggles self.titles_only
        """
        self.titles_only = not self.titles_only
        print(f'Search titles only: {self.titles_only}')

    @staticmethod
    def help_titles_only() -> None:
        """
        Prints titles_only help message
        """
        initial_desc = 'Used to toggle searching titles only'
        usage = 'Type `titles_only` and press enter',\
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_nearby_areas(self, *args) -> None:
        """
        Toggles nearby area search option
        """
        self.nearby_areas = not self.nearby_areas
        print(f'Search nearby areas: {self.nearby_areas}.')

    @staticmethod
    def help_nearby_areas() -> None:
        """
        Prints help message for nearby areas
        """
        initial_desc = 'Used to toggle search nearby areas in addition' \
                       'to the specified city'
        usage = 'Type `nearby_areas` and press enter',\
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)


class OpenEndedShell(BoolShell):
    """
    Further Extends the shell to include open ended option inputs
    """
    def do_postal_code(self, postal: str) -> None:
        """
        Allows user to specify postal code to search
        :param postal:
        :return: None
        """
        self.postal = f'postal={postal}'
        print(f'Postal code set to: {postal}.')

    @staticmethod
    def help_postal_code() -> None:
        """
        Prints help message for postal_code
        """
        initial_desc = 'Used to specify zip / postal code'
        usage = 'Usage: `postal_code <postal_code>`',\
                'ex: `postal_code 10001` specifies postal code 10001'
        help_message(initial_desc, usage, long_desc=None)

    def do_distance_from_postal(self, distance: str) -> None:
        """
        Allows user to specify a distance from postal code in wich to search.
        Max 200 miles/KM
        :param distance:
        :return: None
        """
        if not self.postal:
            print('You must first set a postal/zip code in order to have a distance '
                  'from it.')
            return
        try:
            distance = int(distance)
        except ValueError:
            print(f'Invalid value: `{distance}`, must be a number.')
            return
        if distance > 200:
            print('Distance must be less than 200')
            return
        self.distance_from_postal = f'search_distance={distance}'
        print(f'Distance from postal/zip code set to: {distance}.')

    @staticmethod
    def help_distance_from_postal() -> None:
        """
        Prints help message for distance_from_postal
        """
        initial_desc = 'Used to specify distance from postal/zip code'
        usage = 'Usage: `distance_from_postal <distance>`', \
                'ex: `distance_from_postal 500`'
        long_desc = 'In order for this option to work, you must first set the ' \
                    'postal/zip code.',
        help_message(initial_desc, usage, long_desc)

    def do_min_price(self, price) -> None:
        """
        Allows user to specify min price
        :param price:
        :return: None
        """
        try:
            price = int(price)
        except ValueError:
            print(f'Invalid price: `{price}`.')
            return
        self.min_price = f'min_price={price}'
        print(f'Min price set to: {price}.')

    @staticmethod
    def help_min_price() -> None:
        """
        Prints help message for min_price
        """
        initial_desc = 'Used to specify minimum price'
        usage = 'Usage: `min_price <price>`', 'ex: `min_price 1000`'
        long_desc = 'Price must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_price(self, price) -> None:
        """
        Allows user to specify max price
        :param price:
        :return: None
        """
        try:
            price = int(price)
        except ValueError:
            print(f'Invalid price: `{price}`.')
            return
        self.max_price = f'max_price={price}'
        print(f'Max price set to: {price}.')

    @staticmethod
    def help_max_price() -> None:
        """
        Prints help message for max_price
        """
        initial_desc = 'Used to specify maximum price'
        usage = 'Usage: `max_price <price>`', 'ex: `max_price 1000`'
        long_desc = 'Price must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_min_miles(self, miles) -> None:
        """
        Allows user to specify min mileage
        :param miles:
        :return: None
        """
        try:
            miles = int(miles)
        except ValueError:
            print(f'Invalid miles: `{miles}`.')
            return
        self.min_miles = f'min_auto_miles={miles}'
        print(f'Minimum miles set to: {miles}.')

    @staticmethod
    def help_min_miles() -> None:
        """
        Prints help message for min_miles
        """
        initial_desc = 'Used to specify minimum mileage'
        usage = 'Usage: `min_miles <miles>`', 'ex: `min_miles 10000`'
        long_desc = 'Miles must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_miles(self, miles) -> None:
        """
        Allows user to specify max mileage
        :param miles:
        :return: None
        """
        try:
            miles = int(miles)
        except ValueError:
            print(f'Invalid miles: `{miles}`.')
            return
        self.max_miles = f'max_auto_miles={miles}'
        print(f'Maximum miles set to: {miles}.')

    @staticmethod
    def help_max_miles() -> None:
        """
        Prints help message for max_miles
        """
        initial_desc = 'Used to specify maximum mileage'
        usage = 'Usage: `max_miles <miles>`', 'ex: `max_miles 10000`'
        long_desc = 'Miles must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_year(self, year) -> None:
        """
        Allows user to specify max year
        :param year:
        :return: None
        """
        try:
            year = int(year)
        except ValueError:
            print(f'Invalid year: `{year}`.')
            return
        self.max_year = f'max_auto_year={year}'
        print(f'Maximum year set to: {year}.')

    @staticmethod
    def help_max_year() -> None:
        """
        Prints help message for max_year
        """
        initial_desc = 'Used to specify maximum year'
        usage = 'Usage: `max_year <year>`', 'ex: `max_year 10000`'
        long_desc = 'Year must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_min_year(self, year) -> None:
        """
        Allows user to specify min year for which to search
        :param year:
        :return: None
        """
        try:
            year = int(year)
        except ValueError:
            print(f'Invalid year: `{year}`.')
            return
        self.min_year = f'min_auto_year={year}'
        print(f'Minimum year set to: {year}.')

    @staticmethod
    def help_min_year() -> None:
        """
        Prints help message for min_year
        """
        initial_desc = 'Used to specify minimum year'
        usage = 'Usage: `min_year <year>`', 'ex: `min_year 10000`'
        long_desc = 'Year must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_make_model(self, make_model: str) -> None:
        """
        Allows user to specify make and model for which to search.
        :param make_model: str, vehicle make model
        :return: None
        """
        if make_model:
            self.make_model = f'auto_make_model={make_model.replace(" ", "+")}'
            print(f'Searching for {make_model}')
        else:
            print('Be sure to actually search for something')

    @staticmethod
    def help_make_model() -> None:
        """
        Prints help message for make_model
        """
        initial_desc = 'Used to specify for which vehicle make & model to search.'
        usage = 'Usage: `make_model <make>`', 'ex: make_model toyota tacoma'
        help_message(initial_desc, usage, None)


class SpecificOptionsShell(OpenEndedShell):
    """
    Used to implement options that have specific options
    """
    CONDITIONS = 'new', 'like-new', 'excellent', 'good', 'fair', 'salvage'
    FUEL = 'gas', 'diesel', 'hybrid', 'electric', 'other'
    COLOR = 'black', 'blue', 'brown', 'green', 'grey', 'orange', 'purple', \
            'red', 'silver', 'white', 'yellow', 'other'
    TRANSMISSION = 'manual', 'automatic', 'other'
    TITLE_STATUS = 'clean', 'salvage', 'rebuilt', 'parts-only', 'lien', 'missing'

    def do_condition(self, condition) -> None:
        """
        Allows user to specify vehicle condition
        :param condition:
        :return: None
        """
        if condition in self.CONDITIONS:
            self.condition = CONDITION[condition]
            print(f'Condition set to: {self.condition}.')
        else:
            print(f'Invalid condition: `{condition}`.')
            self.help_condition()

    def help_condition(self) -> None:
        """
        Prints help message for condition
        """
        initial_desc = 'Used to specify vehicle condition'
        usage = 'Usage: `condition <condition>`', 'ex: `condition like-new`'
        long_desc = 'Valid options: ',\
                    ' '.join(self.CONDITIONS)
        help_message(initial_desc, usage, long_desc)

    def complete_condition(self,
                           text: str,
                           line: str,
                           start_index: int,
                           end_index: int) -> List[str]:
        """

        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.CONDITIONS[:]
        else:
            completions = [option for option in self.CONDITIONS
                           if option.startswith(text)]
        return completions

    def do_title_status(self, status: str) -> None:
        """
        Allows user to specify title status
        :param status:
        :return: None
        """
        if status in self.TITLE_STATUS:
            self.title_status = TITLE_STATUS[status]
            print(f'Title status set to: {status}')
        else:
            print(f'Invalid title status: `{status}`.')
            self.help_title_status()

    def help_title_status(self) -> None:
        """
        Prints help message for title_status
        """
        initial_desc = 'Used to specify title status'
        usage = 'Usage: `title_status <status>`', 'ex: `title_status lien`'
        long_desc = 'Valid options: ', ' '.join(self.TITLE_STATUS)
        help_message(initial_desc, usage, long_desc)

    def complete_title_status(self,
                              text: str,
                              line: str,
                              start_index: int,
                              end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.TITLE_STATUS[:]
        else:
            completions = [option for option in self.TITLE_STATUS
                           if option.startswith(text)]
        return completions

    def do_fuel(self, fuel: str) -> None:
        """
        Allows user to specify fuel type
        :param fuel:
        :return: None
        """
        if fuel in self.FUEL:
            self.fuel = FUEL_TYPES[fuel]
            print(f'Fuel set to {fuel}.')
        else:
            print(f'Invalid fuel `{fuel}`.')
            self.help_fuel()

    def help_fuel(self) -> None:
        """
        Prints help message for fuel
        """
        initial_desc = 'Used to specify fuel type'
        usage = 'Usage: `fuel <fuel>`', 'ex: `fuel gas`'
        long_desc = 'Valid options: ', ' '.join(self.FUEL)
        help_message(initial_desc, usage, long_desc)

    def complete_fuel(self,
                      text: str,
                      line: str,
                      start_index: int,
                      end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.FUEL[:]
        else:
            completions = [option for option in self.FUEL if option.startswith(text)]
        return completions

    def do_color(self, color: str) -> None:
        """
        Allows user to specify color for vehicle
        :param color:
        :return: None
        """
        if color in self.COLOR:
            self.color = COLORS[color]
            print(f'Color set to {color}.')
        else:
            print(f'Invalid color: `{color}`.')
            self.help_color()

    def help_color(self) -> None:
        """
        Prints help message for color
        """
        initial_desc = 'Used to specify vehicle color'
        usage = '`color <color>`', 'ex: `color black`'
        long_desc = 'Valid options: ', ' '.join(self.COLOR)
        help_message(initial_desc, usage, long_desc)

    def complete_color(self,
                       text: str,
                       line: str,
                       start_index: int,
                       end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.COLOR[:]
        else:
            completions = [option for option in self.COLOR if option.startswith(text)]
        return completions

    def do_transmission(self, variant: str) -> None:
        """
        Allows user to specify transmission variant
        :param variant: transmission variant
        :return: None
        """
        if variant in self.TRANSMISSION:
            self.transmission = TRANSMISSION[variant]
            print(f'Transmission set to {variant}.')
        else:
            print(f'Invalid transmission: `{variant}`.')
            self.help_transmission()

    def help_transmission(self) -> None:
        """
        Prints help message for transmission
        """
        initial_desc = 'Used to specify transmission type'
        usage = '`transmission <variant>`', 'ex: `transmission manual`'
        long_desc = 'Valid options', ' '.join(self.TRANSMISSION)
        help_message(initial_desc, usage, long_desc)

    def complete_transmission(self,
                              text: str,
                              line: str,
                              start_index: int,
                              end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.TRANSMISSION[:]
        else:
            completions = [option for option in self.TRANSMISSION
                           if option.startswith(text)]
        return completions


class CarShell(SpecificOptionsShell):
    """
    Used to implement options specific to cars/trucks.  Motorcycles share all other
    options with cars
    """
    CYLINDERS = '3', '4', '5', '6', '8', '10', '12', 'other'
    DRIVE = 'fwd', 'rwd', '4wd'
    SUBTYPES = 'bus', 'convertible', 'coupe', 'hatchback', 'minivan', 'offroad', \
               'pickup', 'sedan', 'truck', 'suv', 'wagon', 'van', 'other'
    CAR_SIZE = 'compact', 'full-size', 'mid-size', 'sub-compact'

    def do_cylinders(self, count: str) -> None:
        """
        Allows user to specify cylinder count
        :param count: number of cylinders
        :return: None
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first')
            return
        if count in self.CYLINDERS:
            self.cylinders = CYLINDER_COUNT[count]
            print(f'Set cylinders to {count}.')
        else:
            print(f'Invalid cylinder count: `{count}`.')
            self.help_cylinders()

    def help_cylinders(self) -> None:
        """
        Prints help message for cylinders
        """
        initial_desc = 'Used to specify number of cylinders in vehicle engine'
        usage = 'Usage: `cylinders <count>`', 'ex: `cylinders 10`'
        long_desc = 'Can only be used with cars/trucks', 'Valid options', ' '.join(self.CYLINDERS)
        help_message(initial_desc, usage, long_desc)

    def complete_cylinders(self,
                           text: str,
                           line: str,
                           start_index: int,
                           end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.CYLINDERS[:]
        else:
            completions = [option for option in self.CYLINDERS if option.startswith(text)]
        return completions

    def do_drive_train(self, variant: str) -> None:
        """
        Allows user to specify drive train type.  e.g., 4wd, rwd or fwd
        :param variant:
        :return: None
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first.')
            return
        if variant in self.DRIVE:
            self.drive_train = DRIVETRAIN[variant]
            print(f'Drive train set to : `{variant}`.')
        else:
            print(f'Invalid variant: `{variant}`.')
            self.help_drive_train()

    def help_drive_train(self) -> None:
        """
        Prints help message for drive train
        """
        initial_desc = 'Used to specify drive train type'
        usage = 'Usage: `drive_train <variant>`', 'ex: `drivetrain 4wd`'
        long_desc = 'Can only be used with cars/trucks', 'Valid options: ', ' '.join(self.DRIVE)
        help_message(initial_desc, usage, long_desc)

    def complete_drive_train(self,
                             text: str,
                             line: str,
                             start_index: int,
                             end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.DRIVE[:]
        else:
            completions = [option for option in self.DRIVE if option.startswith(text)]
        return completions

    def do_type(self, variant: str) -> None:
        """
        Allows user to specify type of car/truck
        :param variant:
        :return: None
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first.')
            return
        if variant in self.SUBTYPES:
            self.cage_type = CAR_TYPE[variant]
            print(f'Vehicle subtype set to `{variant}`.')
        else:
            print(f'Invalid vehicle subtype: `{variant}`.')
            self.help_type()

    def help_type(self) -> None:
        """
        Prints help message for cars/trucks subtypes
        """
        initial_desc = 'Used to specify vehicle subtype'
        usage = 'Usage: `type <type>`', 'ex: `type bus`'
        long_desc = 'Can only be used with cars/trucks', 'Valid options: ', ' '.join(self.SUBTYPES)
        help_message(initial_desc, usage, long_desc)

    def complete_type(self,
                      text: str,
                      line: str,
                      start_index: int,
                      end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.SUBTYPES[:]
        else:
            completions = [option for option in self.SUBTYPES if option.startswith(text)]
        return completions

    def do_car_size(self, variant: str) -> None:
        """
        Allows user to specify car size
        :param variant:
        :return: None
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first.')
            return
        if variant in self.CAR_SIZE:
            self.cage_size = CAR_SIZE[variant]
            print(f'Car size set to {variant}.')
        else:
            print(f'Invalid car size: `{variant}`.')
            self.help_type()

    def complete_car_size(self,
                          text: str,
                          line: str,
                          start_index: int,
                          end_index: int) -> List[str]:
        """
        :param text:
        :param line:
        :param start_index:
        :param end_index:
        :return:
        """
        if not text:
            completions = self.CAR_SIZE[:]
        else:
            completions = [option for option in self.CAR_SIZE if option.startswith(text)]
        return completions

    @staticmethod
    def help_car_size():
        """
        Prints help message for car_size
        """
        initial_desc = 'Used to specify car size'
        usage = 'Usage: `car_size <size>`', 'ex: car_size full-size'
        help_message(initial_desc, usage, long_desc=None)


def help_message(initial_desc: str,
                 usage: tuple,
                 long_desc: tuple or None) -> None:
    """
    Used to simplify and standardize printing out help messages for the various
    help_XXX methods
    :param initial_desc: Short usage description
    :param usage: usage example
    :param long_desc: longer description, additional usage examples or info
    :return:
    """
    print('-' * 40)
    print(initial_desc)
    print()
    print('\n'.join(usage))
    if long_desc:
        print('*' * 80)
        print('\n'.join(long_desc))
        print('*' * 80)
