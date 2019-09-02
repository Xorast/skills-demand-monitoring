import requests
import logging
from bs4 import BeautifulSoup, SoupStrainer
from analysis import filter, analysis
from boards import t_indeed_url, get_ad_url_indeed, ad_anchor_indeed, id_from_url_indeed, \
                   target_indeed_title, target_indeed_text


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Ad:

    def __init__(self, title=None, id_=None, url=None, text=None):
        self.id_ = id_
        self.url = url
        self.text = text
        self.title = title

    @classmethod
    def from_url(cls, url, target_title=None, target_text=None, extract_id=None):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_r = soup.find(target_title)
        title = str(title_r.string)
        text_r = soup.find(target_text)
        text = str(text_r)
        id_ = str(extract_id(url))

        return cls(title=title,
                   id_=id_,
                   url=url,
                   text=text)


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


query = {'q_kw': 'python+developer', 'q_location': 'Dublin'}
resp = get_results_page(t_indeed_url, query)

ads_tags = get_ads_tags(resp.text, ad_anchor_indeed)
ads_url = get_ads_url(ads_tags, get_ad_url_indeed)
ads = ads_from_urls(ads_url,
                    target_title=target_indeed_title, target_text=target_indeed_text, extract_id=id_from_url_indeed)
