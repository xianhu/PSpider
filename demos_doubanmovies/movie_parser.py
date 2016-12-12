# _*_ coding: utf-8 _*_

import spider
from bs4 import BeautifulSoup


class MovieParser(spider.Parser):

    def htm_parse(self, priority, url, keys, deep, content):
        url_list, save_list = [], []
        soup = BeautifulSoup(content, "html5lib")

        if keys[0] == "index":
            # 获取列表页中所有的电影页面Url
            div_movies = soup.find_all("a", class_="nbg", title=True)
            url_list.extend([(item.get("href"), ("detail", keys[1]), 0) for item in div_movies])

            # 获取列表页的下一页
            next_page = soup.find("span", class_="next")
            if next_page:
                next_page_a = next_page.find("a")
                if next_page_a:
                    url_list.append((next_page_a.get("href"), ("index", keys[1]), 1))
        else:
            content = soup.find("div", id="content")

            # 标题
            name_and_year = [item.get_text() for item in content.find("h1").find_all("span")]
            name, year = name_and_year if len(name_and_year) == 2 else (name_and_year[0], "")
            movie = [url, name.strip(), year.strip("()")]

            # 左边
            content_left = soup.find("div", class_="subject clearfix")

            nbg_soup = content_left.find("a", class_="nbgnbg").find("img")
            movie.append(nbg_soup.get("src") if nbg_soup else "")

            info = content_left.find("div", id="info").get_text()
            info_dict = dict([line.strip().split(":", 1) for line in info.strip().split("\n") if line.strip().find(":") > 0])

            movie.append(info_dict.get("导演", "").replace("\t", " "))
            movie.append(info_dict.get("编剧", "").replace("\t", " "))
            movie.append(info_dict.get("主演", "").replace("\t", " "))

            movie.append(info_dict.get("类型", "").replace("\t", " "))
            movie.append(info_dict.get("制片国家/地区", "").replace("\t", " "))
            movie.append(info_dict.get("语言", "").replace("\t", " "))

            movie.append(info_dict.get("上映日期", "").replace("\t", " ") if "上映日期" in info_dict else info_dict.get("首播", "").replace("\t", " "))
            movie.append(info_dict.get("季数", "").replace("\t", " "))
            movie.append(info_dict.get("集数", "").replace("\t", " "))
            movie.append(info_dict.get("片长", "").replace("\t", " ") if "片长" in info_dict else info_dict.get("单集片长", "").replace("\t", " "))

            movie.append(info_dict.get("又名", "").replace("\t", " "))
            movie.append(info_dict.get("官方网站", "").replace("\t", " "))
            movie.append(info_dict.get("官方小站", "").replace("\t", " "))
            movie.append(info_dict.get("IMDb链接", "").replace("\t", " "))

            # 右边
            content_right = soup.find("div", class_="rating_wrap clearbox")
            if content_right:
                movie.append(content_right.find("strong", class_="ll rating_num").get_text())

                rating_people = content_right.find("a", class_="rating_people")
                movie.append(rating_people.find("span").get_text() if rating_people else "")

                rating_per_list = [item.get_text() for item in content_right.find_all("span", class_="rating_per")]
                movie.append(", ".join(rating_per_list))
            else:
                movie.extend(["", "", ""])

            assert len(movie) == 21, "length of movie is invalid"
            save_list.append(movie)
        return 1, url_list, save_list
