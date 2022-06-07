# _*_ coding: utf-8 _*_

"""
cresult.py by xianhu
"""

from .ctask import TaskParse, TaskSave


class Result(object):
    """
    class of Result, to define result
    """

    def __init__(self, state_code, excep_class=None, excep_string=None):
        """
        constructor
        :param state_code: can be -1, 0 or 1
        :param excep_class: name of class which raised exception
        :param excep_string: string of exception, error message
        """
        self.state_code = state_code
        self.excep_class = excep_class
        self.excep_string = excep_string
        return


class ResultFetch(Result):
    """
    result of Fetcher
    """

    def __init__(self, state_code: int, state_proxies: int = 1, task_parse: TaskParse = None, excep_class=None, excep_string=None):
        """
        constructor
        :param state_code: can be -1(fetch failed), 0(need repeat), 1(fetch success)
        :param state_proxies: can be -1(unavaiable), 0(return to queue), 1(avaiable)
        """
        super().__init__(state_code, excep_class, excep_string)
        self.state_proxies = state_proxies
        self.task_parse = task_parse
        return


class ResultParse(Result):
    """
    result of Parser
    """

    def __init__(self, state_code: int, task_fetch_list: list = None, task_save: TaskSave = None, excep_class=None, excep_string=None):
        """
        constructor
        :param state_code: can be -1(parse failed), 1(parse success)
        """
        super().__init__(state_code, excep_class, excep_string)
        self.task_fetch_list = task_fetch_list
        self.task_save = task_save
        return


class ResultProxies(Result):
    """
    result of Proxies
    """

    def __init__(self, state_code: int, proxies_list: list, excep_class=None, excep_string=None):
        """
        constructor
        :param state_code: can be -1(save failed), 1(save success)
        """
        super().__init__(state_code, excep_class, excep_string)
        self.proxies_list = proxies_list
        return
