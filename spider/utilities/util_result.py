# _*_ coding: utf-8 _*_

"""
util_result.py by xianhu
"""


class Result(object):
    """
    class of Result, to define result
    """

    def __init__(self, state_code):
        """
        constructor
        """
        self.state_code = state_code
        return


class ResultF(Result):
    """
    result of Fetcher
    """

    def __init__(self, state_code: int):
        """
        constructor
        """
        super().__init__(state_code)
        return


class ResultP(Result):
    """
    result of Parser
    """

    def __init__(self, state_code: int):
        """
        constructor
        """
        super().__init__(state_code)
        return


class ResultS(Result):
    """
    result of Saver
    """

    def __init__(self, state_code: int):
        """
        constructor
        """
        super().__init__(state_code)
        return
