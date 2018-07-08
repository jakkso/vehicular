"""
Contains CLI argparser implementation
"""

from argparse import ArgumentParser as Ag

from shell import Shell


def parser_creator() -> Ag:
    """
    Creates argument parser object containing various options to create a craigslist search RSS URL
    :return: Argument parser
    """
    parser = Ag()
    # Required arguments
    parser.add_argument('vehicle_type', help='Type of vehicle.  Valid options: '
                                             'motorcycle, cars-trucks')
    parser.add_argument('city', help='City craigslist in which to search')
    parser.add_argument('make_model', help='Make and model to search for')
    parser.add_argument('seller_type', help='Search for vehicles for sale by seller type.'
                                            'Valid options: dealer, owner, all')
    # Optional boolean args
    parser.add_argument('--has_images', action='store_true', help='Only return search '
                                                                  'results that have images')
    parser.add_argument('--posted_today', action='store_true', help='Only return search '
                                                                    'results that were posted today')
    parser.add_argument('--crypto', action='store_true', help='Include results that are '
                                                              'okay with payment using cryptocurrency')
    parser.add_argument('--nearby_areas', action='store_true', help='Search nearby areas '
                                                                    'in addition to specified city')
    # TODO make sure that zip and distance from zip are linked in validator
    parser.add_argument('--zip_code', help='Which zip code to search')
    parser.add_argument('--distance_from_zip', help='What distance from zip code to search')

    parser.add_argument('--min_price', help='Minimum price to specify')
    parser.add_argument('--max_price', help='Maximum price to specify')
    parser.add_argument('--min_year', help='Minimum model year')
    parser.add_argument('--max_year', help='Maximum model year')
    parser.add_argument('--min_miles', help='Minimum mileage')
    parser.add_argument('--max_miles', help='Maximum mileage')

    parser.add_argument('--title_status', help='Title status of vehicle.'
                                               '  Valid options: any, clean, salvage,'
                                               ' rebuilt, parts-only, lien, missing')
    parser.add_argument('--vehicle_condition', help='Vehicle condition.'
                                                    '  Valid options: any, new, like new,'
                                                    ' excellent, good, fair, salvage')
    parser.add_argument('--fuel', help='Fuel type.  Valid options: any, gas diesel, '
                                       'hybrid, electric, other')
    parser.add_argument('--color', help='Valid options: any, black, blue, brown, green,'
                                        ' grey, orange, purple, red, silver, white, '
                                        'yellow, other')
    parser.add_argument('--transmission', help='Transmission type.  Valid options: any, '
                                               'manual, automatic, other')
    # TODO motorcycle searches don't use the following
    parser.add_argument('--cylinders', help='Cylinder number.  Valid options: any, 3, 4,'
                                            ' 5, 6, 8, 10, 12, other')
    parser.add_argument('--drive', help='Drive train.  Valid options: any, fwd, rwd, 4wd')
    parser.add_argument('--type', help='Vehicle type.  Valid options: any, bus, '
                                       'convertible, coupe, hatchback, minivan, offroad,'
                                       ' pickup, sedan, truck, suv, wagon, van, other')
    return parser


# Get options from user
    # Cities are the real sticking point: there are ~700 valid cities
    # The JS version of CLNotify use a form of autocorrect to get the spelling correct
    # What to do here? I'd like to allow the user to cities.  Perhaps some sort of CLI autocomplete library?
    # Looks like our solution is a custom shell built using the cmd library and gnureadline!  Woohoo!

class Run(Shell):
    """

    """
    def __init__(self):
        super(Run, self).__init__()
        self.database = ''



# convert rec'd options into URL formatted options via dicts
# Combine URL formatted options into single rss feed url
# Add to database, update, refresh, etc, essentially copy from CLNotify

# def main() -> None:
#     parser = parser_creator()
#     args = parser.parse_args()
#
#     # Required args
#     vehicle_type = args.vehicle_type
#     city = args.city
#     make_model = args.make_model
#     seller_type = args.seller_type
#
#     if vehicle_type == 'motorcycle':
#         seller = MOTO_SELLER[seller_type]
#     elif vehicle_type == 'cars-trucks':
#         seller = CAR_SELLER[seller_type]
#     try:
#         base_url = f'{CITIES[city]}{seller}?format=rss'
#     except IndexError:
#         print('Invalid city')
#     for option in vars(args).items():
#         key, value = option
#         if value:
#             pass
#
#
# def bool_subparser(parser: Ag.add_subparsers) -> Ag:
#     """
#     Creates sub-parser for boolean options
#     :return:
#     """
#
# if __name__ == '__main__':
#     main()


