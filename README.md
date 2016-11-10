# PSpider
Python3下极为简洁的爬虫框架, 简单介绍点[这里](https://zhuanlan.zhihu.com/p/23017812), 实例点[这里](https://zhuanlan.zhihu.com/p/23250032)

#### 包含以下三个大模块
1. utilities module: 定义爬虫需要的工具类/工具函数等
2. instances module: 定义抓取过程中的fetcher/parser/saver类
3. concurrent module: 定义多线程/多进程爬取策略,并保证数据同步

#### 其他文件
1. setup.py为安装文件,可将该框架安装到系统环境中
2. test.py为测试文件,可进行简单的功能性测试
3. pylint.conf是代码检查需要的配置文件
4. demos_yundama封装了yundama接口,方便调用
5. demos_nbastats抓取NBA官网上的所有球员数据,并以此作为案例介绍框架的使用方法

#### 更新日志
1. 2016-10-20之前, 各种更改结构/功能/类/函数等
2. 2016-10-25, 使用re模块替代bs模块, 删除mysql数据库相关操作, 简化框架
3. 2016-10-27, 添加实例nbastats, 抓取NBA官网上所有球员的赛季数据
4. 2016-10-29, 合并"多线程"和"多进程"池文件, 简化代码
5. 2016-11-01, 使用requests替代urllib, 简化框架
6. 2016-11-08, 删除部分无用函数/类等, 简化框架

#### 下一步计划
1. 利用Redis改为分布式爬虫

#### 问题汇总
- 安装时提示: Could not find suitable distribution for Requirement.parse('pybloom>=2.0.0')
    - bloomfilter需要手动安装, 源代码地址在setup文件中, 从GitHub下载后安装即可

### 欢迎大家在"Issues"中提出问题或者建议,也可以fork后提交"Pull requests"
