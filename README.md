# PSpider

A simple spider frame written by Python, which needs Python3.5+

### Features of PSpider
1. Support multi-threading crawling mode (using threading and requests)
2. Support asyncio crawling mode (using aiohttp)
3. Support distributed crawling mode (using redis and threading)
4. Define some utility functions and classes, for example: UrlFilter, make_random_useragent, etc
5. Fewer lines of code, easyer to read, understand and expand

### Modules of PSpider
1. utilities module: define utilities functions and classes for spider
2. insts_async module: define classes of fetcher, parser, saver for asyncio spider
3. insts_thread module: define classes of fetcher, parser, saver for multi-threading spider
4. concurrent module: define WebSpiderFrame of multi-threading spider, asyncio spider and distributed spider

### Procedure of PSpider
1. procedure of multi-threading spider  
![](procedure.png)  
①: Fetcher gets url from UrlQueue, and makes requests based on this url  
②: Put the result of ① to HtmlQueue, and so Parser can get it  
③: Parser gets item from HtmlQueue, and parses it to get new urls and saved items  
④: Put the new urls to UrlQueue, and so Fetcher can get it  
⑤: Put the saved items to ItemQueue, and so Saver can get it  
⑥: Saver gets item from ItemQueue, and saves it to filesystem or database  

2. procedure of asyncio spider  
Similar with multi-threading spider. The only difference is using "coroutine" instead of "multi-threads".  

3. procedure of distributed spider  
Similar with multi-threading spider. The only difference is getting url from redis instead of queue.  

### Tutorials of PSpider
**Installation: you'd better use the first method**  
（1）Copy the "spider" directory to your project directory, and `import spider`  
（2）Install spider to your python system using `python3 setup.py install`  

**See test.py**  

### If you have any questions or advices, you can commit "Issues" or "Pull requests"
