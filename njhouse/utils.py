# coding:utf-8

import re
from typing import Dict
from typing import Optional

from bs4 import BeautifulSoup
from sitepages import page
from xarg import csv


class njhouse_page():
    def __init__(self, url: str):
        self.__page: page = page(url=url)
        self.__cache: Optional[str] = None

    @property
    def page(self) -> page:
        return self.__page

    @property
    def cache(self) -> str:
        if self.__cache is None:
            self.__cache = self.fetch()
        return self.__cache

    def fetch(self) -> str:
        return self.page.fetch()


class njhouse_soup(njhouse_page):
    def __init__(self, url: str):
        self.__soup: Optional[BeautifulSoup] = None
        super().__init__(url=url)

    @property
    def soup(self) -> BeautifulSoup:
        if self.__soup is None:
            self.__soup = BeautifulSoup(self.cache, "html.parser")
        return self.__soup


class njhouse_project(njhouse_soup):
    """商品房
    """

    def __init__(self, url: str = "https://www.njhouse.com.cn/projectindex.html"):  # noqa:E501
        super().__init__(url=url)

    @property
    def subscriptions(self) -> int:
        """认购套数
        """
        match = self.soup.find("div", class_="busniess_num_word")
        return int(match.get_text(strip=True)) if match else 0

    @property
    def transactions(self) -> int:
        """成交套数
        """
        match = self.soup.find("div", class_="busniess_num_word green")
        return int(match.get_text(strip=True)) if match else 0

    @property
    def sales(self) -> int:
        """销售 = 认购 + 成交
        """
        return self.subscriptions + self.transactions


class njhouse_stock(njhouse_page):
    """存量房
    """

    def __init__(self, url: str = "http://njzl.njhouse.com.cn/stock"):
        super().__init__(url=url)

    @property
    def total_listings(self) -> int:
        """总挂牌房源
        """
        match = re.search(r"(总挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def intermediary_listings(self) -> int:
        """中介挂牌房源
        """
        match = re.search(r"(中介挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def personal_listings(self) -> int:
        """个人挂牌房源
        """
        match = re.search(r"(个人挂牌房源：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0

    @property
    def yesterday_tradings(self) -> int:
        """昨日住宅成交量
        """
        match = re.search(r"(昨日住宅成交量：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0


class njhouse_rent(njhouse_page):
    """租赁房
    """

    def __init__(self, url: str = "http://njzl.njhouse.com.cn/rent"):
        super().__init__(url=url)

    @property
    def listings(self) -> int:
        """挂牌量
        """
        match = re.search(r"(挂牌量：)\s*(\d+)", self.cache)
        return int(match.group(2)) if match else 0


class njhouse_query():
    def __init__(self):
        self.__project = njhouse_project()
        self.__stock = njhouse_stock()
        self.__rent = njhouse_rent()

    @property
    def project(self) -> njhouse_project:
        return self.__project

    @property
    def stock(self) -> njhouse_stock:
        return self.__stock

    @property
    def rent(self) -> njhouse_rent:
        return self.__rent

    def dict_project(self) -> Dict[str, int]:
        return {
            "认购": self.project.subscriptions,
            "成交": self.project.transactions,
        }

    def dict_stock(self) -> Dict[str, int]:
        return {
            "总挂牌房源": self.stock.total_listings,
            "中介挂牌房源": self.stock.intermediary_listings,
            "个人挂牌房源": self.stock.personal_listings,
            "昨日住宅成交量": self.stock.yesterday_tradings,
        }

    def dict_rent(self) -> Dict[str, int]:
        return {
            "挂牌量": self.rent.listings,
        }

    def dict_all(self) -> Dict[str, Dict[str, int]]:
        return {
            "商品房": self.dict_project(),
            "存量房": self.dict_stock(),
            "租赁房": self.dict_rent(),
        }


class njhouse_store(njhouse_query):
    def __init__(self, directory: str):
        self.__directory: str = directory
        super().__init__()

    @property
    def directory(self) -> str:
        return self.__directory

    def save(self):
        self.dict_all()
