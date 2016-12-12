# _*_ coding: utf-8 _*_

"""
test_demos.py by xianhu
"""

import re
import spider
import pymysql
import logging
import requests
from bs4 import BeautifulSoup
from demos_doubanmovies import MovieFetcher, MovieParser
from demos_dangdang import BookFetcher, BookParser, BookSaver


def get_douban_movies():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
        "Host": "movie.douban.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "bid=Pd48iLTpsf8"
    }

    # 获取初始url
    all_urls = set()

    resp = requests.get("https://movie.douban.com/tag/", headers=headers, verify=False)
    assert resp.status_code == 200, resp.status_code

    soup = BeautifulSoup(resp.text, "html5lib")
    a_list = soup.find_all("a", href=re.compile(r"^/tag/", flags=re.IGNORECASE))
    all_urls.update([(a_soup.get_text(), "https://movie.douban.com" + a_soup.get("href")) for a_soup in a_list])

    resp = requests.get("https://movie.douban.com/tag/?view=cloud", headers=headers, verify=False)
    assert resp.status_code == 200, resp.status_code

    soup = BeautifulSoup(resp.text, "html5lib")
    a_list = soup.find_all("a", href=re.compile(r"^/tag/", flags=re.IGNORECASE))
    all_urls.update([(a_soup.get_text(), "https://movie.douban.com" + a_soup.get("href")) for a_soup in a_list])
    logging.warning("all urls: %s", len(all_urls))

    # 构造爬虫
    dou_spider = spider.WebSpider(MovieFetcher(), MovieParser(max_deep=-1), spider.Saver(), spider.UrlFilter())
    for tag, url in all_urls:
        dou_spider.set_start_url(url, ("index", tag), priority=1)
    dou_spider.start_work_and_wait_done(fetcher_num=20)
    return


def get_dangdang_books():
    fetcher_number = 10
    fetcher_list = []
    for i in range(fetcher_number):
        fetcher_list.append(BookFetcher())
    parser = BookParser()
    saver = BookSaver()
    dang_spider = spider.WebSpider(fetcher_list, parser, saver, None)

    # 获取所有链接并存入数据库,由于时间太长,因此抓取链接和信息分开进行
    url_prefix_list = ["http://category.dangdang.com/pg{}-cp01.41.43.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.19.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.20.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.22.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.21.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.12.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.17.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.02.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.05.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.05.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.05.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.05.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.05.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.19.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.26.17.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.02.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.27.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.41.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.41.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.41.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.50.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.50.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.50.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.16.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.21.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.19.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.01.14.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.45.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.44.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.17.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.46.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.51.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.47.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.13.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.17.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.15.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.37.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.25.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.23.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.45.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.27.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.43.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.39.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.21.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.09.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.55.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.19.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.29.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.29.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.53.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.11.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.33.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.31.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.35.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.57.41.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.03.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.01.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.07.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.02.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.04.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.05.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.48.06.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.55.00.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.69.00.00.00.html",
                       "http://category.dangdang.com/pg{}-cp01.41.59.00.00.00.html"]

    for url_prefix in url_prefix_list:
        for i in range(100):
            url = url_prefix.format(i)
            dang_spider.set_start_url(url, ("lists",), priority=1)
    dang_spider.start_work_and_wait_done(fetcher_num=fetcher_number)

    # 开始抓取所有的详细信息
    dang_spider = spider.WebSpider(fetcher_list, parser, saver, None)
    conn = pymysql.connect(host="localhost", user="username", password="password", db="dangdang_book", charset="utf8")
    cursor = conn.cursor()
    conn.autocommit(1)
    cursor.execute("select url from book_urls;")
    url_list = [item[0] for item in cursor.fetchall()]

    for url in url_list:
        dang_spider.set_start_url(url, ("detail",), priority=1)

    dang_spider.start_work_and_wait_done(fetcher_num=fetcher_number)
    for f_er in fetcher_list:
        f_er.driver_quit()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    get_douban_movies()
