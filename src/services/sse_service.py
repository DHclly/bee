
from services import uuid_service


def get_sse_message(
    message: str,
    event: str | None = None
) -> str:
    """
    生成一条符合 Server-Sent Events (SSE) 协议标准的消息字符串。

    Args:
        message: data 字段内容
        event: 可选的事件名，传入时会额外输出 ``event: <name>`` 行

    Returns:
        str: 格式化的 SSE 消息字符串，以 ``\\n\\n`` 结尾。

    Note:
        - 每条 SSE 消息必须以两个换行符 ``\\n\\n`` 结束。
    """
    if message is None:
        message =""

    event_part = f"event: {event}\n" if event else ""
    data_part = f"data: {message}\n"
    message_body = f"{event_part}{data_part}\n"
    return message_body