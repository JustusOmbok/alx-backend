#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class inherits from BaseCaching
    """

    def __init__(self):
        """ Initialize LFUCache
        """
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """ Add an item in the cache using LFU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard the least frequency used item (LFU algorithm)
                min_freq = min(self.frequency.values())
                least_frequent_keys = [
                    k for k, v in self.frequency.items() if v == min_freq
                    ]

                if len(least_frequent_keys) > 1:
                    # Use LRU algorithm to discard the least recently used
                    # among the least frequent
                    lru_key = (
                        min(least_frequent_keys,
                            key=lambda k: self.cache_data[k]['access_count'])
                            )
                else:
                    lru_key = least_frequent_keys[0]

                del self.cache_data[lru_key]
                del self.frequency[lru_key]
                print("DISCARD:", lru_key)

            self.cache_data[key] = {'item': item, 'access_count': 0}
            self.frequency[key] = 0

    def get(self, key):
        """ Get an item by key
        """
        if key is not None and key in self.cache_data:
            # Increment access count and update frequency
            self.cache_data[key]['access_count'] += 1
            self.frequency[key] += 1
            return self.cache_data[key]['item']
        return None

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key, value in self.cache_data.items():
            print("{}: {}".format(key, value['item']))
