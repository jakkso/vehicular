MOTO_SELLER = {
    'dealer': 'mcd',
    'owner': 'mco',
    'all': 'mca'
}

CAR_SELLER = {
    'dealer': 'ctd',
    'owner': 'cto',
    'all': 'cta'
}

BOOL_OPTIONS = {
    'titles_only': 'srchType=T',
    'has_images': 'hasPic=1',
    'posted_today': 'postToday=1',
    'crypto_okay': 'crypto_currency_ok=1',
    'nearby_areas': 'searchNearby=1'}

PRETTY_BOOL = {
    'titles_only': 'Search titles only',
    'has_images': 'Search must have images',
    'posted_today': 'Only search for items posted today',
    'crypto_okay': 'Cryptocurrency is okay',
    'nearby_areas': 'Include nearby areas'}

PRETTY_RADIO = {
    'auto_title_status=1': 'Title: Clean',
    'auto_title_status=2': 'Title: Salvage',
    'auto_title_status=3': 'Title: Rebuilt',
    'auto_title_status=4': 'Title: Parts only',
    'auto_title_status=5': 'Title: Lien',
    'auto_title_status=6': 'Title: Missing title',
    'condition=10': 'Condition: New',
    'condition=20': 'Condition: Like new',
    'condition=30': 'Condition: Excellent',
    'condition=40': 'Condition: Good',
    'condition=50': 'Condition: Fair',
    'condition=60': 'Condition: Salvage',
    'auto_fuel_type=1': 'Fuel: Gas',
    'auto_fuel_type=2': 'Fuel: Diesel',
    'auto_fuel_type=3': 'Fuel: Hybrid',
    'auto_fuel_type=4': 'Fuel: Electric',
    'auto_fuel_type=6': 'Fuel: Other',
    'auto_paint=1': 'Color: Black',
    'auto_paint=2': 'Color: Blue',
    'auto_paint=20': 'Color: Brown',
    'auto_paint=3': 'Color: Green',
    'auto_paint=4': 'Color: Grey',
    'auto_paint=5': 'Color: Orange',
    'auto_paint=6': 'Color: Purple',
    'auto_paint=7': 'Color: Red',
    'auto_paint=8': 'Color: Silver',
    'auto_paint=9': 'Color: White',
    'auto_paint=10': 'Color: Yellow',
    'auto_paint=11': 'Color: Other',
    'auto_transmission=1': 'Transmission: Manual',
    'auto_transmission=2': 'Transmission: Automatic',
    'auto_transmission=3': 'Transmission: Other',
    'auto_cylinders=1': 'Cylinders: 3',
    'auto_cylinders=2': 'Cylinders: 4',
    'auto_cylinders=3': 'Cylinders: 5',
    'auto_cylinders=4': 'Cylinders: 6',
    'auto_cylinders=5': 'Cylinders: 8',
    'auto_cylinders=6': 'Cylinders: 10',
    'auto_cylinders=7': 'Cylinders: 12',
    'auto_cylinders=8': 'Cylinders: Other',
    'auto_drivetrain=1': 'Drive: FWD',
    'auto_drivetrain=2': 'Drive: RWD',
    'auto_drivetrain=3': 'Drive: 4WD',
    'auto_size=1': 'Size: Compact',
    'auto_size=2': 'Size: Full-size',
    'auto_size=3': 'Size: Mid-size',
    'auto_size=4': 'Size: Sub-compact',
    'auto_bodytype=1': 'Type: Bus',
    'auto_bodytype=2': 'Type: Convertible',
    'auto_bodytype=3': 'Type: Coupe',
    'auto_bodytype=4': 'Type: Hatchback',
    'auto_bodytype=5': 'Type: Mini-van',
    'auto_bodytype=6': 'Type: Offroad',
    'auto_bodytype=7': 'Type: Pickup',
    'auto_bodytype=8': 'Type: Sedan',
    'auto_bodytype=9': 'Type: Truck',
    'auto_bodytype=10': 'Type: SUV',
    'auto_bodytype=11': 'Type: Wagon',
    'auto_bodytype=12': 'Type: Van',
    'auto_bodytype=13': 'Type: Other'}

PRETTY_STRING = {
    'auto_make_model': 'Make & model: ',
    'postal': 'Postal code: ',
    'search_distance': 'Search distance: ',
    'min_auto_year': 'Min year: ',
    'max_auto_year': 'Max year: ',
    'min_auto_miles': 'Min miles: ',
    'max_auto_miles': 'Max miles: ',
    'min_price': 'Min price: ',
    'max_price': 'Max price: '}
