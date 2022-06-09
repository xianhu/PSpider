# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

from ..utilities import ResultProxies


class Proxieser(object):
    """
    class of Proxieser, must include function working()
    """

    def working(self) -> ResultProxies:
        """
        working function, must "try-except" and return ResultProxies()
        """
        try:
            result_proxies = self.proxies_get()
        except Exception as excep:
            kwargs = dict(excep_class=self.__class__.__name__, excep_string=str(excep))
            result_proxies = ResultProxies(state_code=-1, proxies_list=None, **kwargs)

        return result_proxies

    def proxies_get(self) -> ResultProxies:
        """
        get proxies from web or database. Parameters and returns refer to self.working()
        """
        raise NotImplementedError
