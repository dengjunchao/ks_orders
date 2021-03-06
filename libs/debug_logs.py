"""
    自定义日志模块
"""
import logging
from logging.handlers import RotatingFileHandler


def debug_logs(level):
    """
    file_log_handler:创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    formatter:创建日志记录的格式
                levelname:日志等级
                filename:输入日志信息的文件名
                lineno:行数
                message:日志信息

    logging.getLogger().addHandler：为全局的日志工具对象（flask app使用的）添加日记录器
    logging.basicConfig:设置日志的记录等级
    :param level: 调试debug级
    :return: None
    """

    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)
    logging.basicConfig(level=level)
