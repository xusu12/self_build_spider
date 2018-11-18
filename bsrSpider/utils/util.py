import os, sys
import logging
from logging.handlers import TimedRotatingFileHandler
from conf.config import LOG_TEM_DEBUG, LOG_TEM_INFO, LOG_TEM_DB, LOG_TEM_ERROR, BASE_DIR, LOG_DIR, BASE_TYPE


class Logger:
    def __init__(self, log_level='error', log_name='debug'):
        path = os.path.join(LOG_DIR, '%s_%s.log' % (log_name, log_level))
        if BASE_TYPE == 'develop':
            if log_level == 'error':
                log_level = 'debug'
        if log_level == 'debug':
            formatter = LOG_TEM_DEBUG
            clevel = logging.DEBUG
            flevel = logging.INFO
        if log_level == 'error':
            formatter = LOG_TEM_ERROR
            clevel = logging.INFO
            flevel = logging.WARNING
        if log_level == 'info':
            formatter = LOG_TEM_INFO
            clevel = logging.INFO
            flevel = logging.INFO
        if log_level == 'DB':
            formatter = LOG_TEM_DB
            clevel = logging.DEBUG
            flevel = logging.INFO

        # 初始化日志
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(*formatter)

        # 设置sheel日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        maxBytes = 50 * 1024 * 1024     # 50M

        # 设置file日志
        # fh = TimedRotatingFileHandler(path, mode='a', maxBytes=maxBytes, backupCount=10, encoding='utf-8')
        fh = TimedRotatingFileHandler(path, when='d', interval=1, backupCount=12, encoding='utf-8', delay=False,
                                      utc=False)
        fh.setFormatter(fmt)
        fh.setLevel(flevel)

        # 注册日志
        if not self.logger.handlers:
            self.logger.addHandler(sh)
            self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)