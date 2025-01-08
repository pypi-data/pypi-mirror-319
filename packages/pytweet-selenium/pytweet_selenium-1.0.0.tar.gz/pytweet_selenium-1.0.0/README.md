# PyTweet - Selenium

PyTweet Selenium is a simple Python package to extract tweet content from a given URL. Built on selenium.

---


## Installation

To install PyTweet, use:
```bash
pip install pytweetselenium
```

## Usage

Here's how you can use PyTweet to fetch tweet content:

```python

import pytweetselenium

url = "https://x.com/AlexanderJiazx/status/1876874066319049004"
result = pytweetselenium.get(url)
print(result)

```

### Output Example

The `pytweetselenium.get()` function returns a dictionary containing key information about the tweet:

```python
{
    'author': 'Alexander Jia',
    'author_id': 'AlexanderJiazx',
    'text': 'Got the access of AVM with vision!\nTell me how do you want to test it.',
    'replies': '7',
    'retweets': '3',
    'likes': '57',
    'bookmarks': '8',
    'timestamp': '2024-12-12T23:26:11.000Z'
}
```

## Functions
- Extracts tweet content, including author details, tweet text, engagement metrics (replies, retweets, likes, bookmarks), and timestamp.
- Extraction support text only, image support coming soon.


## License
This project is licensed under the MIT License. See the LICENSE file for details.

---
