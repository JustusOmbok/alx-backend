#!/usr/bin/env python3
"""
Simple helper function for pagination.
"""


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

    return start_index, end_index
