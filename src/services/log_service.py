"""
# 日志模块，在【入口】 python 文件中添加以下代码
from services.log_service import get_logger
logger=get_logger()

# 在其他 python 文件中调用
from services.log_service import logger

# 支持的方法：

# 默认的方法
logger.info("hi")
logger.error("hi")
logger.warning("hi")

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
from typing import Any, Union, Optional, Tuple
from services import env_service


class LogServiceLogger(logging.Logger):
    """自定义 Logger 类型，用于 IDE 类型提示（仅在类型检查时生效）"""

    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        """
        初始化自定义日志记录器。

        :param name: 日志记录器名称
        :param level: 日志级别，默认为 NOTSET
        """
        super().__init__(name, level)
        self.diff_id: int = 1
        self.diff_last_time: float = 0

    def dump_data(self, raw_data: Any, truncate_length: int = 100) -> None:
        """
        用于解析数据，支持普通文本、数字、对象、列表、字典等。
        字典和对象只解析一层，其余部分以字符串形式截断显示。
        如果数据转换后长度超过指定值，则自动截断。

        :param raw_data: 要记录的原始数据（任意类型）
        :param truncate_length: 截断长度，默认 100 字符
        """
        data = deepcopy(raw_data)
        if isinstance(data, str):
            data = self.truncate_data(data, truncate_length)
        elif isinstance(data, (int, float)):
            data = self.truncate_data(data, truncate_length)
        elif isinstance(data, bool):
            pass
        elif isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.truncate_data(value, truncate_length)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                data[idx] = self.truncate_data(item, truncate_length)
        elif isinstance(data, tuple):
            data = tuple(self.truncate_data(item, truncate_length) for item in data)
        elif isinstance(data, object) and hasattr(data, '__dict__'):
            self.dump_data(data.__dict__, truncate_length)
            return
        else:
            pass
        self.info(data, stacklevel=3)

    def with_time(self, message: str) -> None:
        """
        记录带有时间差的日志信息，底层是info级别。
        每次调用会计算与上一次调用之间的时间间隔（毫秒），并输出到日志中。

        :param message: 要记录的消息
        """
        diff_time = 0.000
        current_time = time.time()

        if self.diff_last_time != 0:
            diff_time = round(current_time - self.diff_last_time, 3)
        self.info(f"[step {self.diff_id} cost {diff_time:.3f}s]=>{message}", stacklevel=3)
        self.diff_id = self.diff_id + 1 if self.diff_id < 999999999 else 1
        self.diff_last_time = current_time

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """
        重写 error 方法，自动添加堆栈信息。

        :param msg: 错误消息
        :param args: 额外参数
        :param kwargs: 额外关键字参数
        """
        # 自动添加
        if 'stack_info' not in kwargs:
            kwargs['stack_info'] = True
        if 'stacklevel' not in kwargs:
            kwargs['stacklevel'] = 2  # 指向调用 error() 的那一行
        msg = f"发生错误\n----------------------------------------------------\n{msg}\n"
        super().error(msg, *args, **kwargs)

    def truncate_data(self, param_value: Any, truncate_length: int = 100) -> str:
        """
        截断字符串或数字。

        :param param_value: 需要截断的参数值
        :param truncate_length: 截断长度，默认为100
        :return: 截断后的字符串
        """
        if isinstance(param_value, bytes):
            str_value = param_value.decode('utf-8', errors='ignore')
        else:
            str_value = str(param_value)

        if len(str_value) > truncate_length:
            str_value = f"{str_value[:truncate_length]}..."
        return str_value

logger = None

def _get_log_level() -> int:
    """
    获取日志级别。

    :return: logging 模块中的日志级别常量
    """
    level = env_service.get_log_level()
    if level == "debug":
        return logging.DEBUG

    if level == "info":
        return logging.INFO

    if level == "warning":
        return logging.WARNING

    return logging.INFO


def _get_server_name_and_path(main_path: str) -> Tuple[str, str]:
    """
    根据主路径获取服务器名称和服务器路径。

    :param main_path: 主路径
    :return: 服务器名称和服务器路径的元组
    """
    path_parts = main_path.split(os.sep)
    path_len = len(path_parts)
    server_name = path_parts[-2] if path_len > 2 else "app"
    server_path = os.sep.join(path_parts[:-1]) if path_len > 2 else "/"
    return server_name, server_path


def _get_main_path() -> str:
    """
    获取调用者模块的绝对路径。

    :return: 调用者模块的绝对路径
    """
    # 获取当前栈帧
    current_frame = inspect.currentframe()
    try:
        # 回溯到调用者的栈帧
        if current_frame is not None:
            current_frame = current_frame.f_back

        if current_frame is not None:
            current_frame = current_frame.f_back

        if current_frame is not None:
            module = inspect.getmodule(current_frame)
            if module and hasattr(module, '__file__') and module.__file__ is not None:
                return os.path.abspath(module.__file__)
    finally:
        # 删除帧对象以避免循环引用
        del current_frame
    return ""


def get_logger(print_start: bool = True, server_name: str = "", log_base_path: str = "") -> LogServiceLogger:
    """
    获取一个自定义的日志记录器。

    :param print_start: 是否在日志中打印服务启动信息
    :param server_name: 服务名，默认会以当前日志的目录路径倒数第二个文件夹名称作为服务名，
                        如当前文件路径为 /app/bee/services/log_service.py 则服务名为 bee
    :param log_base_path: 日志存储的基础路径，指定后会在指定目录下创建一个 logs 文件夹存放日志，
                          默认以获取服务名目录下的 logs 文件夹作为日志存储路径
    :return: 返回一个自定义的日志记录器
    """
    global logger

    if logger is not None:
        return logger

    # 注册自定义 logger 类
    logging.setLoggerClass(LogServiceLogger)

    # 获取主路径
    main_path = _get_main_path()

    inner_server_name: str
    inner_log_base_path: str
    inner_server_name, inner_log_base_path = _get_server_name_and_path(main_path)

    if server_name != "":
        inner_server_name = server_name

    if log_base_path != "":
        inner_log_base_path = log_base_path

    # 定义日志格式
    log_formatter = logging.Formatter(
        '[%(name)s][%(asctime)s][%(levelname)s][%(filename)s line:%(lineno)s]:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 创建日志文件路径
    log_folder_path = os.path.join(inner_log_base_path, "logs")
    log_file_path = os.path.join(log_folder_path, f"{inner_server_name}.log")
    log_level = _get_log_level()

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
    inner_logger = LogServiceLogger(inner_server_name)
    # 禁用日志传播
    inner_logger.propagate = False
    inner_logger.setLevel(log_level)
    inner_logger.addHandler(console_handler)
    inner_logger.addHandler(file_handler)

    # 设置全局 logger
    logger = inner_logger

    # 打印服务启动信息
    if print_start:
        inner_logger.info("-----------------------------")
        inner_logger.info("-----------------------------")
        inner_logger.info(f" {server_name} service start ")
        inner_logger.info("-----------------------------")
        inner_logger.info("-----------------------------")

    return inner_logger


def test_log() -> None:
    """
    测试日志功能的示例函数。
    """
    logger = get_logger()
    # 默认的方法
    logger.info("--------------------------")
    logger.info("info message")
    logger.info("--------------------------")
    logger.error("error message")
    logger.info("--------------------------")
    logger.warning("warning message")
    logger.info("--------------------------")
    # 解析对象第一层数据，并对每个值进行截断
    logger.dump_data({"key": "value", "list": [1, 2, 3]}, truncate_length=3)
    logger.info("--------------------------")
    # 记录带有时间差的日志信息
    import time
    logger.with_time("This message has a time stamp,sleep 1s")
    time.sleep(1)
    logger.with_time("This message has a time stamp2,sleep 0.5s")
    time.sleep(0.5)
    logger.with_time("This message has a time stamp2")
    logger.info("--------------------------")


if __name__ == '__main__':
    raise Exception("This is a module, not a script, can not run directly.")