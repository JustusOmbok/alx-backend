#!/usr/bin/env python3
""" MRUCache module
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache class inherits from BaseCaching
    """

    def __init__(self):
        """ Initialize MRUCache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using MRU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the most recently used item (MRU algorithm)
                mru_key = self.order.pop(0)
                del self.cache_data[mru_key]
                print("DISCARD:", mru_key)
            self.cache_data[key] = item
            self.order.insert(0, key)

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data:
            # Move the accessed key to the front of the order 
            # to mark it as most recently used
            self.order.remove(key)
            self.order.insert(0, key)
            return self.cache_data[key]
        return None
