# PSpider

Python3下极为简洁的爬虫框架, A simple spider frame written by Python    
简单介绍点[这里](https://zhuanlan.zhihu.com/p/23017812), 实例点[这里](https://zhuanlan.zhihu.com/p/23250032)

#### 包含以下三个大模块 (three modules)
1. utilities module: 定义爬虫需要的工具类/工具函数等
2. instances module: 定义抓取过程中的fetcher/parser/saver类
3. concurrent module: 定义多线程/多进程爬取策略, 并保证数据同步

#### 其他文件 (other files)
1. setup.py为安装文件, 可将该框架安装到系统环境中
2. test.py为测试文件, 可进行简单的功能性测试
3. pylint.conf是代码检查需要的配置文件
4. demos_yundama封装了yundama接口, 方便调用
5. demos_nbastats抓取NBA官网上的所有球员数据, 并以此作为案例介绍框架的使用方法

#### 更新日志 (update logs)
1. 2016-10-20之前, 各种更改结构/功能/类/函数等
2. 2016-10-25, 使用re模块替代bs模块, 删除mysql数据库相关操作, 简化框架
3. 2016-10-27, 添加实例nbastats, 抓取NBA官网上所有球员的赛季数据
4. 2016-10-29, 合并"多线程"和"多进程"池文件, 简化框架
5. 2016-11-01, 使用requests替代urllib, 简化框架
6. 2016-11-08, 删除部分无用函数/类等, 简化框架
7. 2016-11-13, 更新pybloom至pybloom-live, 可直接利用pip安装
8. 2016-11-17, 添加Dockerfile文件和requirements.txt文件

#### 下一步计划 (next plan)
1. 利用Redis改为分布式爬虫

#### 问题汇总

### 欢迎大家在"Issues"中提出问题或者建议,也可以fork后提交"Pull requests"
### If you have any questions or advices, you can commit "Issues" or "Pull requests"
