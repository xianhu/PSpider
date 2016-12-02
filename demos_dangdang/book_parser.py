# _*_ coding: utf-8 _*_

import spider
import re
import urllib
import logging
from bs4 import BeautifulSoup


class BookParser(spider.Parser):

    def __init__(self):
        spider.Parser.__init__(self)
        self.contents_need = ['isbn', 'pic', 'title', 'con_reco', 'comment', 'brand', 'series', 'author', 'author_origin', 'author_country', 'translator', 'publicator', 'author_prize', 'book_prize', 'raw_title', 'age', 'responsibility', 'lan', 'words', 'size', 'binding', 'pub_date', 'pub_times', 'pages', 'price', 'editor_reco', 'media_reco', 'author_intro', 'review_num', 'dangdang_rank']

    def clean_str(self, in_str):
        clean = re.compile('<.*?>')
        clean_text = re.sub(clean, '', in_str)
        return clean_text

    def getdetail_descripe(self, soup):
        p_info = soup.find(id="detail_describe")
        series = ""
        isbn = ""
        pub_times = ""
        pages = ""
        words = ""
        pub_date = ""
        size = ""
        binding = ""
        if p_info:
            li_list = p_info.findAll("li")
            if li_list:
                try:
                    for item in li_list:
                        item_str = str(item.get_text().strip())
                        if item_str.find("版 次") > -1:
                            pub_times = item_str.replace("版 次：", "")
                            continue
                        if item_str.find("页 数") > -1:
                            pages = item_str.replace("页 数：", "")
                            continue
                        if item_str.find("字 数") > -1:
                            words = item_str.replace("字 数：", "")
                            continue
                        if item_str.find("印刷时间") > -1:
                            pub_date = item_str.replace("印刷时间：", "")
                            continue
                        if item_str.find("开 本") > -1:
                            size = item_str.replace("开 本：", "")
                            continue
                        if item_str.find("包 装") > -1:
                            binding = item_str.replace("包 装：", "")
                            continue
                        if item_str.find("国际标准书号ISBN") > -1:
                            isbn = item_str.replace("国际标准书号ISBN：", "")
                            continue
                        if item_str.find("丛书名") > -1:
                            series = item_str.replace("丛书名：", "")
                    # print [series, isbn, pub_times, pages, words, pub_date, size, binding]
                    return [series, isbn, pub_times, pages, words, pub_date, size, binding]
                except:
                    pass
                    return ["", "", "", "", "", "", "", ""]
            return ["", "", "", "", "", "", "", ""]
        else:
            return ["", "", "", "", "", "", "", ""]

    def get_title(self, soup):
        name_tag = soup.find("div", class_="name_info")
        if name_tag:
            title_tag = name_tag.find("h1")
            if title_tag:
                try:
                    title = title_tag.get_text().strip()
                    return str(title)
                except:
                    return ""
            else:
                return ""
        else:
            return ""

    def get_comment(self, soup):
        name_tag = soup.find("div", class_="name_info")
        if name_tag:
            content_tag = name_tag.find("h2")
            if content_tag:
                try:
                    content = content_tag.get_text().strip()
                    return str(content)
                except:
                    return ""
            else:
                return ""
        else:
            return ""

    def get_content(self, soup):
        content_tag = soup.find(id="content")
        if content_tag:
            dsc_tag = content_tag.find(id="content-textarea")
            if not dsc_tag:
                dsc_tag = content_tag.find("div", class_="descrip")
            try:
                content = dsc_tag.get_text().strip()
                return self.clean_str(str(content))
            except:
                return ""
        else:
            return ""

    def get_country(self, soup):
        name_tag = soup.find(id="author")
        name = ""
        if name_tag:
            name = str(name_tag.get_text()).strip().replace("作者:", "")
        pattern1 = re.compile(r'.*\【(.+?)\】.*')
        pattern2 = re.compile(r'.*\[(.+?)\].*')
        pattern3 = re.compile(r'.*\（(.+?)\）.*')
        pattern_list = [pattern1, pattern2, pattern3]
        for pattern in pattern_list:
            match = pattern.match(name)
            if match:
                return match.group(1)
        return ""

    def get_author_and_trans(self, soup):
        name_tag = soup.find(id="author")
        author = ""
        trans = ""
        previous = ""
        if name_tag:
            for item_l in name_tag.contents:
                if type(item_l).__name__ == "NavigableString":
                    content = str(item_l.string).strip()
                    if content.find("译") > -1:
                        if content.find("编译") > -1:
                            content.replace("编译", "")
                        else:
                            content.replace("译", "")
                        trans = previous
                        previous = ""
                    else:
                        if content.find("作者") > -1:
                            previous = previous + content.replace("作者:", "")
                        else:
                            if content and content != "，":
                                author = author + previous + content
                                previous = ""
                            else:
                                previous = previous + " " + content
                else:
                    content = str(item_l.get_text()).strip()
                    previous = previous + content
            author = author + previous
            return [author, trans]
        else:
            return ["", ""]

    def get_publicator(self, soup):
        pub_tag = soup.find("span", {"dd_name": "出版社"})
        if pub_tag:
            pub_a = pub_tag.find("a")
            if pub_a:
                return str(pub_a.get_text()).strip()
            return ""
        else:
            return ""

    def get_price(self, soup):
        o_price_tag = soup.find(id="original-price")
        if o_price_tag:
            return str(o_price_tag.get_text()).strip()
        price_tag = soup.find(id="dd-price")
        if price_tag:
            return str(price_tag.get_text()).strip()
        else:
            return ""

    def get_editor_reco(self, soup):
        abstract_tag = soup.find(id="abstract")
        editor_reco = ""
        if abstract_tag:
            reco_tag = abstract_tag.find(id="abstract-all")
            if reco_tag:
                editor_reco = str(reco_tag.get_text()).strip()
            if not editor_reco:
                dis_tag = abstract_tag.find("div", class_="descrip")
                if dis_tag:
                    editor_reco = str(dis_tag.get_text()).strip()
        return editor_reco

    def get_media_reco(self, soup):
        content_tag = soup.find(id="mediaFeedback")
        if content_tag:
            media_tag = content_tag.find(id="mediaFeedback-textarea")
            if not media_tag:
                media_tag = content_tag.find("div", class_="descrip")
            try:
                content = media_tag.get_text().strip()
                return self.clean_str(str(content))
            except:
                return ""
        else:
            return ""

    def get_author_intro(self, soup):
        content_tag = soup.find(id="authorIntroduction")
        if content_tag:
            media_tag = content_tag.find(id="authorIntroduction-textarea")
            if not media_tag:
                media_tag = content_tag.find("div", class_="descrip")
            try:
                content = media_tag.get_text().strip()
                return self.clean_str(str(content))
            except:
                return ""
        else:
            return ""

    def get_reviws_number(self, soup):
        num_tag = soup.find(id="comm_num_down")
        if num_tag:
            return str(num_tag.get_text()).strip()
        else:
            return ""

    def get_rank(self, soup):
        rank_tag = soup.find("span", {"dd_name": "图书排行榜排名"})
        if rank_tag:
            return str(rank_tag.get_text()).strip()
        else:
            return ""

    def get_pic(self, soup, lines_map):
        lines_map[self.contents_need[1]] = "miss"
        img_tag = soup.find(id="main-img-slider")
        img_url = []
        if img_tag:
            img_lists = img_tag.findAll("a")
            if img_lists:
                for img_li in img_lists:
                    if str(img_li["data-imghref"]) not in img_url:
                        img_url.append(str(img_li["data-imghref"]))
        lines_map[self.contents_need[1]] = ','.join(img_url)


    def init_map(self):
        lines_map = {}
        c_len = len(self.contents_need)
        for i in range(0, c_len):
            lines_map[self.contents_need[i]] = ''
        # lines_map['age'] = age[option]
        return lines_map

    def write_to_line(self, lines_map):
        line = []
        c_len = len(self.contents_need)
        for i in range(0, c_len):
            line.append(lines_map[self.contents_need[i]])
        return line

    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        url_list, save_list = [], []
        soup = BeautifulSoup(content, "lxml")
        if keys[0] == "lists":
            ul_tag = soup.find("ul", class_="list_aa listimg")
            if not ul_tag:
                return 1, url_list, save_list
            lists_tag = ul_tag.findAll("a", class_="pic")
            if not lists_tag:
                return 1, url_list, save_list
            for link in lists_tag:
                save_list.append([str(link["href"]), str(link["title"])])
        elif keys[0] == "detail":
            lines_map = self.init_map()
            [series, isbn, pub_times, pages, words, pub_date, size, binding] = self.getdetail_descripe(soup)
            lines_map[self.contents_need[6]] = series
            lines_map[self.contents_need[0]] = isbn
            lines_map[self.contents_need[22]] = pub_times
            lines_map[self.contents_need[23]] = pages
            lines_map[self.contents_need[18]] = words
            lines_map[self.contents_need[21]] = pub_date
            lines_map[self.contents_need[19]] = size
            lines_map[self.contents_need[20]] = binding
            lines_map[self.contents_need[2]] = self.get_title(soup)
            lines_map[self.contents_need[3]] = self.get_content(soup)
            lines_map[self.contents_need[4]] = self.get_comment(soup)
            [author, translator] = self.get_author_and_trans(soup)
            lines_map[self.contents_need[7]] = author
            lines_map[self.contents_need[10]] = translator
            lines_map[self.contents_need[9]] = self.get_country(soup)
            lines_map[self.contents_need[11]] = self.get_publicator(soup)
            lines_map[self.contents_need[24]] = self.get_price(soup)
            lines_map[self.contents_need[25]] = self.get_editor_reco(soup)
            lines_map[self.contents_need[26]] = self.get_media_reco(soup)
            lines_map[self.contents_need[27]] = self.get_author_intro(soup)
            lines_map[self.contents_need[28]] = self.get_reviws_number(soup)
            lines_map[self.contents_need[29]] = self.get_rank(soup)
            self.get_pic(soup, lines_map)
            item = self.write_to_line(lines_map)
            item.append(url)
            #logging.warning(item)
            save_list.append(item)
        return 1, url_list, save_list
