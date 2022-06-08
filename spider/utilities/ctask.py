# _*_ coding: utf-8 _*_

"""
ctask.py by xianhu
"""

import re


class Task(object):
    """
    class of Task, to define task of fetcher, parser and saver
    """
    # class variable, which to parse error message to get a TaskFetch()
    re_obj = re.compile(r"priority=(?P<p>\d+),\s*keys=(?P<k>.+?),\s*deep=(?P<d>\d+),\s*url=(?P<u>.+)$", flags=re.IGNORECASE)

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

    def __init__(self, priority: int = 0, keys: dict = None, deep: int = 0, url: str = None, repeat: int = 0):
        """
        constructor
        """
        super().__init__(priority, keys, deep, url)
        self.repeat = repeat
        return

    @staticmethod
    def from_string(error_message):
        """
        initial a TaskFetch() from error_message
        """
        reg = Task.re_obj.search(error_message)
        return TaskFetch(
            priority=int(reg.group("p")),
            keys=eval(reg.group("k")),
            deep=int(reg.group("d")),
            url=reg.group("u").strip(),
        )


class TaskParse(Task):
    """
    class of TaskParse, to define task of parser
    """

    def __init__(
            self, priority: int = 0, keys: dict = None, deep: int = 0, url: str = None,
            content: object = None, task_fetch: TaskFetch = None,
    ):
        """
        constructor
        """
        if task_fetch:
            priority, keys, deep, url = task_fetch.priority, task_fetch.keys, task_fetch.deep, task_fetch.url
        super().__init__(priority, keys, deep, url)
        self.content = content
        return


class TaskSave(Task):
    """
    class of TaskSave, to define task of saver
    """

    def __init__(
            self, priority: int = 0, keys: dict = None, deep: int = 0, url: str = None,
            item: object = None, task_parse: TaskParse = None,
    ):
        """
        constructor
        """
        if task_parse:
            priority, keys, deep, url = task_parse.priority, task_parse.keys, task_parse.deep, task_parse.url
        super().__init__(priority, keys, deep, url)
        self.item = item
        return
