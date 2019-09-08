# APP
import requests
import logging

from board import get_results_page, get_ads_tags, get_ads_url, ads_from_urls
from indeed import t_indeed_url, get_ad_url_indeed, ad_anchor_indeed, id_from_url_indeed, \
                   target_indeed_title, target_indeed_text

from mongo import co_indeed


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

query = {'q_kw': 'python+developer', 'q_location': 'Dublin'}
resp = get_results_page(t_indeed_url, query)

if resp.status_code != requests.codes.ok:
    logger.info(f'Initial request failed: {resp.status_code}')
else:
    ads_tags = get_ads_tags(resp.text, ad_anchor_indeed)
    ads_url = get_ads_url(ads_tags, get_ad_url_indeed)
    ads = ads_from_urls(ads_url, target_title=target_indeed_title,
                        target_text=target_indeed_text, extract_id=id_from_url_indeed)

    co_indeed.insert_many([ad.to_dict() for ad in ads if ad is not None])
