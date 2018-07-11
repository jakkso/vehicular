from command import Run

r = Run()
r.vehicle_type = 'motorcycle'
r.seller_type = 'all'
r.city = 'denver'
r.make_model = 'ferd+fteenthousand'
r.titles_only = True
r.has_images = True
r. posted_today = True
r.crypto_okay = True
r.nearby_areas = True
url = r.search_url
