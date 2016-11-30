# _*_ coding: utf-8 _*_

import spider
import pymysql


class MovieSaver(spider.Saver):

    def __init__(self):
        spider.Saver.__init__(self)
        self.conn = pymysql.connect(host="59.110.49.40", user="root", password="mimaMIMA123456", db="db_my", charset="utf8")
        self.cursor = self.conn.cursor()
        self.conn.autocommit(1)
        return

    def item_save(self, url, keys, item):
        self.cursor.execute("insert into t_doubanmovies (m_url, m_name, m_year, m_imgurl, m_director, m_writer, m_actors, "
                            "m_genre, m_country, m_language, m_release, m_season, m_jishu, m_length, m_alias, m_website, m_dbsite, "
                            "m_imdb, m_score, m_comment, m_starpercent)"
                            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                            [i.strip() if i is not None else "" for i in item])
        return True
