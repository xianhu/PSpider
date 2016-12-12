# _*_ coding: utf-8 _*_

import random
import string
import spider
import logging
import requests
import requests.adapters
requests.packages.urllib3.disable_warnings()


class MovieFetcher(spider.Fetcher):

    def __init__(self):
        spider.Fetcher.__init__(self, max_repeat=3, sleep_time=0)

        self.session = requests.Session()
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))
        self.clear_session()
        return

    def clear_session(self):
        self.session.headers.clear()
        self.session.cookies.clear()
        self.session.headers = {
            "User-Agent": spider.make_random_useragent("pc"),
            "Host": "movie.douban.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN, zh; q=0.8, en; q=0.6",
            "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
        }
        return

    def url_fetch(self, url, keys, repeat):
        resp = self.session.get(url, allow_redirects=False, verify=False, timeout=5)
        if resp.status_code == 200:
            return 1, resp.text
        logging.warning("Fetcher change cookie: %s", resp.status_code)
        self.clear_session()
        resp.raise_for_status()
        return 1, resp.text
