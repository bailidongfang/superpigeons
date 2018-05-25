from django.core.paginator import Paginator
from django.utils import six


class NewPaginator(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, range_num=2, page_num=0):
        Paginator.__init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True)
        self.range_num = range_num
        self.page_num = page_num

    def page(self, number):
        self.page_num = number
        return super(NewPaginator, self).page(number)

    def get_page_range(self):
        first = int(self.page_num) - int(self.range_num)
        end = first + int(self.range_num)*2 + 1
        if first < 1:
            first = 1
            end = first + int(self.range_num) * 2 + 1
        if end > int(self.num_pages) + 1:
            end = int(self.num_pages) + 1
            first = end - int(self.range_num) * 2 - 1
            if first < 1:
                first = 1
        return six.moves.range(first, end)
