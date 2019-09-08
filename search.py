import logging
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class Search:

    def __init__(self, domain=None, query_template=None, filters=None, get_ad_url=None, get_ad_id=None, query=None):
        self.domain = domain
        self.query_template = query_template
        self.filters = filters
        self.get_ad_url = get_ad_url
        self.get_ad_id = get_ad_id
        self.query = query
        self.pages = None
        self.ads_tag = None
        self.ads_url = None
        self.ads = None

    def _get_results_pages(self):
        """ Returns the list of the results page's url (pagination) """
        url = self.query_template.substitute(**self.query)
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            logger.warning(f'Initial request failed: {resp.status_code} - Check the domain and query template')
        else:
            soup = BeautifulSoup(resp.text, "html.parser")
            pages_tags = soup.find_all(self.filters['pages'])
            self.pages = [self.domain + tag.get('href') for tag in pages_tags]
            self.pages.insert(0, url)

    @staticmethod
    def _get_ads_tags(text, target):
        """ Returns the ads tags in the html code """
        soup = BeautifulSoup(text, "html.parser")   # Need to optimise using SoupStrainer !
        ads_tags = soup.find_all(target)
        return ads_tags

    def _get_all_ads_tags(self):
        self.ads_tags = list()
        for page in self.pages:
            resp = requests.get(page)
            tags = self._get_ads_tags(resp.text, self.filters['ad_tags'])
            for tag in tags:
                self.ads_tags.append(tag)

    def _get_ads_url(self):
        self.ads_url = {self.get_ad_url(tag) for tag in self.ads_tags}  # add another check for unique job id

    def _generate_ads(self):
        self.ads = [Ad.from_url(url, filter_title=self.filters['title'],
                                filter_text=self.filters['text'], get_id=self.get_ad_id) for url in self.ads_url]
        self.ads = list(filter(None, self.ads))

    def go(self):
        self._get_results_pages()
        self._get_all_ads_tags()
        self._get_ads_url()
        self._generate_ads()
        return [ad.to_dict() for ad in self.ads]


class Ad:

    def __init__(self, title=None, id_=None, url=None, text=None):
        self.id_ = id_
        self.url = url
        self.text = text
        self.title = title

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_url(cls, url, filter_title=None, filter_text=None, get_id=None):
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            logger.info(f'Ad url request failed: {resp.status_code}')
        else:
            soup = BeautifulSoup(resp.text, 'html.parser')
            title_r = soup.find(filter_title)
            title = str(title_r.string)  # if title_r else 'None'
            text_r = soup.find(filter_text)
            text = str(text_r)  # if text_r else 'None'
            id_ = str(get_id(url))

            return cls(title=title,
                       id_=id_,
                       url=url,
                       text=text)
