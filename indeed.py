# BOARD: INDEED.IE

from string import Template
import re
from bs4 import SoupStrainer


def filter_ad_tag(tag):  # get_ad_tag()
    """ Beautiful Soup filtering - Select job ads anchors. """
    return str(tag.name) == 'a' and tag.has_attr('data-tn-element') and tag['data-tn-element'] == 'jobTitle'


def filter_ad_title(tag):
    return tag.has_attr('class') and 'jobsearch-JobInfoHeader-title' in tag['class']


def filter_pages_url(tag):
    return tag.has_attr('data-pp')


def get_ad_id(url):
    match = re.search(r"^.*jk=(.*)&fccid=.*$", url)
    return match.group(1)


def get_ad_url(tag):  # get_ad_url()
    """ Complete ad's URL"""
    radical = 'https://ie.indeed.com/viewjob?'
    href = tag.get('href')
    return radical + href.split('?')[1]


indeed = {'domain': 'https://ie.indeed.com/',
          'query_template': Template("https://ie.indeed.com/jobs?"
                                     "as_and=$kw"
                                     "&as_phr="
                                     "&as_any="
                                     "&as_not="
                                     "&as_ttl="
                                     "&as_cmp="
                                     "&jt=fulltime"
                                     "&st="
                                     "&as_src="
                                     "&radius=25"
                                     "&l=$location"
                                     "&fromage=any"
                                     "&limit=50"
                                     "&sort=date"
                                     "&psf=advsrch"),
          'get_ad_url': get_ad_url,
          'get_ad_id': get_ad_id,
          'filters': {'pages': SoupStrainer(filter_pages_url),
                      'ad_tags': filter_ad_tag,
                      'title': SoupStrainer(filter_ad_title),
                      'text': SoupStrainer(id="jobDescriptionText")}}
