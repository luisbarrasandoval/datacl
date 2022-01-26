import requests_cache
from bs4 import BeautifulSoup
from datetime import timedelta
import json


def Session(x_requests=None):
    browser = requests_cache.CachedSession(
        '.cache',
        use_cache_dir=True,                # Save files in the default user cache dir
        # Use Cache-Control headers for expiration, if available
        cache_control=True,
        # Otherwise expire responses after seven day
        expire_after=timedelta(days=7),
        # Cache POST requests to avoid sending the same data twice
        allowable_methods=['GET', 'POST'],
        # Cache 400 responses as a solemn reminder of your failures
        allowable_codes=[200, 400],
        match_headers=True,                # Match all request headers
        # In case of request errors, use stale cache data if possible
        stale_if_error=True,
    )

    browser.headers.update({
        "user-agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
        "connection": "keep-alive",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "x-requested-with": x_requests
    })

    if x_requests == None:
        browser.headers.pop("x-requested-with")

    return browser
