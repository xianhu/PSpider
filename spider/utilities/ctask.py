# _*_ coding: utf-8 _*_

"""
ctask.py by xianhu
"""

import re
from typing import TypeVar


class Task(object):
    """
    class of Task, to define task of fetcher, parser and saver
    """
    # class variable, which to define type of parameters
    TypeContent = TypeVar("TypeContent", str, tuple, list, dict)
    TypeItem = TypeVar("TypeItem", str, tuple, list, dict)

    # class variable, which to parse error message to get a TaskFetch()
    re_obj = re.compile(r"priority=(?P<p>\d+),\s*keys=(?P<k>.+?),\s*deep=(?P<d>\d+),\s*url=(?P<u>.*)$", flags=re.IGNORECASE)

    def __init__(self, priority: int = 0, keys: dict = None, deep: int = 0, url: str = None):
        """
        constructor
        """
        self.priority = priority
        self.keys = keys or {}
        self.deep = deep
        self.url = url or ""
        return

    def __lt__(self, other):
        """
        compare function
        """
        return self.priority < other.priority

    def __str__(self):
        """
        string function
        """
        return f"priority={self.priority}, keys={self.keys}, deep={self.deep}, url={self.url}"


class TaskFetch(Task):
    """
    class of TaskFetch, to define task of fetcher
    """

    def __init__(self, priority=0, keys=None, deep=0, url=None, repeat: int = 0):
        """
        constructor
        """
        super().__init__(priority, keys, deep, url)
        self.repeat = repeat
        return

    @staticmethod
    def from_task_fetch(task_fetch):
        """
        initial a TaskFetch() from task_fetch, repeat += 1
        """
        priority, keys, deep, url = task_fetch.priority, task_fetch.keys, task_fetch.deep, task_fetch.url
        return TaskFetch(priority=priority, keys=keys, deep=deep, url=url, repeat=task_fetch.repeat + 1)

    @staticmethod
    def from_task_parse(task_parse, url_new: str = None):
        """
        initial a TaskFetch() from task_parse and url_new, priority += 1, deep += 1
        """
        priority, keys, deep, url = task_parse.priority, task_parse.keys, task_parse.deep, task_parse.url
        return TaskFetch(priority=priority + 1, keys=keys, deep=deep + 1, url=url_new, repeat=0)

    @staticmethod
    def from_error_message(error_message: str):
        """
        initial a TaskFetch() from error_message
        """
        reg = Task.re_obj.search(error_message)
        priority, keys, deep, url = [reg.group(i) for i in ["p", "k", "d", "u"]]
        return TaskFetch(priority=int(priority), keys=eval(keys), deep=int(deep), url=url.strip(), repeat=0)


class TaskParse(Task):
    """
    class of TaskParse, to define task of parser
    """

    def __init__(self, priority=0, keys=None, deep=0, url=None, content: Task.TypeContent = None):
        """
        constructor
        """
        super().__init__(priority, keys, deep, url)
        self.content = content
        return

    @staticmethod
    def from_task_fetch(task_fetch: Task, content: Task.TypeContent = None):
        """
        initial a TaskParse() from task_fetch and content
        """
        priority, keys, deep, url = task_fetch.priority, task_fetch.keys, task_fetch.deep, task_fetch.url
        return TaskParse(priority=priority, keys=keys, deep=deep, url=url, content=content)


class TaskSave(Task):
    """
    class of TaskSave, to define task of saver
    """

    def __init__(self, priority=0, keys=None, deep=0, url=None, item: Task.TypeItem = None):
        """
        constructor
        """
        super().__init__(priority, keys, deep, url)
        self.item = item
        return

    @staticmethod
    def from_task_parse(task_parse: Task, item: Task.TypeItem = None):
        """
        initial a TaskSave() from task_parse and item
        """
        priority, keys, deep, url = task_parse.priority, task_parse.keys, task_parse.deep, task_parse.url
        return TaskSave(priority=priority, keys=keys, deep=deep, url=url, item=item)
