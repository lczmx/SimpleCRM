"""
此模块可将数据分页并产生分页标签
"""

__author__ = "lczmx"

import re

class Pagination():
    def __init__(self, totalCount, currentPage, perPageItemNum=10, maxPageNum=11):
        """
        :param totlaCount: 数据长度
        :param currentPage: 当前页
        :param perPageItemNum: 每一页显示数据条数
        :param maxPageNum: 页码个数
        """

        self.totalCount = totalCount
        self.perPageItemNum = perPageItemNum
        self.maxPageNum = maxPageNum
        try:
            self.currentPage = int(currentPage)
            if self.currentPage <= 0:
                self.currentPage = 1
            elif self.currentPage > self.num_pages:
                self.currentPage = self.num_pages
        except:
            self.currentPage = 1

    @property
    def start(self):
        return (self.currentPage - 1) * self.perPageItemNum if self.totalCount else 0

    @property
    def end(self):
        return self.currentPage * self.perPageItemNum if self.totalCount else self.totalCount + 1

    @property
    def num_pages(self):
        # 总页码
        num_Mod, num_Rem = divmod(self.totalCount, self.perPageItemNum)
        # 为空数据时
        if num_Rem == 0:
            return num_Mod
        return num_Mod + 1

    def page_num_range(self):
        # 生成页码
        part = int(self.maxPageNum / 2)
        if self.maxPageNum > self.num_pages:
            return range(1, self.num_pages + 1)
        if self.currentPage <= part:
            return range(1, self.maxPageNum + 1)
        if self.currentPage + part > self.num_pages:
            return range(self.num_pages - self.maxPageNum + 1, self.num_pages + 1)
        return range(self.currentPage - part, self.currentPage + part + 1)

    def page_str(self, targetUrl="?", otherParameters=False, javaScriptMode=False, ):
        """
        生成分页标签
        targetUrl：要跳转的URL绝对路径
        otherParameters:是否有其他的get参数保留
        :return: HTML
        """

        # 为空数据时
        if self.num_pages == 0:
            return ''

        targetUrl = self.initTargetUrl(targetUrl, otherParameters, javaScriptMode)

        pages_list = []

        if javaScriptMode:
            self.setUpJs(targetUrl, pages_list)
        else:
            # 正常a标签
            self.setUp_Normal_Label(targetUrl, pages_list)

        pages_list_str = ''.join(pages_list)
        pages_list_str.replace("//", "/")
        return pages_list_str

    def initTargetUrl(self, targetUrl, otherParameters, javaScriptMode):
        """"
        初始化字符串，将字符串的不合法成分替换 或 直接报错
        """
        if otherParameters and not targetUrl.startswith("?"):
            raise ValueError("otherParameters 已开启,其输入如下格式\n:'?a=1")
        if javaScriptMode and not targetUrl.startswith("javascript:"):
            raise ValueError("javaScriptMode已开启,其输入如下格式\n:'javascript:void(0);'")

        if not javaScriptMode:
            targetUrl = re.sub(r"_page=\w*", '',targetUrl)
            # 兼容url的其他其他get参数,必须在已经有其参数时使用，否则自动拼接
            targetUrl = targetUrl + "&" if not targetUrl.__eq__("?") and otherParameters else "?"
        return targetUrl

    def setUpJs(self, targetUrl, pages_list):
        # javascript 标签   以to-pager属性获取转跳的页码
        if self.currentPage == 1:
            pass
        else:
            first = "<li><a to-pager='1' class='first-page'href='%s'>首页</a></li>" % targetUrl
            pages_list.append(first)
            perv_page = "<li class='perv-page'><a to-pager='%s'href='%s'>上一页</a></li>" % (
                (self.currentPage - 1), targetUrl)
            pages_list.append(perv_page)

        for i in self.page_num_range():
            if self.currentPage == i:
                tmp = "<li class='active'><a to-pager='%s' href='%s'>%s</a></li>" % (i, targetUrl, i)
            else:
                tmp = "<li><a to-pager='%s' href='%s'>%s</a></li>" % (i, targetUrl, i)
            pages_list.append(tmp)
        if self.currentPage == self.num_pages:
            pass
        else:
            next_page = "<li class='next-page'><a to-pager='%s' href='%s'>下一页</a></li>" % (
                self.currentPage + 1, targetUrl)
            pages_list.append(next_page)
            last = "<li class='last-page'><a to-pager='%s' href='%s'>尾页</a></li>" % (self.num_pages, targetUrl)
            pages_list.append(last)

    def setUp_Normal_Label(self, targetUrl, pages_list):
        if self.currentPage == 1:
            pass
        else:
            first = "<li><a class='first-page'href='%s_page=1'>首页</a></li>" % targetUrl
            pages_list.append(first)
            perv_page = "<li class='perv-page'><a href='%s_page=%s'>上一页</a></li>" % (
                targetUrl, (self.currentPage - 1))
            pages_list.append(perv_page)

        for i in self.page_num_range():
            if self.currentPage == i:
                tmp = "<li class='active'><a href='%s_page=%s'>%s</a></li>" % (targetUrl, i, i)
            else:
                tmp = "<li><a href='%s_page=%s'>%s</a></li>" % (targetUrl, i, i)
            pages_list.append(tmp)
        if self.currentPage == self.num_pages:
            pass
        else:
            next_page = "<li class='next-page'><a href='%s_page=%s'>下一页</a></li>" % (
                targetUrl, self.currentPage + 1)
            pages_list.append(next_page)
            last = "<li class='last-page'><a href='%s_page=%s'>尾页</a></li>" % (targetUrl, self.num_pages)
            pages_list.append(last)
