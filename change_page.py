from math import *


# turn page util
class Paginator(object):

    def __init__(self, total_records=None, page_size=None):
        # total records
        self.total_records = total_records
        # peerage size
        self.page_size = page_size
        # total pages
        self.total_pages = 0
        # peerage skip inform 每一页要跳过的数据体量
        self.data = {}
        self.__judge__()

    # 计算页数及每一页的具体情况
    def __judge__(self):
        # calculate total pages
        if self.total_records > self.page_size:
            # floor() 返回数字的下舍整数。整体数据除以每页的数据 得到总页数 注意少一页
            self.total_pages = int(floor(self.total_records / float(self.page_size)))
            # the first page skip inform 第一页
            self.data[1] = Page(self, page_number=1, skip=0)
            # from the second page应该是从第二页开始 跳过的内容为字典里规定的前一项要跳过的数量加上前一页的整体尺寸
            for i in range(1, self.total_pages):
                self.data[i + 1] = Page(self, page_number=i + 1, skip=self.data[i].skip + self.page_size)

            # 如果计算出来的页数不恰巧是个整数，那么还需要计算最后一页
            if self.total_pages:
                # 计算最后一页,因为最后一页肯定是能全页显示的
                self.data[self.total_pages + 1] = Page(self, self.total_pages + 1,
                                                       skip=self.data[self.total_pages].skip + self.page_size)

        else:
            self.total_pages = 1
            self.data[1] = Page(self, 1, skip=0)

    # 获取页数 choose the page which you want
    def get_page(self, page_number):
        page_number = int(page_number)
        if page_number in self.data.keys():
            return self.data[page_number]
        else:
            return None


# page
class Page(object):

    def __init__(self, paginator, page_number=1, skip=0):
        self.page_number = page_number
        self.skip = skip
        self.paginator = paginator
        self.next_page_number = self.page_number + 1
        self.prev_page_number = self.page_number - 1

    # def has_next(self):
    #     return self.page_number

    def has_next(self):
        return self.page_number

    def has_prev(self):
        return self.page_number > 1

    def get_next_page(self):
        return self.paginator.get_page(self.next_page_number)

    def get_prev_page(self):
        return self.paginator.get_page(self.prev_page_number)
