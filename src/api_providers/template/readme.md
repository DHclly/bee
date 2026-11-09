# provider 适配说明

此 provider 为 Anthropic（Claude）Messages API 适配模板

## 适配说明

- 适配向量：否
- 适配重排：否
- 适配问答对话：是

## 适配详情

## 适配向量

未适配

## 适配重排

未适配

## 适配问答对话

适配原始请求参数:

```
POST /v1/messages
{
  "model": "claude-opus-5-5",
  "max_tokens": 4096,
  "system": "你是一位助手",
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}
```

适配原始返回参数（非流式）：

```
{
  "id": "msg_xxx",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-5-5",
  "stop_reason": "end_turn",
  "content": [
    {"type": "thinking", "thinking": "..."},
    {"type": "text", "text": "你好，有什么可以帮你？"}
  ],
  "usage": {"input_tokens": 10, "output_tokens": 20}
}
```

适配原始返回参数（流式 SSE，仅列关键事件）：

```
event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"你好"}}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn"},"usage":{"output_tokens":20}}

event: message_stop
data: {"type":"message_stop"}
```

## 转换说明

- 认证：使用 `x-api-key` 头，附带 `anthropic-version`
- system 消息：抽出合并为 Anthropic 顶层 `system` 字段
- `max_tokens` 为 Anthropic 必填项，未传时默认 8192
- 图片：支持 URL 与 base64（data URI），音频、视频内容块会被忽略
- `stop_reason` 映射：`end_turn`/`stop_sequence` → `stop`，`max_tokens` → `length`，`tool_use` → `tool_calls`，`refusal` → `content_filter`
- 流式：`input_json_delta`（工具参数分片）暂不逐片透传
