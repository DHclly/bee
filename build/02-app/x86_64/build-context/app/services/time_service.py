import time


def get_current_timestamp_int()->int:
    # 获取当前时间戳（浮点数，包含小数部分表示毫秒）
    timestamp = time.time()
    return int(timestamp)