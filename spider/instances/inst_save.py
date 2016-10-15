# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import time
import logging
import pymysql
from ..utilities import params_chack


class SaverBase(object):
    """
    class of SaverBase, must include function working() and item_save()
    """

    def __init__(self):
        """
        constructor
        """
        self.save_num = 0       # initial: 0, count of items which have been saved successfully
        return

    @params_chack(object, str, object, object)
    def working(self, url, keys, item):
        """
        working function, must "try, except" and call self.item_save(), don't change parameters and returns
        :return result: True or False
        """
        logging.debug("Saver start: keys=%s, url=%s", keys, url)

        try:
            result = self.item_save(url, keys, item)
            self.save_num += 1
        except Exception as excep:
            result = False
            logging.error("Saver error: %s, keys=%s, url=%s", excep, keys, url)

        logging.debug("Saver end: result=%s, url=%s", result, url)
        return result

    def item_save(self, url, keys, item):
        """
        save the item of a url, you can rewrite this function
        :return result: True or False
        """
        raise NotImplementedError


class Saver(SaverBase):
    """
    class of Saver, as subclass of SaverBase
    """

    def __init__(self, save_pipe):
        """
        constructor
        """
        SaverBase.__init__(self)
        self.save_pipe = save_pipe      # output streaming, can be sys.stdout or file handler
        return

    def item_save(self, url, keys, item):
        """
        save the item of a url
        :return result: True or False
        """
        self.save_pipe.write("\t".join([url, str(keys), "\t".join([str(i) for i in item.get_list()])]) + "\n")
        return True


class SaverDatabase(SaverBase):
    """
    class of SaverDatabase, as subclass of SaverBase
    """

    def __init__(self, host="localhost", port=3306, user="", passwd="", database="", charset="utf8", sqlstr=""):
        """
        constructor
        """
        SaverBase.__init__(self)
        self.host = host            # database host
        self.port = port            # database port
        self.user = user            # database user
        self.passwd = passwd        # database password
        self.database = database    # database name
        self.charset = charset      # database charset
        self.sqlstr = sqlstr        # sql string
        return

    def connect_database(self):
        """
        connect database based on self.host, self.user, self.passwd, etc
        """
        raise NotImplementedError

    def check_status(self):
        """
        check the connecting status of database, return True or False
        """
        raise NotImplementedError

    def change_sqlstr(self, sqlstr):
        """
        change sqlstr of this class
        """
        logging.debug("Saver change_sqlstr: %s", sqlstr)
        self.sqlstr = sqlstr
        return

    def item_save(self, url, keys, item):
        """
        save the item of a url, you can rewrite this function
        :return result: True or False
        """
        raise NotImplementedError


class SaverMysql(SaverDatabase):
    """
    class of SaverMysql, as subclass of SaverDatabase
    """

    def __init__(self, host="localhost", port=3306, user="", passwd="", database="", charset="utf8", sqlstr=""):
        """
        constructor
        """
        SaverDatabase.__init__(self, host=host, port=port, user=user, passwd=passwd, database=database, charset=charset, sqlstr=sqlstr)
        self.conn = None             # database connection
        self.cursor = None           # database cursor
        self.connect_database()      # connect database

        # change database status
        if not self.check_status():
            exit()
        return

    def connect_database(self):
        """
        connect database based on self.host, self.user, self.passwd, etc
        """
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.database, charset=self.charset)
            self.cursor = self.conn.cursor()
            self.conn.autocommit(1)
        except Exception as excep:
            self.conn, self.cursor = None, None
            logging.error("Saver error: connect_database %s", excep)
        return

    def check_status(self):
        """
        check the connecting status of database, return True or False
        """
        return True if self.conn and self.cursor else False

    @params_chack(object, str, object, object)
    def working(self, url, keys, item):
        """
        working function, must "try, except" and call self.item_save(), don't change parameters and returns
        :return result: True or False
        """
        logging.debug("Saver start: keys=%s, url=%s", keys, url)

        result, repeat = True, 10
        while repeat > 0:
            try:
                result = self.item_save(url, keys, item)
                self.save_num += 1
                break
            except pymysql.OperationalError as excep:
                repeat -= 1
                if repeat > 0:
                    logging.debug("Saver reconnection: %s, keys=%s, url=%s", excep, keys, url)
                    time.sleep(6)
                    self.connect_database()
                else:
                    logging.error("Saver error: %s, keys=%s, url=%s", excep, keys, url)
                    result = False
                    break
            except Exception as excep:
                logging.error("Saver error: %s, keys=%s, url=%s", excep, keys, url)
                result = False
                break

        logging.debug("Saver end: result=%s, url=%s", result, url)
        return result

    def item_save(self, url, keys, item):
        """
        save the item of a url
        :return result: True or False
        """
        self.cursor.execute(self.sqlstr, item.get_list())
        return True
