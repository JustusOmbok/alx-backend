#!/usr/bin/env python3
"""
Hypermedia pagination functionality for a dataset of popular baby names.
"""

import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    Returns a tuple of start index
    and end index for a given page and page size.

    Args:
        page (int): Page number (1-indexed).
        page_size (int): Number of items per page.

    Returns:
        tuple: Start index and end index.
    """
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size must be greater than 0.")

    start_index = (page - 1) * page_size
    end_index = page * page_size

    return start_index, end_index  # Adjust end index to be inclusive


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns a specific page of the dataset based on pagination parameters.

        Args:
            page (int): Page number (1-indexed).
            page_size (int): Number of items per page.

        Returns:
            List[List]: Page of the dataset.
        """
        assert isinstance(page, int) and isinstance(page_size, int), "int."
        assert page > 0 and page_size > 0, "must be greater than 0."

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:min(end_index + 1, len(dataset))]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Returns a dictionary containing hypermedia pagination information.

        Args:
            page (int): Page number (1-indexed).
            page_size (int): Number of items per page.

        Returns:
            dict: Hypermedia pagination information.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
