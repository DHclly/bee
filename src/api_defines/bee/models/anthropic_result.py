from pydantic import BaseModel, Field


class AnthropicUsageModel(BaseModel):
    """
    Anthropic token 使用情况
    """
    input_tokens: int | None = Field(0, description="输入 token 数")
    output_tokens: int | None = Field(0, description="输出 token 数")


class AnthropicTextBlock(BaseModel):
    """
    Anthropic 文本内容块
    """
    type: str = Field("text", description="内容类型")
    text: str = Field("", description="文本内容")


class AnthropicThinkingBlock(BaseModel):
    """
    Anthropic 思考内容块
    """
    type: str = Field("thinking", description="内容类型")
    thinking: str = Field("", description="思考内容")
    signature: str | None = Field(None, description="思考签名")


class AnthropicToolUseBlock(BaseModel):
    """
    Anthropic 工具调用内容块
    """
    type: str = Field("tool_use", description="内容类型")
    id: str = Field("", description="工具调用 ID")
    name: str = Field("", description="工具名称")
    input: dict = Field(default_factory=dict, description="工具入参")


class AnthropicResult(BaseModel):
    """
    Anthropic Messages API 非流式结果
    """
    id: str = Field("", description="消息 ID")
    type: str = Field("message", description="对象类型")
    role: str = Field("assistant", description="消息角色")
    model: str = Field("", description="模型名称")
    stop_reason: str | None = Field(None, description="停止原因")
    stop_sequence: str | None = Field(None, description="触发的停止序列")
    content: list[
        AnthropicTextBlock | AnthropicThinkingBlock | AnthropicToolUseBlock
    ] = Field(default_factory=list, description="内容块列表")
    usage: AnthropicUsageModel | None = Field(None, description="token 使用情况")


class AnthropicStreamChunkResult(BaseModel):
    """
    Anthropic Messages API 流式事件
    """
    type: str = Field("", description="事件类型，如 content_block_delta、message_delta")
    index: int | None = Field(None, description="内容块索引")
    delta: dict | None = Field(None, description="增量数据")
    content_block: dict | None = Field(None, description="内容块起始数据")
    message: dict | None = Field(None, description="message_start 事件中的消息信息")
    usage: AnthropicUsageModel | None = Field(None, description="token 使用情况")
