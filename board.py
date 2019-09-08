import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Search:

    def __init__(self, domain=None, query_template=None, query=None, target_pages=None, target_anchor=None, get_ad_url=None):
        self.domain = domain
        self.query_template = self.domain + query_template
        self.query = query
        self.target_pages = target_pages
        self.target_anchor = target_anchor  # filter
        self.get_ad_url = get_ad_url
        self.results_pages = None
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
            pages_tags = soup.find_all(self.target_pages)
            self.results_pages = [tag.get('href') for tag in pages_tags]
            self.results_pages.insert(0, url)

    @staticmethod
    def _get_ads_tags(text, filter):
        """ Returns the ads tags in the html code """
        soup = BeautifulSoup(text, "html.parser")   # Need to optimise using SoupStrainer !
        ads_tags = soup.find_all(filter)
        return ads_tags

    def _get_all_ads_tags(self):
        self.ads_tags = list()
        for page in self.results_pages:
            resp = requests.get(page)
            page_tags = self._get_ads_tags(resp.text, self.target_anchor)
            for tag in page_tags:
                self.ads_tags.append(tag)

    def _get_ads_url(self):
        self.ads_url = {self.get_ad_url(tag) for tag in self.ads_tags}  # add another check for unique job id

    def _generate_ads(self):
        self.ads = [Ad.from_url(url, self.target_title, self.target_text, self.extract_id) for url in self.ads_urls]

    def go(self):
        self._get_results_pages()
        self._get_all_ads_tags()
        self._get_ads_url()
        self._generate_ads()


class Ad:

    def __init__(self, title=None, id_=None, url=None, text=None):
        self.id_ = id_
        self.url = url
        self.text = text
        self.title = title

    @classmethod
    def from_url(cls, url, target_title=None, target_text=None, extract_id=None):
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            logger.info(f'Ad url request failed: {resp.status_code}')
        else:
            soup = BeautifulSoup(resp.text, 'html.parser')
            title_r = soup.find(target_title)
            title = str(title_r.string)  # if title_r else 'None'
            text_r = soup.find(target_text)
            text = str(text_r)  # if text_r else 'None'
            id_ = str(extract_id(url))

            return cls(title=title,
                       id_=id_,
                       url=url,
                       text=text)

    def to_dict(self):
        return vars(self)


def get_results_page(q_template, query):
    url = q_template.substitute(**query)
    resp = requests.get(url)
    return resp


def get_ads_tags(text, filter):
    soup = BeautifulSoup(text, "html.parser")
    ads_tags = soup.find_all(filter)
    return ads_tags


def get_ads_url(ads_tags, get_ad_url):
    ads_url = [get_ad_url(tag) for tag in ads_tags]
    return ads_url


def ads_from_urls(urls, target_title=None, target_text=None, extract_id=None):
    return [Ad.from_url(url, target_title, target_text, extract_id) for url in urls]
