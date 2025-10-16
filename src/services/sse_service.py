
from services import uuid_service


def get_sse_message(
    message: str
) -> str:
    """
    生成一条符合 Server-Sent Events (SSE) 协议标准的消息字符串，只支持 data 字段。

    Returns:
        str: 格式化的 SSE 消息字符串，包含指定字段并以 ``\\n\\n`` 结尾。
             例如：

                data: Hello
    Note:
        - 每条 SSE 消息必须以两个换行符 ``\\n\\n`` 结束。
    """
    if message is None:
        message =""

    data_part = f"data: {message}\n"
    message_body = f"{data_part}\n"
    return message_body