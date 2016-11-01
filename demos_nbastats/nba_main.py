# _*_ coding: utf-8 _*_

import spider
import requests

# NBA球员索引URL
url_player_index = "http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=00&Season=2016-17"

# NBA球员统计数据URL,传递参数PlayerID和PerMode("PerGame", "Totals")
url_player_stats = "http://stats.nba.com/stats/playercareerstats?LeagueID=00&PlayerID=%s&PerMode=%s"


# 定义抓取过程
class NBAFetcher(spider.Fetcher):

    def url_fetch(self, url, keys, critical, fetch_repeat):
        """
        这里只需要重写url_fetch函数,参数含义及返回结果见框架
        """
        headers = {"User-Agent": spider.make_random_useragent("pc"), "Accept-Encoding": "gzip"}
        response = requests.get(url, headers=headers, timeout=10)
        return 1, (response.json(), )


# 定义解析过程
class NBAParser(spider.Parser):

    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        这里只需要重写htm_parse函数,参数含义及返回结果见框架
        """
        url_list, saver_list = [], []
        if keys[0] == "index":
            # 解析索引页
            content_json = content[0]

            # 解析所有的球员
            for item in content_json["resultSets"][0]["rowSet"]:
                # 这里放入url_list的item为(url, keys, critical, priority), 注意这里keys的用法
                url_list.append((url_player_stats % (item[0], "Totals"), ("Totals", item[2]), True, 0))
                url_list.append((url_player_stats % (item[0], "PerGame"), ("PerGame", item[2]), True, 0))
        else:
            # 解析球员数据页
            content_json = content[0]

            # 解析球员数据
            saver_list = content_json["resultSets"][0]["rowSet"]
        return 1, url_list, saver_list


# 定义保存过程
class NBASaver(spider.Saver):

    def __init__(self, file_name_total, file_name_pergame):
        """
        构造函数,重写的目的是为了添加表头,并且不同的数据源写入到不同的文件
        """
        spider.Saver.__init__(self)

        # 打开文件,并写入表头
        self.save_pipe_total = open(file_name_total, "w", encoding="utf-8")
        self.save_pipe_total.write("\t".join(["PLAYER_NAME", "PLAYER_ID", "SEASON_ID", "LEAGUE_ID", "TEAM_ID", "TEAM_ABBREVIATION", "PLAYER_AGE",
                                              "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
                                              "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]) + "\n")
        self.save_pipe_pergame = open(file_name_pergame, "w", encoding="utf-8")
        self.save_pipe_pergame.write("\t".join(["PLAYER_NAME", "PLAYER_ID", "SEASON_ID", "LEAGUE_ID", "TEAM_ID", "TEAM_ABBREVIATION", "PLAYER_AGE",
                                                "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
                                                "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]) + "\n")
        return

    def item_save(self, url, keys, item):
        """
        这里只需要重写item_save函数,参数含义及返回结果见框架
        """
        if keys[0] == "Totals":
            self.save_pipe_total.write("\t".join([keys[1]] + [str(i) for i in item]) + "\n")
        elif keys[0] == "PerGame":
            self.save_pipe_pergame.write("\t".join([keys[1]] + [str(i) for i in item]) + "\n")
        else:
            return False
        return True


if __name__ == "__main__":
    """
    main流程
    """
    # 初始化fetcher, parser和saver
    fetcher = NBAFetcher(critical_max_repeat=3, critical_sleep_time=0)
    parser = NBAParser(max_deep=-1, max_repeat=3)
    saver = NBASaver(file_name_total="nba_total.txt", file_name_pergame="nba_pergame.txt")

    # 初始化爬虫, 并传入初始Url
    nba_spider = spider.WebSpider(fetcher, parser, saver, url_filter=None)
    nba_spider.set_start_url(url_player_index, ("index",), critical=True)

    # 开启10个线程抓取数据
    nba_spider.start_work_and_wait_done(fetcher_num=10, is_over=True)

    exit()
