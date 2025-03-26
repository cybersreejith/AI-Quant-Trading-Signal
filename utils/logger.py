import logging
import os
from datetime import datetime
from config.settings import LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str) -> logging.Logger:
    """
    设置日志记录器
    :param name: 日志记录器名称
    :return: 配置好的日志记录器
    """
    # 创建logs目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # 如果已经有处理器，不重复添加
    if logger.handlers:
        return logger
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # 创建文件处理器
    log_file = f'logs/{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger 