from bs4 import BeautifulSoup
import requests


def extract_tweet_data(html_content,Debug):

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Tweet Content
        tweet_text_div = soup.find('div', {'data-testid': 'tweetText'})
        if tweet_text_div:
            tweet_text = ""
            for child in tweet_text_div.children:
                if child.name == 'span':
                    tweet_text += child.text
                elif child.name == 'img':
                    tweet_text += child['alt']  # Get the alt text of the emoji
        else:
            tweet_text = None

        # Tweet Author
        tweet_author_div = soup.find('div', {'data-testid': 'User-Name'})
        if tweet_author_div:
            tweet_author_link = tweet_author_div.find('a')
            tweet_author_name = tweet_author_link.find('span', class_='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3').text
            author_id = tweet_author_link['href'].split('/')[1]  # Extract ID from the link
        else:
            tweet_author_name = None
            author_id = None

        # Find the div containing the counts using a more robust approach
        counts_div = soup.find('div', {'aria-label': True, 'role': 'group'})

        # Extract the numbers from the aria-label
        replies_count = retweets_count = likes_count = bookmarks_count = None  # Initialize to None
        if counts_div:
            aria_label_text = counts_div['aria-label']
            parts = aria_label_text.split(',')

            for part in parts:
                if 'replies' in part.lower():
                    replies_count = part.split()[0]
                elif 'reposts' in part.lower():
                    retweets_count = part.split()[0]
                elif 'likes' in part.lower():
                    likes_count = part.split()[0]
                elif 'bookmarks' in part.lower():
                    bookmarks_count = part.split()[0]

        # Timestamp
        timestamp_tag = soup.find('time')
        timestamp = timestamp_tag.get('datetime') if timestamp_tag else None

        # Put the extracted data into a dictionary
        tweet_data = {
            'author': tweet_author_name,
            'author_id': author_id,
            'text': tweet_text,
            'replies': replies_count,
            'retweets': retweets_count,
            'likes': likes_count,
            'bookmarks': bookmarks_count,
            'timestamp': timestamp
        }

        return tweet_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

