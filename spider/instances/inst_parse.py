# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def working(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, object):
        """
        working function, must "try, except" and don't change the parameters and returns
        :return parse_state: can be -1(parse failed), 1(parse success)
        :return url_list: [(url1, keys1, priority1), ...], or exception information[class_name, excep]
        :return item: which waits for saved, can be any object, None for nothing
        """
        try:
            parse_state, url_list, item = self.htm_parse(priority, url, keys, deep, content)
        except Exception as excep:
            parse_state, url_list, item = -1, [self.__class__.__name__, str(excep)], None

        return parse_state, url_list, item

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object) -> (int, list, object):
        """
        parse the content of a url, you must overwrite this function, parameters and returns refer to self.working()
        """
        raise NotImplementedError
