#!/usr/bin/python3
""" BaseCaching module: MRU (Most Recently Used) caching system
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRU caching system
    """

    def __init__(self):
        """ Initialize MRUCache """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                discarded_key = self.queue.pop()
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)
            self.cache_data[key] = item

            if key in self.queue:
                self.queue.remove(key)
            self.queue.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data.keys():
            if key in self.queue:
                self.queue.remove(key)
            self.queue.append(key)
            return self.cache_data[key]
        return None
