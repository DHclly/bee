"""
# 日志模块，在入口文件中添加以下代码，需要在其他模块之前加上

from services.log_service import get_logger
logger=get_logger()

# 在其他子模块中调用

from services.log_service import logger

# 支持的方法：

# 默认的方法
logger.info("hi")
logger.error("hi")
logger.warn("hi")

# 解析对象第一层数据，并对每个值进行截断
logger.dump_data({"key": "value", "list": [1, 2, 3]}, truncate_length=3)

# 记录带有时间差的日志信息
import time
logger.with_time("This message has a time stamp")
time.sleep(3)
logger.with_time("This message has a time stamp2")
"""

import inspect
import logging
import logging.handlers
import os
import time
from copy import deepcopy

from services import env_service

# 初始化 logger
logger = None

def get_logger(main_path=None, print_start=True):
    """
    获取一个自定义的日志记录器。

    :param main_path: 主路径，用于确定服务器名称和路径。
    :param print_start: 是否在日志中打印服务启动信息。
    :return: 返回一个自定义的日志记录器。
    """
    global logger
    
    if logger is not None:
        return logger
    
    # 获取主路径
    if main_path is None:
        main_path = _get_main_path()
    
    server_name, server_path = _get_server_name_and_path(main_path)
    
    # 定义日志格式
    log_formatter = logging.Formatter(
        '[%(name)s][%(asctime)s][%(levelname)s][%(filename)s line:%(lineno)s]:%(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 创建日志文件路径
    log_folder_path = os.path.join(server_path, "logs")
    log_file_path = os.path.join(log_folder_path, f"{server_name}.log")
    log_level=_get_log_level()
    
    # 创建日志文件夹
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    
    # 定义日志文件大小和备份数量
    max_file_size = 2 * 1024 * 1024  # 2 MB
    backup_count = 3  # 最多保留3个备份文件
    
    # 创建文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path, 
        maxBytes=max_file_size, 
        backupCount=backup_count,
        encoding='utf-8'
    ) 
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_formatter)

    # 获取或创建日志记录器
    inner_logger = logging.getLogger(server_name)
    # 禁用日志传播
    inner_logger.propagate = False
    inner_logger.setLevel(log_level)
    inner_logger.addHandler(console_handler)
    inner_logger.addHandler(file_handler)
    
    # 重写 error 方法，添加 stack_info 和 stacklevel 参数
    raw_error = inner_logger.error
    def error(msg, *args, **kwargs):
        if 'stack_info' not in kwargs:
            kwargs['stack_info'] = True
        if 'stacklevel' not in kwargs:
            kwargs['stacklevel'] = 2
        raw_error(msg, *args, **kwargs)
    inner_logger.error = error
    
    # 添加 dump_data 方法，用于解析和截断数据
    inner_logger.dump_data = lambda raw_data, truncate_length=100: _dump_data(inner_logger, raw_data, truncate_length)
    
    # 添加 with_time 方法，用于记录带有时间差的日志信息
    inner_logger.diff_id = 1
    inner_logger.diff_last_time = None
    inner_logger.with_time = lambda message: _with_time(inner_logger, message)
    
    # 设置全局 logger
    logger = inner_logger
    
    # 打印服务启动信息
    if print_start:
        inner_logger.info("-----------------------------")
        inner_logger.info("-----------------------------")
        inner_logger.info(f"{server_name} service start")
        inner_logger.info("-----------------------------")
        inner_logger.info("-----------------------------")
    
    return inner_logger

def _get_log_level():
    level=env_service.get_log_level()
    if level=="debug":
        return logging.DEBUG
    
    if level=="info":
        return logging.INFO
    
    if level=="warning":
        return logging.WARNING
    
    return logging.INFO

def _get_server_name_and_path(main_path):
    """
    根据主路径获取服务器名称和服务器路径。
    
    :param main_path: 主路径。
    :return: 服务器名称和服务器路径的元组。
    """
    path_parts = main_path.split(os.sep)
    path_len=len(path_parts)
    server_name = path_parts[-2] if path_len > 2 else "app"
    server_path = os.sep.join(path_parts[:-1]) if path_len > 2 else "/"
    return server_name, server_path

def _get_main_path():
    """
    获取调用者模块的绝对路径。
    
    :return: 调用者模块的绝对路径。
    """
    # 获取当前栈帧
    current_frame = inspect.currentframe()
    try:
        # 回溯到调用者的栈帧
        caller_frame = current_frame.f_back.f_back
        if caller_frame:
            module = inspect.getmodule(caller_frame)
            if module and hasattr(module, '__file__'):
                return os.path.abspath(module.__file__)
    finally:
        # 删除帧对象以避免循环引用
        del current_frame
    return None

def _dump_data(logger, raw_data, truncate_length=100):
    """
    解析并截断 raw_data，然后通过 logger 输出。
    
    :param logger: 日志记录器。
    :param raw_data: 原始数据。
    :param truncate_length: 截断长度，默认为100。
    """
    data = deepcopy(raw_data)
    if isinstance(data, str):
        data = _truncate_data(data, truncate_length)
    elif isinstance(data, int | float):
        data = _truncate_data(data, truncate_length)
    elif isinstance(data, bool):
        pass
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = _truncate_data(value, truncate_length)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            data[idx] = _truncate_data(item, truncate_length)
    elif isinstance(data, tuple):
        data = tuple(_truncate_data(item, truncate_length) for item in data)
    elif isinstance(data, object) and hasattr(data, '__dict__'):
        _dump_data(logger, data.__dict__, truncate_length)
        return
    else:
        pass
    logger.info(data, stacklevel=3)

def _truncate_data(param_value, truncate_length=100):
    """
    截断字符串或数字。
    
    :param param_value: 需要截断的参数值。
    :param truncate_length: 截断长度，默认为100。
    :return: 截断后的字符串。
    """
    if isinstance(param_value, bytes):
        str_value = param_value.decode('utf-8', errors='ignore')
    else:
        str_value = str(param_value)
        
    if len(str_value) > truncate_length:
        str_value = f"{str_value[:truncate_length]}..."
    return str_value

def _with_time(logger, message):
    """
    记录带有时间差的日志信息。
    
    :param logger: 日志记录器。
    :param message: 日志信息。
    """
    diff_time = 0.000
    current_time = time.time()
    if logger.diff_last_time is not None:
        diff_time = round(current_time - logger.diff_last_time, 3)
    logger.info(f"[step {logger.diff_id} cost {diff_time:.3f}s]=>{message}", stacklevel=3)
    logger.diff_id = logger.diff_id+1 if logger.diff_id < 999999999 else 1
    logger.diff_last_time = current_time

if __name__ == '__main__':
    raise Exception("This is a module, not a script, can not run directly.")
