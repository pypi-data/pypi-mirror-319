from .get_content import extract_tweet_data
from .get_page_source import get_tweet_html

def get(tweet_url,Debug=False):
    page_source = get_tweet_html(tweet_url,Debug)
    info = extract_tweet_data(page_source,Debug)
    return info
