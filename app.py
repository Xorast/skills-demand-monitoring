# APP

import logging
from search import Search
import mongo
from indeed import indeed


logging.basicConfig(level=logging.DEBUG)

python_dev = Search(**indeed, query={'kw': 'python+developer', 'location': 'Dublin'})
results = python_dev.go()
found_ads = {ad['id_'] for ad in results}

stored_ads = mongo.collections["indeed"].find({}, {"id_": 1, "_id": 0})
stored_ads = {ad['id_'] for ad in stored_ads}

new_ads = found_ads - stored_ads
new_results = [ad for ad in results if ad['id_'] in new_ads]

print("TEST")
print(new_results)
# mongo.collections['indeed'].insert_many(new_results)

