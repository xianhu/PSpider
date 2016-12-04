# PSpider

Python3下极为简洁的爬虫框架, A simple spider frame written by Python

#### 包含以下模块 (include modules)
1. utilities module: 定义爬虫需要的工具类/工具函数等
2. instances module: 定义抓取过程中的fetcher/parser/saver类
3. abcbase module: 定义多线程、分布式等策略的基础类、函数等
4. concurrent module: 定义多线程爬取策略, 并保证数据同步
5. distributed module: 定义分布式抓取策略（待完善）

#### 包含以下Demo (include demos)
1. demos_yundama: 封装了yundama接口, 方便调用
2. demos_nbastats: 抓取NBA官网上的所有球员数据, 并以此作为案例介绍框架的使用方法
3. demos_doubanmovies: 抓取全部豆瓣电影数据, 也可作为框架使用案例
4. demos_dangdang: 利用selenium抓取当当网数据, 由@Foristkirito提供

#### 其他文件 (other files)
1. setup.py: 安装文件, 可将该框架安装到系统环境中
2. test.py: 测试文件, 可进行简单的功能性测试
3. pylint.conf: 代码检查需要的配置文件

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

#### 下一步计划 (next plan)
1. 利用Redis改为分布式爬虫
2. 利用aiohttp改为协程抓取
3. 完善说明文档

#### 问题汇总
1. 运行报错: Broken pipe    
1.1 老版本会出现这个问题, 主要是由于多线程、多进程同时存在造成的, 更新至最新版本即可
2. 运行报错: No module named 'spider' 或者 'spider don't have attribute WebSpider'    
2.1 该框架目前无法直接利用pip进行安装, 需要下载源文件后, 利用'python setup.py install'进行安装

### 欢迎大家在"Issues"中提出问题或者建议,也可以fork后提交"Pull requests"
### If you have any questions or advices, you can commit "Issues" or "Pull requests"
