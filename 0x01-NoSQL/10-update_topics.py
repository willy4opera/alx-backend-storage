#!/usr/bin/env python3
'''Write a Python function that returns the list of school having a specific topic:

    Prototype: def schools_by_topic(mongo_collection, topic):
    mongo_collection will be the pymongo collection object
    topic (string) will be topic searched
'''


def update_topics(mongo_collection, name, topics):
    '''Changes all topics of a collection's document based on the name.
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
