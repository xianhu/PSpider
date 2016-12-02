## 当当童书数据爬取

### 爬取所有书籍链接

使用 `key = "lists"` 进行爬取, 爬取之后直接存入数据库中

### 爬取对应书籍页面的详细信息

-  使用 `key = "detail"` 进行爬取
- 当当书籍信息中, 内容推荐, 媒体推荐, 作者简介等信息只有当屏幕显示到那里时才会被 `javascript` 给渲染。因此使用 `selenium + PhantomJS` 爬取时, 要将窗口开大, 同时等待加载完毕。
- 由于 `selenium` 本身一个 `driver` 只能单线程, 如果每一次爬取都反复开关 `driver` 开销太大, 因此在下修改了框架, 在初始化 `spider` 时传入一个 `fetcher` 的 `list`。

### 文件说明

- `demos_dangdang` :  存放 `fetcher`, `parser`, `saver` 的三个类
- `dangdang_book.py`: 分两步抓取链接以及详细信息（合并到test_demos.py中）
