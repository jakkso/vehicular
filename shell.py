try:
    import gnureadline
except ImportError:
    import readline
    gnureadline = readline
import cmd
import sys

sys.modules['readline'] = gnureadline


class BaseShell(cmd.Cmd):
    """
    Creates shell environment

    For cmd.Cmd subclasses, there are several special methods that come in the
    form of do_XXX, complete_XXX and help_XXX.

    do_XXX: Inside the shell created by running cmd.Cmd().cmdloop(), when the user types
        command `XXX` and presses enter, do_XXX is called, passing whatever argument follows
        command `XXX`.

    complete_XXX: This is used to enable bash-style auto-completion upon pressing tab.
        It takes 4 parameters:
            text: the text after the command
            line: the entire line
            start_index: start index of `text`
            end_index: end index of `text`
        The way it's implemented is that if `text` is empty, then the entire list
        of potential options is returned. Otherwise, a list of items that start with `text`
        is returned.

        The user types the command followed by a partial option, presses tab.  If the
        partial option is close to a single option, that option replaces the partial option.
        Otherwise, the system bell sounds.  If there are no matches, successive tab key presses
        just ring the system bell.  If there are multiple matches, pressing tab prints the
        partial matches.

    help_XXX: Is called when user types help XXX.
    """

    with open('city.txt') as file:
        CITIES = file.read().split('\n')
    VEHICLE_TYPES = 'motorcycle', 'cars/trucks'
    SELLER_TYPES = 'dealer', 'owner', 'both'

    def __init__(self):
        super(BaseShell, self).__init__()
        #  Required args
        self.city = None
        self.vehicle_type = None
        self.make_model = None
        self.seller_type = None
        #  Boolean options
        self.has_images = False
        self.posted_today = False
        self.crypto = False
        self.nearby_areas = False
        #  Open ended, numerical options
        self.zip_code = None
        self.distance_from_zip = None
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

    def do_EOF(self, line: str) -> True:
        """
        Allows user to exit shell upon using the standard `ctrl + d`
        :param line:
        :return:
        """
        print('Exiting shell...')
        return True

    def help_EOF(self) -> None:
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
            print(f'Invalid city: `{city}`.  Be sure to enter exactly what is suggested')

    def complete_city(self, text: str, line: str, start_index: int, end_index: int) -> list:
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

    def help_city(self) -> None:
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
                self.cylinders = None
                self.drive_train = None
                self.cage_type = None
            self.vehicle_type = vehicle_type
            print(f'Vehicle type set to {self.vehicle_type}.')
        else:
            print(f'Invalid vehicle type: `{vehicle_type}`.')
            self.help_vehicle_type()

    def complete_vehicle_type(self, text: str, line: str, start_index: int, end_index: int) -> list:
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
            completions = [type_ for type_ in self.VEHICLE_TYPES if type_.startswith(text)]
        return completions

    def help_vehicle_type(self) -> None:
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

    def complete_seller_type(self, text: str, line: str, start_index: int, end_index: int) -> list:
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
            completions = [option for option in self.SELLER_TYPES if option.startswith(text)]
        return completions

    def help_seller_type(self) -> None:
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
    def do_has_images(self, arg) -> None:
        """
        Toggles self.has_images
        """
        print(f'Posts must have images: {not self.has_images}.')
        self.has_images = not self.has_images

    def help_has_images(self) -> None:
        """
        Prints has_images help message
        """
        initial_desc = 'Used to toggle has_images option'
        usage = 'Type `has_images` and press enter.',\
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_posted_today(self, arg) -> None:
        """
        Toggles self.posted_today
        """
        print(f'Posts must have been posted today: {not self.posted_today}')
        self.posted_today = not self.posted_today

    def help_posted_today(self) -> None:
        """
        Prints posted_today help message
        """
        initial_desc = 'Used to toggle posted_today option'
        usage = 'Type `posted_today` and press enter.', \
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)

    def do_crypto(self, arg) -> None:
        """
        Toggles self.crypto
        """
        print(f'Posts must accept payment in cryptocurrency: {not self.crypto}')
        self.crypto = not self.crypto

    def help_crypto(self) -> None:
        """
        Prints crypto help message
        """
        print('-' * 40)
        print()
        initial_desc = 'Used to toggle cryptocurrency option'
        usage = 'Type `crypto` and press enter.', \
                'Program prints the current status after it has been set.'
        help_message(initial_desc, usage, long_desc=None)


class OpenEndedShell(BoolShell):
    """
    Further Extends the shell to include open ended option inputs
    """
    def do_zip_code(self, zip_code: str) -> None:
        """
        Sets self.zip_code to zip_code
        """
        self.zip_code = zip_code
        print(f'Zip code set to: {self.zip_code}.')

    def help_zip_code(self) -> None:
        """
        Prints help message for zip_code
        """
        initial_desc = 'Used to specify zip / postal code'
        usage = 'Usage: `zip_code <zip_code>`',\
                'ex: `zip_code 10001` specifies zip code 10001'
        help_message(initial_desc, usage, long_desc=None)

    def do_distance_from_zip(self, distance: str) -> None:
        """
        Sets self.distance_from_zip to distance
        """
        if self.zip_code:
            self.distance_from_zip = distance
            print(f'Distance from zip code set to: {self.distance_from_zip}.')
        else:
            print('You must first set a zip code in order to have a distance from it.')

    def help_distance_from_zip(self) -> None:
        """
        Prints help message for distance_from_zip
        """
        initial_desc = 'Used to specify distance from zip code'
        usage = 'Usage: `distance_from_zip <distance>`', 'ex: `distance_from_zip 500`'
        long_desc = 'In order for this option to work, you must first set the zip code.',
        help_message(initial_desc, usage, long_desc)

    def do_min_price(self, price) -> None:
        """
        Sets self.min_price to price
        """
        try:
            price = int(price)
        except ValueError:
            print(f'Invalid price: `{price}`')
            return
        self.min_price = price
        print(f'Min price set to: {self.min_price}.')

    def help_min_price(self) -> None:
        """
        Prints help message for min_price
        """
        initial_desc = 'Used to specify minimum price'
        usage = 'Usage: `min_price <price>`', 'ex: `min_price 1000`'
        long_desc = 'Price must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_price(self, price) -> None:
        """
        Sets self.max_price to price
        """
        try:
            price = int(price)
        except ValueError:
            print(f'Invalid price: `{price}`')
            return
        self.max_price = price
        print(f'Max price set to: {self.max_price}.')

    def help_max_price(self) -> None:
        """
        Prints help message for max_price
        """
        initial_desc = 'Used to specify maximum price'
        usage = 'Usage: `max_price <price>`', 'ex: `max_price 1000`'
        long_desc = 'Price must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_min_miles(self, miles) -> None:
        """
        Sets self.min_miles to miles
        """
        try:
            miles = int(miles)
        except ValueError:
            print(f'Invalid miles: `{miles}`')
            return
        self.min_miles = miles
        print(f'Minimum miles set to: {self.min_miles}.')

    def help_min_miles(self) -> None:
        """
        Prints help message for min_miles
        """
        initial_desc = 'Used to specify minimum mileage'
        usage = 'Usage: `min_miles <miles>`', 'ex: `min_miles 10000`'
        long_desc = 'Miles must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_miles(self, miles) -> None:
        """
        Sets self.max_miles to miles
        """
        try:
            miles = int(miles)
        except ValueError:
            print(f'Invalid miles: `{miles}`')
            return
        self.max_miles = miles
        print(f'Maximum miles set to: {self.max_miles}.')

    def help_max_miles(self) -> None:
        """
        Prints help message for max_miles
        """
        initial_desc = 'Used to specify maximum mileage'
        usage = 'Usage: `max_miles <miles>`', 'ex: `max_miles 10000`'
        long_desc = 'Miles must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_max_year(self, year) -> None:
        """
        Sets self.max_year to year
        """
        try:
            year = int(year)
        except ValueError:
            print(f'Invalid year: `{year}`')
            return
        self.max_year = year
        print(f'Maximum year set to: {self.max_year}.')

    def help_max_year(self) -> None:
        """
        Prints help message for max_year
        """
        initial_desc = 'Used to specify maximum year'
        usage = 'Usage: `max_year <year>`', 'ex: `max_year 10000`'
        long_desc = 'Year must be a number',
        help_message(initial_desc, usage, long_desc)

    def do_min_year(self, year) -> None:
        """
        Sets self.min_year to year
        """
        try:
            year = int(year)
        except ValueError:
            print(f'Invalid year: `{year}`')
            return
        self.min_year = year
        print(f'Minimum year set to: {self.min_year}.')

    def help_min_year(self) -> None:
        """
        Prints help message for min_year
        """
        initial_desc = 'Used to specify minimum year'
        usage = 'Usage: `min_year <year>`', 'ex: `min_year 10000`'
        long_desc = 'Year must be a number',
        help_message(initial_desc, usage, long_desc)


class SpecificOptionsShell(OpenEndedShell):
    """
    Used to implement options that have specific options
    """
    CONDITIONS = 'any', 'new', 'like-new', 'excellent', 'good', 'fair', 'salvage'
    FUEL = 'any', 'gas', 'diesel', 'hybrid', 'electric', 'other'
    COLOR = 'any', 'black', 'blue', 'brown', 'green', 'grey', 'orange', 'purple', \
            'red', 'silver', 'white', 'yellow', 'other'
    TRANSMISSION = 'any', 'manual', 'automatic', 'other'
    TITLE_STATUS = 'any', 'clean', 'salvage', 'rebuilt', 'parts-only', 'lien', 'missing'

    def do_condition(self, condition) -> None:
        """

        :param condition:
        :return:
        """
        if condition in self.CONDITIONS:
            self.condition = condition
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

    def complete_condition(self, text: str, line: str, start_index: int, end_index: str) -> list:
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
            completions = [option for option in self.CONDITIONS if option.startswith(text)]
        return completions

    def do_title_status(self, status: str) -> None:
        """

        :param status:
        :return:
        """
        if status in self.TITLE_STATUS:
            self.title_status = status
        else:
            print(f'Invalid title status: `{status}`')
            self.help_title_status()

    def help_title_status(self) -> None:
        """
        Prints help message for title_status
        """
        initial_desc = 'Used to specify title status'
        usage = 'Usage: `title_status <status>`', 'ex: `title_status lien`'
        long_desc = 'Valid options: ', ' '.join(self.TITLE_STATUS)
        help_message(initial_desc, usage, long_desc)

    def complete_title_status(self, text: str, line: str, start_index: int, end_index: str) -> list:
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
            completions = [option for option in self.TITLE_STATUS if option.startswith(text)]
        return completions

    def do_fuel(self, fuel: str) -> None:
        """

        :param fuel:
        :return:
        """
        if fuel in self.FUEL:
            self.fuel = fuel
            print(f'Fuel set to {fuel}')
        else:
            print(f'Invalid fuel `{fuel}`')
            self.help_fuel()

    def help_fuel(self) -> None:
        """
        Prints help message for fuel
        """
        initial_desc = 'Used to specify fuel type'
        usage = 'Usage: `fuel <fuel>`', 'ex: `fuel gas`'
        long_desc = 'Valid options: ', ' '.join(self.FUEL)
        help_message(initial_desc, usage, long_desc)

    def complete_fuel(self, text: str, line: str, start_index: int, end_index: str) -> list:
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
        Specifies color for vehicle
        """
        if color in self.COLOR:
            self.color = color
            print(f'Color set to {color}')
        else:
            print(f'Invalid color: `{color}`')
            self.help_color()

    def help_color(self) -> None:
        """
        Prints help message for color
        """
        initial_desc = 'Used to specify vehicle color'
        usage = '`color <color>`', 'ex: `color black`'
        long_desc = 'Valid options: ', ' '.join(self.COLOR)
        help_message(initial_desc, usage, long_desc)

    def complete_color(self, text: str, line: str, start_index: int, end_index: str) -> list:
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

        :param variant: transmission variant
        :return:
        """
        if variant in self.TRANSMISSION:
            self.transmission = variant
            print(f'Transmission set to {self.transmission}')
        else:
            print(f'Invalid transmission: `{self.transmission}`')
            self.help_transmission()

    def help_transmission(self) -> None:
        """
        Prints help message for transmission
        """
        initial_desc = 'Used to specify transmission type'
        usage = '`transmission <variant>`', 'ex: `transmission manual`'
        long_desc = 'Valid options', ' '.join(self.TRANSMISSION)
        help_message(initial_desc, usage, long_desc)

    def complete_transmission(self, text: str, line: str, start_index: int, end_index: str) -> list:
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
            completions = [option for option in self.TRANSMISSION if option.startswith(text)]
        return completions


class Shell(SpecificOptionsShell):
    """
    Used to implement options specific to cars/trucks.  Motorcycles share all other
    options with cars
    """
    CYLINDERS = 'any', '3', '4', '5', '6', '8', '10', '12', 'other'
    DRIVE = 'any', 'fwd', 'rwd', '4wd'
    SUBTYPES = 'any', 'bus','convertible', 'coupe', 'hatchback', 'minivan', 'offroad', \
               'pickup', 'sedan', 'truck', 'suv', 'wagon', 'van', 'other'

    def do_cylinders(self, count: str) -> None:
        """

        :param count:
        :return:
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first')
            return
        if count in self.CYLINDERS:
            self.cylinders = count
            print(f'Set cylinders to {self.cylinders}.')
        else:
            print(f'Invalid cylinder count: `{count}`')
            self.help_cylinders()

    def help_cylinders(self) -> None:
        """
        Prints help message for cylinders
        """
        initial_desc = 'Used to specify number of cylinders in vehicle engine'
        usage = 'Usage: `cylinders <count>`', 'ex: `cylinders 10`'
        long_desc = 'Can only be used with cars/trucks', 'Valid options', ' '.join(self.CYLINDERS)
        help_message(initial_desc, usage, long_desc)

    def complete_cylinders(self, text: str, line: str, start_index: int, end_index: str) -> list:
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

        :param variant:
        :return:
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first')
            return
        if variant in self.DRIVE:
            self.drive_train = variant
            print(f'Drive train set to : {self.drive_train}')
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

    def complete_drive_train(self, text: str, line: str, start_index: int, end_index: str) -> list:
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

        :param variant:
        :return:
        """
        if self.vehicle_type != 'cars/trucks':
            print('Set vehicle type to cars/trucks first')
            return
        if variant in self.SUBTYPES:
            self.cage_type = variant
            print(f'Vehicle subtype set to {self.cage_type}.')
        else:
            print(f'Invalid vehicle subtype: `{variant}`.')
            self.help_type()

    def help_type(self) -> None:
        """
        Prints help message for subtypes option
        """
        initial_desc = 'Used to specify vehicle subtype'
        usage = 'Usage: `type <type>`', 'ex: `type bus`'
        long_desc = 'Can only be used with cars/trucks', 'Valid options: ', ' '.join(self.SUBTYPES)
        help_message(initial_desc, usage, long_desc)

    def complete_type(self, text: str, line: str, start_index: int, end_index: str) -> list:
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


def help_message(initial_desc: str, usage: list or tuple, long_desc: list or tuple) -> None:
    """
    Used to simplify and standardize printing out help messages for various
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


if __name__ == '__main__':
    Shell().cmdloop()
