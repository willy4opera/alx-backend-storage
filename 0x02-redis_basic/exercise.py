#!/usr/bin/env python3

'''Redis NoSQL data storage Module: How to.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union

class Cache:
    '''The represention of object in data storage in a Redis.
    '''
    def __init__(self) -> None:
        '''Initializes Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Fetches a value from the Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Fetches a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Fetches an integer value from a Redis data storage.
        '''
        return self.get(key, lambda x: int(x))
