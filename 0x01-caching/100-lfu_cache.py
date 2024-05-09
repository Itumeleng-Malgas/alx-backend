#!/usr/bin/env python3
""" BaseCaching module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache (Least Frequently Used) caching system"""

    def __init__(self):
        """Initialize the LFUCache"""
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                self._discard_least_frequent_used()
            self.cache_data[key] = item
            self.frequency[key] = self.frequency.get(key, 0) + 1

    def get(self, key):
        """Get an item by key"""
        if key is not None:
            if key in self.cache_data:
                self.frequency[key] = self.frequency.get(key, 0) + 1
                return self.cache_data[key]
        return None

    def _discard_least_frequent_used(self):
        """Discard the least frequent used item"""
        min_frequency = min(self.frequency.values())
        least_frequent_keys = [key for key, value in self.frequency.items()
                               if value == min_frequency]
        if len(least_frequent_keys) == 1:
            discarded_key = least_frequent_keys[0]
        else:
            # If multiple items have the same frequency, use LRU algorithm to
            # decide which one to discard
            lru_key = min(self.cache_data,
                          key=lambda k: self.frequency.get(k, 0))
            discarded_key = lru_key
        del self.cache_data[discarded_key]
        del self.frequency[discarded_key]
        print("DISCARD:", discarded_key)
