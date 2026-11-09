from typing import Literal

from pydantic import BaseModel, Field


class AnthropicTextContent(BaseModel):
    """
    Anthropic 消息中的文本内容块
    """
    type: Literal["text"] = Field("text", description="内容类型：文本")
    text: str = Field(..., description="文本内容")


class AnthropicImageSource(BaseModel):
    """
    Anthropic 图像来源（base64 或 url）
    """
    type: Literal["base64", "url"] = Field(..., description="来源类型：base64 或 url")
    media_type: str | None = Field(
        None,
        description="媒体类型，base64 时必填，如 image/png、image/jpeg",
        examples=["image/png"]
    )
    data: str | None = Field(None, description="base64 编码的图像数据")
    url: str | None = Field(None, description="图像 URL")


class AnthropicImageContent(BaseModel):
    """
    Anthropic 消息中的图像内容块
    """
    type: Literal["image"] = Field("image", description="内容类型：图像")
    source: AnthropicImageSource = Field(..., description="图像来源")


class AnthropicToolUseContent(BaseModel):
    """
    Anthropic 消息中的工具调用内容块
    """
    type: Literal["tool_use"] = Field("tool_use", description="内容类型：工具调用")
    id: str = Field(..., description="工具调用 ID")
    name: str = Field(..., description="工具名称")
    input: dict = Field(default_factory=dict, description="工具入参")


class AnthropicToolResultContent(BaseModel):
    """
    Anthropic 消息中的工具结果内容块
    """
    type: Literal["tool_result"] = Field("tool_result", description="内容类型：工具结果")
    tool_use_id: str = Field(..., description="对应的工具调用 ID")
    content: str | None = Field(None, description="工具执行结果")


class AnthropicThinkingContent(BaseModel):
    """
    Anthropic 的思考内容块（用于回传历史）
    """
    type: Literal["thinking"] = Field("thinking", description="内容类型：思考")
    thinking: str = Field("", description="思考内容")
    signature: str | None = Field(None, description="思考签名")


class AnthropicMessage(BaseModel):
    """
    Anthropic 消息对象
    """
    role: Literal["user", "assistant"] = Field(..., description="消息角色")
    content: str | list[
        AnthropicTextContent
        | AnthropicImageContent
        | AnthropicToolUseContent
        | AnthropicToolResultContent
        | AnthropicThinkingContent
    ] = Field(..., description="消息内容，字符串或内容块列表")


class AnthropicTool(BaseModel):
    """
    Anthropic 工具定义
    """
    name: str = Field(..., description="工具名称")
    description: str | None = Field(None, description="工具描述")
    input_schema: dict = Field(
        default_factory=lambda: {"type": "object", "properties": {}},
        description="工具入参的 JSON Schema"
    )


class AnthropicArgs(BaseModel):
    """
    Anthropic Messages API 请求参数模型（/v1/messages）
    """
    model: str = Field(
        ...,
        description="要使用的模型名称，如 claude-opus-5-5",
        examples=["claude-opus-5-5"]
    )
    messages: list[AnthropicMessage] = Field(
        ...,
        description="由历史对话组成的消息列表，按时间顺序排列",
        min_length=1
    )
    max_tokens: int = Field(
        ...,
        ge=1,
        description="最大生成 token 数，Anthropic 必填",
        examples=[4096]
    )
    system: str | list[AnthropicTextContent] | None = Field(
        None,
        description="系统提示词，字符串或文本内容块列表"
    )
    stream: bool | None = Field(
        False,
        description="是否启用流式输出"
    )
    temperature: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="采样温度，Anthropic 取值范围 0.0 到 1.0"
    )
    top_p: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="核采样概率阈值"
    )
    top_k: int | None = Field(
        None,
        ge=1,
        description="top-k 采样参数"
    )
    stop_sequences: list[str] | None = Field(
        None,
        description="停止序列列表"
    )
    tools: list[AnthropicTool] | None = Field(
        None,
        description="工具定义列表"
    )
    tool_choice: dict | None = Field(
        None,
        description="工具选择策略，如 {\"type\": \"auto\"}"
    )
    thinking: dict | None = Field(
        None,
        description="思考配置，如 {\"type\": \"adaptive\"}"
    )
