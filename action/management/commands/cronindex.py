#coding=utf8
from dbss.daemonize import Daemonize
import logging
import logging.handlers
import time

from django.conf import settings
from django.core.management.base import BaseCommand

import django_rq
from redis_cache import get_redis_connection

from dbss.cardspace.models import warp_update_index

def test():
    pass

class MyDaemonized(Daemonize):

    def run(self):
        while True:
            self.logger.info('cron update index start')
            index_queue = django_rq.get_queue(settings.INDEX_QUEUE)
            if index_queue.count < 1 :
                index_redis = get_redis_connection('djrq')
                index_count = int(index_redis.get(settings.INDEX_NAME))
                if index_count > 0:
                    self.logger.info('index count is ' + str(index_count) + ', cron update index enqueue')
                    index_redis.set(settings.INDEX_NAME, 0)
                    index_queue.enqueue(warp_update_index)
            self.logger.info('cron update index done, sleep ' + str(settings.INDEX_TIME) + '\n*********************')
            time.sleep(settings.INDEX_TIME)

class Command(BaseCommand):

    help =  '''
    crond job to update index'
    cron excute update index action
    configurate time and count in settings.py
    '''
    def handle(self, *args, **kwargs):
        loghandler = logging.handlers.RotatingFileHandler('/var/log/cronindex.log' , maxBytes=10*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s')
        loghandler.setFormatter(formatter)
        cronlog = logging.getLogger('cronindex')
        cronlog.addHandler(loghandler)
        cronlog.setLevel(logging.DEBUG)
        daemond = MyDaemonized(app='cronindex', pid='/tmp/cronui.pid', action = test, keep_fds=[loghandler.stream.fileno()])
        daemond.start()
