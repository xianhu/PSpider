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
from demos_doubanmovies import MovieFetcher, MovieParser, MovieSaver


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

    # 查询已有数据
    conn = pymysql.connect(host="59.110.49.40", user="root", password="mimaMIMA123456", db="db_my", charset="utf8")
    cursor = conn.cursor()
    cursor.execute("select m_url from t_doubanmovies;")

    bloomfilter = spider.UrlFilter()
    bloomfilter.update([item[0] for item in cursor.fetchall()])
    logging.warning("update bloomfilter success: %s", cursor.rowcount)

    cursor.close()
    conn.close()

    # 构造爬虫
    dou_spider = spider.WebSpider(MovieFetcher(), MovieParser(max_deep=-1, max_repeat=1), MovieSaver(), bloomfilter)
    for tag, url in all_urls:
        dou_spider.set_start_url(url, ("index", tag), priority=1, critical=True)
    dou_spider.start_work_and_wait_done(fetcher_num=20)
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    get_douban_movies()
