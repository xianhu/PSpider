# _*_ coding: utf-8 _*_

import spider
import logging
import requests.adapters
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
requests.packages.urllib3.disable_warnings()


class BookFetcher(spider.Fetcher):

    def __init__(self):
        spider.Fetcher.__init__(self, normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=3, critical_sleep_time=0)
        self.driver = webdriver.PhantomJS(service_args=['--load-images=no'])
        self.driver.set_window_size(1120, 2000)
        return

    def clear_session(self):
        self.driver.delete_all_cookies()
        return

    def driver_quit(self):
        self.driver.quit()
        return

    def url_fetch(self, url, keys, critical, fetch_repeat):
        try:
            logging.warning("-------------------------------")
            if keys[0] == "detail":
                logging.warning("fetch %s", url)
                x_str = "//*[@id='detail'][contains(@isloaded, '1')]"
                self.driver.get(url)
                element_present = EC.presence_of_element_located((By.XPATH, x_str))
                WebDriverWait(self.driver, 60).until(element_present)
        except:
            logging.warning("Unexpected error: %s", sys.exc_info()[0])
            #self.clear_session()
            return 0, ""
        response = self.driver.page_source
        if not response:
            logging.warning("not response %s", response)
            return 0, ""
        logging.warning("fetch done!")
        return 1, response
