from math import ceil

'''
    Pagination.py
    author: Tao Liu and Xi Chen
    The pagination class that handles the pagination display on the search_page.html
'''

class Pagination(object):
    def __init__(self, page, per_page, total_count):
        """
        Intiate a pagination object 
        :param page: the current page
               per_page: number of movies per page  
               total_count: total number of movies
        """
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        """
        Get the total number of pages
        :return the total number of pages
        """
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        """
        Check whether the current page has a previous page
        :return return true if the current page has a previous page, vice versa
        """
        return self.page > 1

    @property
    def has_next(self):
        """
        Check whether the current page has a next page
        :return return true if the current page has a next page, vice versa
        """
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """
        Iterates through the pages that can be shown on the webpage
        :para left_edge: the number of first several pages that will be shown on any page
              right_edge: the number of last several pages that will be shown on any page
              right_current: the number of pages after the current page that will be shown
              left_current: the number of pages before the current page that will be shown
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num