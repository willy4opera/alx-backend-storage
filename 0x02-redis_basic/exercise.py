#!/usr/bin/env python3

'''Redis NoSQL data storage Module: How to.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union

def call_history(method: Callable) -> Callable:
    '''Monitors the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Here, we returns the method's output
        after storing its inputs and output.
        '''
        input_ky = '{}:inputs'.format(method.__qualname__)
        output_ky = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_ky, str(args))
        ch_output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_ky, ch_output)
        return ch_output
    return invoker

def replay(fn: Callable) -> None:
    '''Show the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    input_ky = '{}:inputs'.format(fxn_name)
    output_ky = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(input_ky, 0, -1)
    fxn_outputs = redis_store.lrange(output_ky, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


def count_calls(method: Callable) -> Callable:
    '''Monitors the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Calls the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker

class Cache:
    '''The represention of object in data storage in a Redis.
    '''
    def __init__(self) -> None:
        '''Initializes Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in a Redis data storage and returns the key.
        '''
        data_ky = str(uuid.uuid4())
        self._redis.set(data_ky, data)
        return data_ky

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
    
