"""
Contains CLI argparser implementation
"""
from database import Database
from dicts import (BOOL_OPTIONS,
                   CAR_SELLER,
                   MOTO_SELLER)
from shell import Shell

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
        self.database = Database()
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
                      'seller_abbrev', 'database'
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
            url = base_url + '&'.join(sel_options)
            print(url)
            return url
        else:
            msg = 'At a minimum, you must set the city, seller type,' \
                  ' vehicle type and a make_model.'
            print(msg)

    def do_create_search(self, *args) -> None:
        """

        :param args:
        :return:
        """
        # Now to write the method that actually validates / adds search url to database.


if __name__ == '__main__':
    Run().cmdloop()
