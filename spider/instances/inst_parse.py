# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        :param max_deep: default 0, if -1, spider will not stop until all urls are fetched
        """
        self._max_deep = max_deep
        return

    def working(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, list):
        """
        working function, must "try, except" and don't change the parameters and returns
        :return parse_state: can be -1(parse failed), 1(parse success)
        :return url_list: [(url1, keys1, priority1), ...], or exception information[class_name, excep]
        :return save_list: [item1(a list or tuple), item2(a list or tuple), ...]
        """
        try:
            parse_state, url_list, save_list = self.htm_parse(priority, url, keys, deep, content)
        except Exception as excep:
            parse_state, url_list, save_list = -1, [self.__class__.__name__, str(excep)], []

        return parse_state, url_list, save_list

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, list):
        """
        parse the content of a url, you must overwrite this function, parameters and returns refer to self.working()
        """
        raise NotImplementedError
