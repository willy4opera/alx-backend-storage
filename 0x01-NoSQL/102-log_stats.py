#!/usr/bin/env python3
'''Task Log stats - new version.
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''Show Nginx request logs Statistics.
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        reuest_cnt = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, reuest_cnt))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def print_top_ips(server_collection):
    '''Show statistics of the top 10 HTTP IPs in a collection.
    '''
    print('IPs:')
    request_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


def run():
    '''Show some stats about Nginx logs stored in MongoDB.
    '''
    node = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(node.logs.nginx)
    print_top_ips(node.logs.nginx)


if __name__ == '__main__':
    run()
