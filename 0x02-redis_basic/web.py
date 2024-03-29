#!/usr/bin/env python3
"""
Here, we Implements an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
r_store = redis.Redis()


def link_count(method: Callable) -> Callable:
    """Monitors the number of url access to server"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        r_store.incr(f"count:{url}")
        cached = r_store.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        r_store.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@link_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
