# provider 适配说明

此provider 为模板

## 适配说明

- 适配向量：否
- 适配重排：否
- 适配问答对话：否
- 适配 Anthropic 问答对话：否

## 适配详情

## 适配向量

适配原始请求参数:

```

```

适配原始返回参数：

```

```

## 适配重排

适配原始请求参数:

```

```

适配原始返回参数：

```

```

## 适配问答对话

适配原始请求参数:

```

```

适配原始返回参数：

```

```

## 适配 Anthropic 问答对话

适配原始请求参数:

```
POST /v1/messages
{
    "model": "claude-opus-5-5",
    "max_tokens": 4096,
    "system": "你是一位助手",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        }
    ]
}
```

适配原始返回参数：

```
{
    "id": "msg_xxx",
    "type": "message",
    "role": "assistant",
    "model": "claude-opus-5-5",
    "stop_reason": "end_turn",
    "content": [
        {
            "type": "text",
            "text": "你好，有什么可以帮你？"
        }
    ],
    "usage": {
        "input_tokens": 10,
        "output_tokens": 20
    }
}
```

适配原始流式返回参数（SSE）：

```
event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"你好"}}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn"},"usage":{"output_tokens":20}}

event: message_stop
data: {"type":"message_stop"}
```
