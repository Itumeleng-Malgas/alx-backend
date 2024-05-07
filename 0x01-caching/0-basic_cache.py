#!/usr/bin/env python3
"""
Create a class BasicCache that inherits from BaseCaching
and is a caching system:
"""

BaseCaching = __import__('base_caching.py').BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class inherits from BaseCaching and is a caching system"""
    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key is not None:
            return self.cache_data.get(key)