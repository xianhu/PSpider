# _*_ coding: utf-8 _*_

"""
util_config.py by xianhu
"""

__all__ = [
    "CONFIG_URLPATTERN_ALL",
    "CONFIG_URLPATTERN_FILES",
    "CONFIG_URLPATTERN_IMAGE",
    "CONFIG_URLPATTERN_VIDEO",
    "CONFIG_USERAGENT_PC",
    "CONFIG_USERAGENT_PHONE",
    "CONFIG_USERAGENT_ALL",
]


# define url_patterns, include urlpattern_all, urlpattern_files, urlpattern_image and urlpattern_video
CONFIG_URLPATTERN_ALL = r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|" \
                        "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|pyc|java|c|cc|js|css|log|" \
                        "jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff|" \
                        "mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$"

CONFIG_URLPATTERN_FILES = r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|" \
                          "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|pyc|java|c|cc|js|css|log)$"

CONFIG_URLPATTERN_IMAGE = r"\.(jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff)$"

CONFIG_URLPATTERN_VIDEO = r"\.(mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$"


# define user_agents, include useragent_pc, useragent_phone and useragent_all
CONFIG_USERAGENT_PC = [

    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0)",

    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; The World)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",

    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0)",

    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0)",

    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Maxthon 2.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; TencentTraveler 4.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; The World)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; 360SE)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Avant Browser)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",

    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Maxthon 2.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; TencentTraveler 4.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; The World)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; 360SE)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Avant Browser)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0)",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0 Safari/535.11",

    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.1.3886.400",
    "Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.2.3638.400",
    "Mozilla/5.0 (MSIE 9.0; Windows NT 6.0; Trident/7.0; rv:11.0) like Gecko QQBrowser/8.3.4765.400",
    "Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko QQBrowser/9.1.3471.400",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 3.4.0.12519)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 3.5.0.12758)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 4.0.0.13120)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 4.2.0.13550)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer 5.0.0.14004)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer/6.1.0.8158)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; 2345Explorer/6.2.0.9202)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.0.1369.26)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.2.2603.1)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; UBrowser/5.4.4237.43)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:39.0) Gecko/20100101 Firefox/39.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:41.0) Gecko/20100101 Firefox/41.0",

    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/2.1.7.6 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.11 YYE/3.6 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.46 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2478.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2498.0 Safari/537.36",

    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",

    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
    "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
    "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    "Opera/12.0 (Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
    "Opera/12.0 (Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
]

CONFIG_USERAGENT_PHONE = [
    "Dalvik/1.4.0 (Linux; U; Android 2.3.6; GT-I9108 Build/GINGERBREAD)",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.3; HTC T328d Build/IML74K)",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.4; GT-S7568 Build/IMM76D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.4; HS-EG906 Build/IMM76D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.4; Lenovo A630t Build/IMM76D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.4; T29 Build/IMM76D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.1.1; MI 2 MIUI/JLB54.0)",
    "Dalvik/1.6.0 (Linux; U; Android 4.1.1; MI 2S MIUI/JLB50.0)",
    "Dalvik/1.6.0 (Linux; U; Android 4.1.2; baffin3gduosctc Build/A3244509)",
    "Dalvik/1.6.0 (Linux; U; Android 4.1.2; SM-T211 Build/JZO54K)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.1; 2013022 MIUI/JHACNBL30.0)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.1; vivo X3t Build/JOP40D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.1; ZTE U889 Build/JOP40D)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; 2014011 MIUI/JHFCNBH24.0)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; Coolpad 7296S Build/JDQ39)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; SCH-P709 Build/JDQ39)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; SM-G3818 Build/JDQ39)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; vivo X510t Build/JDQ39)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; A355e Build/534F4F11)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; Coolpad 8720L Build/JSS15Q)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; Coolpad9190L Build/9770AB7E)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; HUAWEI B199 Build/HuaweiB199)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; Lenovo A788t Build/S104)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; loganctc Build/CA651406)",
    "Dalvik/1.6.0 (Linux; U; Android 4.3; R831S Build/JLS36C)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9500 Build/KOT49H)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo S850t Build/KOT49H)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo X2-TO Build/KOT49H)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; 1105 Build/KTU84P)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; Coolpad SK1-01 Build/KTU84P)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; GT-I9508V Build/KTU84P)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; MI 4LTE MIUI/V6.7.1.0.KXDCNCH)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R7c Build/KTU84P)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; T5 Build/KTU84P)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; vivo Y27 Build/KTU84P)",
    "Dalvik/2.1.0 (Linux; U; Android 5.0.2; vivo X5M Build/LRX22G)",
    "Dalvik/2.1.0 (Linux; U; Android 5.0; Lenovo K50-t5 Build/LRX21M)",
    "Dalvik/2.1.0 (Linux; U; Android 5.1; m2 note Build/LMY47D)",

    "Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176",
    "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) FlyFlow/2.0 Mobile/9A405",
    "Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176",
    "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9A334",
    "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) FlyFlow/2.0 Mobile/9B206",
    "Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176",
    "Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B146",
    "Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176",
    "Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B651",
    "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D201",
]

CONFIG_USERAGENT_ALL = CONFIG_USERAGENT_PC + CONFIG_USERAGENT_PHONE


# request headers
CONFIG_HEADERS = {
    "Accept", "Accept-Charset", "Accept-Encoding", "Accept-Language", "Accept-Ranges",
    "Age", "Allow", "Authorization", "Cache-Control", "Connection",
    "Content-Encoding", "Content-Language", "Content-Length", "Content-Location", "Content-MD5", "Content-Range", "Content-Type",
    "Cookie", "Date", "ETag", "Expect", "Expires", "From", "Host",
    "If-Match", "If-Modified-Since", "If-None-Match", "If-Range", "If-Unmodified-Since",
    "Last-Modified", "Location", "Max-Forwards", "Pragma", "Proxy-Authenticate", "Proxy-Authorization", "Range", "Referer", "Retry-After",
    "Server", "TE", "Trailer", "Transfer-Encoding", "Upgrade", "User-Agent", "Vary", "Via",
    "Warning", "WWW-Authenticate", "Origin", "Upgrade-Insecure-Requests", "X_FORWARDED_FOR"
}
