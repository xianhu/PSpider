# PSpider

Python3下极为简洁的爬虫框架, A simple spider frame written by Python

#### 框架（spider）包含以下模块
1. utilities module: 定义爬虫需要的工具类、工具函数等
2. instances module: 定义多线程抓取过程中的fetcher抓取类、parser解析类、saver保存类
3. abcbase module: 定义多线程爬虫、协程爬虫、分布式爬虫等需要的一些基类
4. concurrent module: 定义多线程爬虫框架、异步爬虫框架, 并保证数据同步
5. distributed module: 定义分布式爬虫框架（待完成）

#### 框架抓取流程示意图
1. 多线程抓取流程
![](otherfiles/threads.png)  
①：Fetcher抓取类从UrlQueue中获取需要抓取的Url进行请求
②：请求得到的内容（自定义）放入HtmlQueue中, 供Parser解析类获取
③：Parser解析类从HtmlQueue中获取需要解析的内容进行解析
④：解析得到的新的待抓取Url放入UrlQueue中, 供Fetcher抓取类获取
⑤：解析得到的需要保存的内容（自定义）放入ItemQueue中, 供Saver保存类获取
⑥：Saver保存类从ItemQueue中获取需要保存的内容, 将其写入到文件系统或数据库

2. 协程抓取流程
协程抓取流程类似于多线程抓取流程, 只不过用"协程"替代了多线程。
协程框架中只有一个队列Queue, 用于保存待抓取的Url。
Fetcher类从队列中获取Url进行请求, 并将结果给到Parser类。
Parser类从请求的内容中获取新的Url和待保存的内容, 分别给到队列Queue和Saver类。
Saver类保存需要保存的内容。
重复上述过程即可。

#### 框架开始教程

**安装: 以下两种方法均可, 建议使用第一种**
（1）直接将"spider"文件夹拷贝到项目所在目录, 然后新建Py文件并引入spider即可
（2）利用setup.py文件将该框架安装到Python的第三方库中: `python3 setup.py install`

**开始使用多线程爬虫: 以抓取豆瓣电影中tag为"爱情"的电影数据为例**
（1）引入spider库 `import spider`
（2）继承spider.Fetcher类, 构造MovieFetcher抓取类, 并重写url_fetch函数

    class MovieFetcher(spider.Fetcher):

        def __init__(self, max_repeat=3, sleep_time=0):
            spider.Fetcher.__init__(self, max_repeat=max_repeat, sleep_time=sleep_time)    
            self.session = requests.Session()
            return
        
        def url_fetch(self, url, keys, repeat):
            resp = self.session.get(url, allow_redirects=False, verify=False, timeout=5)
            if resp.status_code == 200:
                return 1, resp.text
            resp.raise_for_status()

（3）继承spider.Parser类, 构造MovieParser解析类, 并重写htm_parse函数
    
    class MovieParser(spider.Parser):
    
        def htm_parse(self, priority, url, keys, deep, content):
            url_list, save_list = [], []
            soup = BeautifulSoup(content, "html5lib")
    
            # 根据keys决定content如何进行解析, 类似于回调函数的功能
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
                # 解析电影详情页, 并将结果放入到save_list中
                content = soup.find("div", id="content")
                ......
                save_list.append(movie)
            return 1, url_list, save_list
    
（4）构造多线程爬虫, 这里的Saver保存类直接使用框架自带的即可, 当然你也可以自定义

    # 利用MovieFetcher、MovieParser和Saver构造爬虫, 并传入框架自带的UrlFilter进行Url过滤
    dou_spider = spider.WebSpider(MovieFetcher(), MovieParser(max_deep=-1), spider.Saver(), spider.UrlFilter())
    
    # 设置种子Url, 并设置Keys, Keys用于实现回调函数的功能
    dou_spider.set_start_url("https://movie.douban.com/tag/%E7%88%B1%E6%83%85", ("index",), priority=1)
    
    # 开启多线程进行抓取工作, 并等待其结束
    dou_spider.start_work_and_wait_done(fetcher_num=20)
一个简单的多线程爬虫就构造完成了, 框架本身完成线程调度、数据同步等功能, 使用者只需要专注于"抓取如何防止被封", "如何解析页面", "如何保存内容"即可。

**开始使用协程爬虫: 以抓取360应用市场为例**

    # 初始化WebSpiderAsync
    web_spider_async = spider.WebSpiderAsync(max_repeat=3, sleep_time=0, max_deep=1, save_pipe=open("out_async.txt", "w"), url_filter=spider.UrlFilter())

    # 添加种子Url
    web_spider_async.set_start_url("http://zhushou.360.cn/")

    # 开始抓取任务并等待其结束
    web_spider_async.start_work_and_wait_done(fetcher_num=10)
这里并没有自定义Fetcher、Parser和Saver流程, 而是全部使用了框架自带的, 会得到每一个页面的Url、Title和获取时间。
如果使用者需要自定义抓取、解析、保存过程, 则需要学习Python的异步库aiohttp, 并继承spider.WebSpiderAsync类, 重写里边的方法。

#### 项目包含以下Demo（由于时间原因, 不保证所有Demo可用）
1. demos_yundama: 封装了yundama接口, 方便调用
2. demos_nbastats: 抓取NBA官网上的所有球员数据
3. demos_doubanmovies: 抓取全部豆瓣电影数据
4. demos_dangdang: 利用selenium抓取当当网数据, 由@Foristkirito提供

#### 更新日志 (update logs)
1. 2016-10-20之前, 各种更改结构/功能/类/函数等
2. 2016-10-25, 使用re模块替代bs模块, 删除mysql数据库相关操作, 简化框架
3. 2016-10-27, 添加实例nbastats, 抓取NBA官网上所有球员的赛季数据
4. 2016-10-29, 合并"多线程"和"多进程"池文件, 简化框架
5. 2016-11-01, 使用requests替代urllib, 简化框架
6. 2016-11-08, 删除部分无用函数/类等, 简化框架
7. 2016-11-13, 更新pybloom至pybloom-live, 可直接利用pip安装
8. 2016-11-17, 添加Dockerfile文件和requirements.txt文件
9. 2016-11-27, 删除多进程策略, 此策略在Mac上可以, 但在Windows上有问题
10. 2016-11-29, 添加豆瓣电影爬虫, 单机半小时爬取全部电影数据
11. 2016-12-03, 修改Fetcher全为一个的Bug, 在此感谢@Foristkirito
12. 2016-12-07, 添加异步爬虫框架代码, 并更改spider的代码文件结构
13. 2016-12-12, 增加爬虫流程说明、文档说明等

#### 下一步计划 (next plan)
1. 利用Redis改为分布式爬虫
2. ~~利用aiohttp改为协程抓取~~

### 欢迎大家在"Issues"中提出问题或者建议,也可以fork后提交"Pull requests"
