import datetime
import os
import pathlib
import re
import time
import queue
import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


class MyTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    时间为切割点日志
    """

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.
        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        # prefix = baseName + "."
        # plen = len(prefix)
        for fileName in fileNames:
            # if fileName[:plen] == prefix:
            # suffix = fileName[:-4]
            if self.extMatch.match(fileName):
                result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result


def split_file_name(filename):
    """
    修改日志文件名称
    """
    file_path = filename.split('default.log.')
    return ''.join(file_path)


log_queue = queue.Queue()


class QueueHandler(logging.Handler):
    def __init__(self, handler_queue):
        super().__init__()
        self.handler_queue = handler_queue

    def emit(self, record):
        self.handler_queue.put(record)


def setup_log(path, log_name="default", **kwargs):
    '''

    :param path: 文件保存的路径，如果没有传，则采用默认路径，在当前路径下创建一个logs的文件夹
    :param log_name: logger对象名称，不传采用默认值：default
    :param kwargs: 支持三种handler：file_handler，console_handler，queue_handler,默认console_handler
    :return:
    '''
    # 创建logger对象,log_name: 日志名字
    logger_obj = logging.getLogger(log_name)
    logger_obj.setLevel(logging.INFO)
    # 创建日志输出格式
    logger_formatter = logging.Formatter(
        "[%(asctime)s] [%(process)d] [%(levelname)s] - %(module)s.%(funcName)s (%(filename)s:%(lineno)d) - %(message)s")
    # logger_formatter = logging.Formatter()
    #  创建一个文件handler
    if kwargs.pop('file_handler', None):  # 关键参数需要设置queue_handler=True
        # log文件夹路径
        YMD = "{}".format(datetime.datetime.now().strftime('%Y%m%d'))
        if path:
            logger_folder_path = pathlib.Path(path) / YMD
        else:
            # logger_folder_path = Path(__file__).parent / 'logs' / YMD
            #  在所在目录的上一级创建目录
            logger_folder_path = Path(__file__).parent.parent / 'logs' / YMD
        # 创建log文件夹
        # print(logger_folder_path)
        logger_folder_path.mkdir(exist_ok=True, parents=True)
        # loge文件路径
        log_file_path = logger_folder_path / 'default.log'
        # when="MIDNIGHT", interval=1,表示每天0点为更新点，每天生成一个文件
        file_handler = MyTimedRotatingFileHandler(filename=str(log_file_path), when='D', interval=1, backupCount=0,
                                                  encoding='utf-8')
        file_handler.namer = split_file_name  # 处理日志文件名称
        file_handler.suffix = "%Y%m%d-%H%M%S.dat"
        file_handler.extMatch = re.compile(r"^\d{4}\d{2}\d{2}-\d{2}\d{2}\d{2}(.dat)$", re.ASCII)
        # 配置日志输出格式
        file_handler.setFormatter(logger_formatter)
        # 增加日志处理器
        logger_obj.addHandler(file_handler)
        # 设置日志的记录等级,常见等级有: DEBUG<INFO<WARING<ERROR
    # 创建一个StreamHandler,用于输出到控制台
    if not kwargs or kwargs.pop('console_handler', None):  # 关键参数需要设置consolehandler=True,如果没有传递参数，则默认设置一个console_handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logger_formatter)
        logger_obj.addHandler(console_handler)
    # 创建一个handler用于传输日志到队列中
    if kwargs.pop('queue_handler', None):  # 关键参数需要设置queue_handler=True
        queue_handler = QueueHandler(log_queue)
        queue_handler.setLevel(logging.DEBUG)
        queue_handler.setFormatter(logger_formatter)
        logger_obj.addHandler(queue_handler)

    return logger_obj


Log = setup_log
if __name__ == "__main__":
    logger = setup_log(path='', log_name="llz_log", file_handler=True)
    n = 1
    while True:
        logger.info(f"this is info message")
        time.sleep(1)
        logger.warning(f"this is a warning message")
        n += 1
