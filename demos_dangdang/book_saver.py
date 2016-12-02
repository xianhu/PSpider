# _*_ coding: utf-8 _*_

import spider
import pymysql


class BookSaver(spider.Saver):

    def __init__(self):
        spider.Saver.__init__(self)
        self.conn = pymysql.connect(host="localhost", user="username", password="password", db="dangdang_book", charset="utf8")
        self.cursor = self.conn.cursor()
        self.conn.autocommit(1)
        return

    def item_save(self, url, keys, item):
        '''
        self.cursor.execute("insert into t_doubanmovies (m_url, m_name, m_year, m_imgurl, m_director, m_writer, m_actors, "
                            "m_genre, m_country, m_language, m_release, m_season, m_jishu, m_length, m_alias, m_website, m_dbsite, "
                            "m_imdb, m_score, m_comment, m_starpercent)"
                            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                            [i.strip() if i is not None else "" for i in item])
        '''
        if keys[0] == "lists":
            self.cursor.execute("insert into book_urls (url, title) values(%s, %s);", [i.strip() if i is not None else "" for i in item])
        elif keys[0] == "detail":

            self.cursor.execute(
                "insert into book_detail (isbn, pic, title, con_reco, comment, brand, series, "
                "author, author_origin, author_country, translator, publicator, author_prize, book_prize, raw_title, age, responsibility, "
                "lan, words, size, binding, pub_date, pub_times, pages, price, editor_reco, media_reco, author_intro, review_num, dangdang_rank, link)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                [i.strip() if i is not None else "" for i in item])

        return True
