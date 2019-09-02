from string import Template
from bs4 import SoupStrainer
import re

""" INDEED.IE """

t_indeed_url = Template("https://ie.indeed.com/jobs?"
                        "as_and=$q_kw"
                        "&as_phr="
                        "&as_any="
                        "&as_not="
                        "&as_ttl="
                        "&as_cmp="
                        "&jt=fulltime"
                        "&st="
                        "&as_src="
                        "&radius=25"
                        "&l=$q_location"
                        "&fromage=any"
                        "&limit=50"
                        "&sort=date"
                        "&psf=advsrch")


def ad_anchor_indeed(tag):
    """ Beautiful Soup filtering - Select job ads anchors. """
    return str(tag.name) == 'a' and tag.has_attr('data-tn-element') and tag['data-tn-element'] == 'jobTitle'


def ad_filter_title(tag):
    return tag.has_attr('class') and 'jobsearch-JobInfoHeader-title' in tag['class']


def ad_filter_text(tag):
    return tag.has_attr('id') and tag['id'] == 'jobDescriptionText'


def id_from_url_indeed(url):
    match = re.search(r"^.*jk=(.*)&fccid=.*$", url)
    return match.group(1)


def get_ad_url_indeed(tag):
    """ Complete ad's URL"""
    radical = 'https://ie.indeed.com/viewjob?'
    href = tag.get('href')
    return radical + href.split('?')[1]


target_indeed_title = SoupStrainer(ad_filter_title)
target_indeed_text = SoupStrainer(id="jobDescriptionText")
