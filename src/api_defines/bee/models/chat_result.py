from typing import Literal

from pydantic import BaseModel, Field


class ChatChoiceDeltaModel(BaseModel):
    """
    流式输出中 delta 的内容结构
    """
    role: str | None = Field(
        None , 
        description="角色")
    content: str | None = Field(
        None ,
        description="回复内容")
    reasoning_content: str | None = Field(
        None ,
        description="思考回复内容")


class ChatChoiceModel(BaseModel):
    """
    聊天选择项模型（非流式）
    """
    
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"] | None = Field(
    None,
    description=(
        """模型停止生成 token 的原因。取值含义如下：
- `null`：仍在生成中，尚未结束；
- `stop`：模型到达自然结束点或触发了请求中指定的停止序列（stop sequence）；
- `length`：生成内容达到请求中指定的最大 token 数限制，被截断；
- `content_filter`：因内容安全过滤机制触发，部分内容被屏蔽或省略；
- `tool_calls`：模型调用了工具（tool）；
"""
    )
)
    index: int | None = Field(
        0, 
        description="消息索引编号")
    
    message: ChatChoiceDeltaModel | None=Field(
        None, 
        description="非流式时候返回的消息体")
    
class ChatStreamChoiceModel(BaseModel):
    """
    聊天选择项模型（流式）
    """
    
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"] | None = Field(
    None,
    description=(
        """模型停止生成 token 的原因。取值含义如下：
- `null`：仍在生成中，尚未结束；
- `stop`：模型到达自然结束点或触发了请求中指定的停止序列（stop sequence）；
- `length`：生成内容达到请求中指定的最大 token 数限制，被截断；
- `content_filter`：因内容安全过滤机制触发，部分内容被屏蔽或省略；
- `tool_calls`：模型调用了工具（tool）；
"""
    )
)
    index: int | None = Field(
        0, 
        description="消息索引编号")
    
    delta: ChatChoiceDeltaModel | None=Field(
        None, 
        description="流式时候返回的消息体")

class ChatPromptTokensDetailsModel(BaseModel):
    """
    提示词 token 详细信息
    """
    cached_tokens: int | None = Field(
        0, 
        description="缓存中命中的 token 数")

class ChatCompletionTokensDetailsModel(BaseModel):
    """
    生成 token 详细信息
    """
    accepted_prediction_tokens: int | None = Field(
        0, 
        description="接受的推测 token 数")
    rejected_prediction_tokens: int | None = Field(
        0, 
        description="拒绝的推测 token 数")
    reasoning_tokens: int | None = Field(
        0, 
        description="推理过程中消耗的 token 数")

class ChatUsageModel(BaseModel):
    """
    token 使用情况模型（包含性能指标）
    """
    prompt_tokens: int | None = Field(
        0, 
        description="输入 prompt 的 token 数")
    completion_tokens: int | None = Field(
        0, 
        description="生成内容的 token 数")
    total_tokens: int | None = Field(
        0, 
        description="总 token 数")

    # 细节
    prompt_tokens_details: ChatPromptTokensDetailsModel | None = Field(
        None, 
        description="输入 token 详细信息"
    )
    completion_tokens_details: ChatCompletionTokensDetailsModel | None = Field(
        None, 
        description="生成 token 详细信息"
    )

    # 推测解码相关
    draft_tokens: int | None = Field(
        0, 
        description="草稿阶段生成的 token 数")
    draft_tokens_acceptance: float | None = Field(
        0.0, 
        description="草稿 token 接受率")

    # 性能指标（可选）
    prompt_tokens_per_second: float | None = Field(
        0.0, 
        description="每秒输入 token 数"
    )
    time_per_output_token_ms: float | None = Field(
        0, 
        description="每个输出 token 的平均耗时（毫秒）"
    )
    time_to_first_token_ms: float | None = Field(
        0, 
        description="首 token 延迟（毫秒）"
    )
    tokens_per_second: float | None = Field(
        0, 
        description="每秒输出 token 数"
    )

class ChatResult(BaseModel):
    """
    非流式聊天补全结果（完整响应）
    """
    
    id: str = Field(
        ..., 
        description="会话 ID")
    object: str | None = Field(
        "chat.completion", 
        description="对象类型")
    created: int = Field(
        ..., 
        description="创建时间戳（Unix 时间）"
        )
    model: str = Field(
        ..., 
        description="使用的模型名称")
    choices: list[ChatChoiceModel] = Field(
        ..., 
        description="生成的回复列表")
    usage: ChatUsageModel | None = Field(
        None, 
        description="token 使用情况及性能指标",
        examples=[None])
    
    
class ChatStreamChunkResult(BaseModel):
    """
    流式聊天接口返回的单个 chunk 数据（对应一行 `data: {...}`）。

    用于 `text/event-stream` 响应，兼容 OpenAI 和 Qwen 流式格式。
    """
    id: str = Field(
        ..., 
        description="会话 ID")
    
    object: str | None = Field(
        "chat.completion.chunk",
        description="对象类型，流式输出固定为 'chat.completion.chunk'")
    created: int | None = Field(
        ...,
        description="生成时间戳（Unix 时间，秒）",
    )
    model: str | None = Field(
        ...,
        description="实际使用的模型名称",
    )
    choices: list[ChatStreamChoiceModel] = Field(
        ...,
        description="生成结果的候选列表，通常只包含一个元素"
    )

    usage: ChatUsageModel | None = Field(
        None, 
        description="token 使用情况及性能指标",
        examples=[None])
    