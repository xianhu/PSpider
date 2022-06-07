# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

from ..utilities import TaskParse, ResultParse


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def working(self, task_parse: TaskParse) -> ResultParse:
        """
        working function, must "try-except"
        """
        try:
            result_parse = self.htm_parse(task_parse)
        except Exception as excep:
            kwargs = dict(excep_class=self.__class__.__name__, excep_string=str(excep))
            result_parse = ResultParse(state_code=-1, **kwargs)

        return result_parse

    def htm_parse(self, task_parse: TaskParse) -> ResultParse:
        """
        parse the content of an url. Parameters and returns refer to self.working()
        """
        raise NotImplementedError
