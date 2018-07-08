from dicts import (CITIES,
                   CAR_SELLER,
                   MOTO_SELLER,
                   BOOL_OPTIONS,
                   PRETTY_BOOL,
                   PRETTY_RADIO,
                   PRETTY_STRING)


def url_parser(form_data):
    """
    :param form_data: wtform form data
    :return: str, concatenated URL based upon the values of form_data
    """
    bool_items = ('titles_only', 'has_images', 'posted_today', 'crypto_okay',
                  'nearby_areas')
    radio_items = ('title', 'transmission', 'cylinders', 'drive',
                   'size', 'type')
    string_items = ('auto_make_model', 'postal', 'search_distance',
                    'min_auto_year', 'max_auto_year', 'min_auto_miles',
                    'max_auto_miles', 'min_price', 'max_price')
    misc = ('city', 'seller_type')
    search_items = bool_items + radio_items + string_items + misc

    options = []
    rendered_options = []
    search_selections = {item: form_data[item] for item in form_data if item in search_items}

    if 'cylinders' in search_selections:
        base_url = f'{CITIES[search_selections["city"]]}{CAR_SELLER[search_selections["seller_type"]]}?format=rss'
    else:
        base_url = f'{CITIES[search_selections["city"]]}{MOTO_SELLER[search_selections["seller_type"]]}?format=rss'

    for item in search_selections:
        if item in bool_items:
            if search_selections[item]:
                options.append(BOOL_OPTIONS[item])
                rendered_options.append(PRETTY_BOOL[item])
        if item in radio_items and search_selections[item] != 'any':
            options.append(search_selections[item])
            rendered_options.append(PRETTY_RADIO[search_selections[item]])
        if item in string_items and search_selections[item] != '':
            options.append(f'{item}={search_selections[item]}')
            rendered_options.append(f'{PRETTY_STRING[item]}{search_selections[item]}')
    if options:
        url = '&'.join([base_url, '&'.join(options)])
    else:
        url = base_url
    return url, ','.join(rendered_options)
