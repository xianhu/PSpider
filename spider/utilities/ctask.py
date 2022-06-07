# _*_ coding: utf-8 _*_

"""
util_task.py by xianhu
"""

import re


class Task(object):
    """
    class of Task, to define task
    """
    # class variable, which to parse error message to get a task
    re_obj = re.compile(r"priority=(?P<p>\d+),\s*keys=(?P<k>.+?),\s*deep=(?P<d>\d+),\s*url=(?P<u>.+)$", flags=re.IGNORECASE)

    def __init__(self, url: str, priority: int = 0, keys: dict = None, deep: int = 0):
        """
        constructor
        """
        self.url = url
        self.priority = priority
        self.keys = keys or {}
        self.deep = deep
        return

    def __lt__(self, other):
        """
        compare function
        """
        return self.priority < other.priority

    def __str__(self):
        """
        str function
        """
        return "priority={p}, keys={k}, deep={d}, url={u}".format(
            p=self.priority,
            k=self.keys,
            d=self.deep,
            u=self.url,
        )

    @staticmethod
    def from_str(error_message):
        """
        initial a task from error_message
        """
        reg = Task.re_obj.search(error_message)
        return Task(
            url=reg.group("u").strip(),
            priority=int(reg.group("p")),
            keys=eval(reg.group("k")),
            deep=int(reg.group("d")),
        )


class TaskFetch(Task):
    """
    task of Fetcher
    """

    def __init__(self, url: str, priority: int = 0, keys: dict = None, deep: int = 0, repeat: int = 0):
        """
        constructor
        """
        super().__init__(url, priority, keys, deep)
        self.repeat = repeat
        return


class TaskParse(Task):
    """
    task of Parser
    """

    def __init__(self, url: str, priority: int = 0, keys: dict = None, deep: int = 0, html: str = None):
        """
        constructor
        """
        super().__init__(url, priority, keys, deep)
        self.html = html
        return


class TaskSave(Task):
    """
    task of Saver
    """

    def __init__(self, url: str, priority: int = 0, keys: dict = None, deep: int = 0, item: object = None):
        """
        constructor
        """
        super().__init__(url, priority, keys, deep)
        self.item = item
        return
