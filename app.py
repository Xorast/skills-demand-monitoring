# APP
import logging
from search import Search
import mongo
from indeed import indeed


logging.basicConfig(level=logging.DEBUG)

python_dev = Search(**indeed, query={'kw': 'python+developer', 'location': 'Dublin'})
results = python_dev.go()
mongo.collections['indeed'].insert_many(results)
