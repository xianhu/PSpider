# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

from ..utilities import TaskSave, ResultSave


class Saver(object):
    """
    class of Saver, must include function working()
    """

    def working(self, task_save: TaskSave) -> ResultSave:
        """
        working function, must "try-except" and return ResultSave()
        """
        try:
            result_save = self.item_save(task_save)
        except Exception as excep:
            kwargs = dict(excep_class=self.__class__.__name__, excep_string=str(excep))
            result_save = ResultSave(state_code=-1, **kwargs)

        return result_save

    def item_save(self, task_save: TaskSave) -> ResultSave:
        """
        save the content of an url. Parameters and returns refer to self.working()
        """
        raise NotImplementedError
