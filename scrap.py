from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import os
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def custom_filter(tag):
    return tag.has_attr('data-tn-element') and tag['data-tn-element'] == "jobTitle"


def bar(href):
    return 'https://ie.indeed.com/viewjob?' + href.split('?')[1]


logger.info('Script Starting...')
url = "https://ie.indeed.com/jobs?as_and=python+developer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&radius=25&l=Dublin&fromage=any&limit=50&sort=date&psf=advsrch"
resp = requests.get(url)
logger.info('Main page received.')

target = SoupStrainer('a')
soup = BeautifulSoup(resp.text, "html.parser", parse_only=target)
jobs = soup.find_all(custom_filter)

ads = [{'title': re.sub('/', '', job.get('title')), 'url': bar(job.get('href'))} for job in jobs]

target = SoupStrainer(id="jobDescriptionText")
i = 1
folder = 'data-scraped'
extension = ".txt"
logger.info('Starting ads...')
for index, ad in enumerate(ads):
    logger.info(f'- Ad {index} - Fetch')
    resp = requests.get(ad['url'])
    logger.info(f'- Ad {index} - Fetched')
    soup = BeautifulSoup(resp.text, "html.parser", parse_only=target)
    filename = str(index) + '_' + re.sub(' ', '_', ad.get('title')) + extension
    path = os.path.join(folder, filename)
    with open(path, 'w') as file:
        file.write(str(soup))
    logger.info(f'- Ad {index} - Written')

logger.info('Script Ended.')