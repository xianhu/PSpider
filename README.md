# PSpider
Python3下极为简洁的爬虫框架, 简单介绍点[这里](https://zhuanlan.zhihu.com/p/23017812), 实例点[这里](https://zhuanlan.zhihu.com/p/23250032)

### utilities module
定义爬虫需要的工具类/工具函数等

### instances module
定义抓取过程中的fetcher/parser/saver类

### concurrent module
定义多线程/多进程爬取策略,并保证数据同步

### others
- setup.py为安装文件,可将该框架安装到系统环境中
- test.py为测试文件,可进行简单的功能性测试
- pylint.conf是代码检查需要的配置文件
- demos_yundama封装了yundama接口,方便调用
- demos_nbastats抓取NBA官网上的所有球员数据,并以此作为案例介绍框架的使用方法

### 问题汇总
- 安装时提示: Could not find suitable distribution for Requirement.parse('pybloom>=2.0.0')
> bloomfilter需要手动安装, 源代码地址在setup文件中, 从GitHub下载后安装即可

### 欢迎大家在"Issues"中提出问题或者建议,也可以fork后提交"Pull requests"
