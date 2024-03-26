#!/usr/bin/env python3

'''Task  Log stats .
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Prints Nginx request logs statistics.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def run():
    '''Show stats about Nginx logs stored in the MongoDB.
    '''
    node = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(node.logs.nginx)


if __name__ == '__main__':
    run()
