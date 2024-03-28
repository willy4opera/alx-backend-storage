#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


r_store = redis.Redis()
'''The redis store object.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        r_store.incr(f'count:{url}')
        res = r_store.get(f'result:{url}')
        if res:
            return res.decode('utf-8')
        res = method(url)
        r_store.set(f'count:{url}', 0)
        r_store.setex(f'result:{url}', 10, res)
        return res
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
