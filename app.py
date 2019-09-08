# APP

import logging
from search import Search
from indeed import indeed
import mongo


logging.basicConfig(level=logging.DEBUG)

python_dev = Search(**indeed, query={'kw': 'developer', 'location': 'Dublin'})
results = python_dev.go()
found_ads = {ad['id_'] for ad in results}

stored_ads = mongo.collections["developer"].find({}, {"id_": 1, "_id": 0})
stored_ads = {ad['id_'] for ad in stored_ads}

new_ads = found_ads - stored_ads
new_results = [ad for ad in results if ad['id_'] in new_ads]

mongo.collections['developer'].insert_many(new_results)

