# PSpider

A simple web spider frame written by Python, which needs Python3.5+

### Features of PSpider
1. Support multi-threading crawling mode (using threading and requests)
2. Support multi-processing in parse process, automatically (using multiprocessing)
3. Support using proxies for crawling (using threading and queue)
4. Define some utility functions and classes, for example: UrlFilter, get_string_num, etc
5. Fewer lines of code, easyer to read, understand and expand

### Modules of PSpider
1. utilities module: define some utilities functions and classes for spider
2. instances module: define classes of fetcher, parser, saver for multi-threading spider
3. concurrent module: define WebSpiderFrame of multi-threading spider

### Procedure of PSpider
![](procedure.png)
①: Fetcher gets url from UrlQueue, and makes requests based on this url  
②: Put the result of ① to HtmlQueue, and so Parser can get it  
③: Parser gets item from HtmlQueue, and parses it to get new urls and saved items  
④: Put the new urls to UrlQueue, and so Fetcher can get it  
⑤: Put the saved items to ItemQueue, and so Saver can get it  
⑥: Saver gets item from ItemQueue, and saves it to filesystem or database  
⑦: Proxieser gets proxies from web or database and puts proxies to ProxiesQueue  
⑧: Fetcher gets proxies from ProxiesQueue if needed, and makes requests based on this proxies  

### Tutorials of PSpider
**Installation: you'd better use the first method**  
（1）Copy the "spider" directory to your project directory, and `import spider`  
（2）Install spider to your python system using `python3 setup.py install`  

**See test.py**  

### TodoList
1. Distribute Spider
2. Execute JavaScript
3. More Demos

### If you have any questions or advices, you can commit "Issues" or "Pull requests"
