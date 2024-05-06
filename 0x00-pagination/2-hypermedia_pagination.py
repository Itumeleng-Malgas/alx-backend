#!/usr/bin/env python3
"""
Simple pagination
"""
import csv
from typing import List, Tuple, Dict
import math


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """
        The function should return a tuple of size two containing a start index
        and an end index corresponding to the range of indexes to return in a
        list for those particular pagination parameters.
        """
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        return start_index, end_index

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
        Takes two integer arguments page with default value 1 and page_size
        with default value 10.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        if page < 1 or page_size < 1:
            return []

        start, end = self.index_range(page, page_size)
        if start >= len(self.dataset()):
            return []

        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Returns a dictionary containing hyperlinked pagination information.
        """
        page_data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)

        return {
            "page_size": len(page_data),
            "page": page,
            "data": page_data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
