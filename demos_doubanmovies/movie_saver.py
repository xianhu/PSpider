# _*_ coding: utf-8 _*_

import spider


class MovieSaver(spider.Saver):

    def item_save(self, url, keys, item):
        self.save_pipe.write("\t".join([i if i else "" for i in item]) + "\n")
        return True
