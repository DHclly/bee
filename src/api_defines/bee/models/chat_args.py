from typing import Literal

from pydantic import BaseModel, Field, field_validator


# 文本内容单元
class ChatMessageTextContentModel(BaseModel):
    """
    多模态消息中的文本内容单元
    """
    type: Literal["text"] = Field(
        "text",
        description="内容类型：文本"
    )
    text: str = Field(
        ...,
        description="文本内容",
        min_length=1
    )
    
# 图像 URL 对象
class ChatMessageImageUrlModel(BaseModel):
    """
    图像输入信息
    支持 URL 或 base64 编码数据
    """
    url: str = Field(
        ...,
        description="图像 URL 或 base64 编码数据（data:image/jpeg;base64,xxx）",
        examples=[
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBD...",
            "https://example.com/image.jpg"
        ]
    )

class ChatMessageImageContentModel(BaseModel):
    """
    多模态消息中的图像内容单元
    """
    type: Literal["image_url"] = Field(
        "image_url",
        description="内容类型：图像"
    )
    image_url: ChatMessageImageUrlModel = Field(
        ...,
        description="图像信息"
    )

# 音频输入对象（Qwen-Omni）
class ChatMessageInputAudioModel(BaseModel):
    """
    音频输入信息（Qwen-Omni 模型）
    """
    data: str = Field(
        ...,
        description="base64 编码的音频数据"
    )
    format: Literal["mp3", "wav"] = Field(
        ...,
        description="音频格式"
    )

class ChatMessageAudioContentModel(BaseModel):
    """
    多模态消息中的音频内容单元（Qwen-Omni）
    """
    type: Literal["input_audio"] = Field(
        "input_audio",
        description="内容类型：音频输入"
    )
    input_audio: ChatMessageInputAudioModel = Field(
        ...,
        description="音频信息"
    )

# 视频输入（图片列表形式）
class ChatMessageVideoContentModel(BaseModel):
    """
    多模态消息中的视频内容单元（图片列表形式）
    """
    type: Literal["video"] = Field(
        "video",
        description="内容类型：视频（图片列表）"
    )
    video: list[str] = Field(
        ...,
        description="视频帧图片 URL 列表",
        min_length=1
    )


# 视频文件输入
class ChatMessageVideoUrlModel(BaseModel):
    """
    视频文件输入信息
    """
    url: str = Field(
        ...,
        description="视频文件 URL"
    )


class ChatMessageVideoUrlContentModel(BaseModel):
    """
    多模态消息中的视频文件内容单元
    """
    type: Literal["video_url"] = Field(
        "video_url",
        description="内容类型：视频文件"
    )
    video_url: ChatMessageVideoUrlModel = Field(
        ...,
        description="视频文件信息"
    )
    
class ChatSystemMessageModel(BaseModel):
    """
    系统消息对象（System Message）

    用于设定模型的行为、角色或上下文目标。
    在 messages 列表中，系统消息应放在第一位。

    示例：
    ```json
    {
        "role": "system",
        "content": "你是一个 helpful assistant."
    }
    ```
    """
    role: Literal["system"] = Field(
        "system",
        description="消息角色，系统消息固定为 'system'"
    )
    content: str | ChatMessageTextContentModel = Field(
        ...,
        description="系统消息内容，可以是字符串（纯文本）或多模态文本内容列表"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if isinstance(value, list):
            if not value:
                raise ValueError("content 列表不能为空")
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("content 字符串不能为空或仅空白字符")
        return value

class ChatUserMessageModel(BaseModel):
    """
    用户消息对象（User Message）

    用户发送给模型的消息，支持纯文本和多模态输入。

    ### 使用说明
    - **纯文本**：`content` 为字符串
    - **多模态**：`content` 为对象列表，如 `[{"type": "text", "text": "描述这张图"}, {"type": "image_url", "image_url": {"url": "https://..."}}]`

    ### 支持的多模态类型
    | type | 模型支持 | 说明 |
    |------|----------|------|
    | `text` | 所有模型 | 文本输入 |
    | `image_url` | Qwen-VL, QVQ, Qwen-Omni | 图像输入 |
    | `input_audio` | Qwen-Omni | 音频输入 |
    | `video` | Qwen-VL, QVQ, Qwen-Omni | 图片列表形式的视频 |
    | `video_url` | Qwen-VL（部分）, QVQ, Qwen-Omni | 视频文件输入 |

    > ⚠️ 注意：音频和视频文件输入需使用 Qwen-Omni 或特定 Qwen-VL 模型。
    """
    role: Literal["user"] = Field(
        "user",
        description="消息角色，用户消息固定为 'user'"
    )
    content: str | list[ChatMessageTextContentModel | ChatMessageImageContentModel | ChatMessageAudioContentModel | ChatMessageVideoContentModel | ChatMessageVideoUrlContentModel] = Field(
        ...,
        description="""
        消息内容：
        - 纯文本时为字符串
        - 多模态时为内容单元列表（支持文本、图像、音频、视频）
        """
    )
    
    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("纯文本 content 不能为空")
        elif isinstance(value, list):
            if not value:
                raise ValueError("content 列表不能为空")
        else:
            raise ValueError("content 必须是字符串或对象列表")
        return value

class ChatMessageFunctionCallModel(BaseModel):
    """
    需要被调用的函数信息。
    """
    name: str = Field(..., description="需要被调用的函数名")
    arguments: str = Field(..., description="需要输入到工具中的参数，为JSON字符串")

class ChatMessageToolCallModel(BaseModel):
    """
    模型回复中要调用的工具和参数。
    """
    id: str = Field(..., description="本次工具响应的ID")
    type: Literal["function"] = Field(..., description="工具的类型，当前只支持function")
    function: ChatMessageFunctionCallModel = Field(..., description="需要被调用的函数")
    index: int | None = Field(None, description="工具信息在tool_calls列表中的索引")

class ChatAssistantMessageModel(BaseModel):
    """
    助手消息对象（Assistant Message）

    模型对用户消息的回复。

    示例：
    ```json
    {
        "role": "assistant",
        "content": "这是助手的消息内容。",
        "partial": false,
        "tool_calls": [
            {
                "id": "1",
                "type": "function",
                "function": {
                    "name": "example_function",
                    "arguments": "{\"param\": \"value\"}"
                },
                "index": 0
            }
        ]
    }
    ```
    """
    role: Literal["assistant"] = Field(
        "assistant",
        description="消息角色，助手消息固定为 'assistant'"
    )
    content: str | ChatMessageTextContentModel = Field(
        ...,
        description="助手消息内容，可以是字符串（纯文本）或多模态文本内容列表"
    )
    partial: bool | None = Field(
        None,
        description="是否开启Partial Mode。使用方法请参考前缀续写。"
    )
    tool_calls: list[ChatMessageToolCallModel] | None = Field(
        None,
        description="模型回复的要调用的工具和调用工具时需要的参数。包含一个或多个对象。由上一轮模型响应的tool_calls字段获得。"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if isinstance(value, list):
            if not value:
                raise ValueError("content 列表不能为空")
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("content 字符串不能为空或仅空白字符")
        return value

class ChatToolMessageModel(BaseModel):
    """
    工具消息对象（Tool Message）

    表示工具（Function/Tool）执行完成后返回的结果消息，由开发者或系统生成，
    用于将工具执行结果返回给模型，以便模型继续推理和生成最终回复。

    在对话流程中，工具消息应与对应的工具调用（tool_call）通过 `tool_call_id` 关联。

    示例：
    ```json
    {
        "role": "tool",
        "content": "天气查询结果：北京，晴，28°C",
        "tool_call_id": "call_123456789"
    }
    ```
    """
    role: Literal["tool"] = Field(
        "tool",
        description="消息角色，工具消息固定为 'tool'"
    )
    content: str | ChatMessageTextContentModel = Field(
        ...,
        description="工具执行结果内容，可以是字符串（纯文本）或多模态文本内容列表"
    )
    tool_call_id: str | None = Field(
        None,
        description="关联的工具调用ID，对应 assistant 消息中 tool_calls[n].id。"
                    "用于将工具执行结果与具体的工具调用进行绑定。"
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value):
        if isinstance(value, list):
            if not value:
                raise ValueError("content 列表不能为空")
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("content 字符串不能为空或仅空白字符")
        return value


class ChatStreamOptionsModel(BaseModel):
    """
    流式输出选项模型
    """
    include_usage: bool = Field(
        True,
        description="是否在流式输出的最后一行包含 token 使用情况。仅在 stream=True 时生效。"
    )
    
class ChatArgs(BaseModel):
    """
    聊天模型请求参数模型（兼容文本与多模态模型）。

    支持 Qwen 系列模型，包括：
    - 纯文本模型：如 qwen2.5-7b-instruct
    - 多模态模型：如 qwen2-vl-7b-instruct
    """
    model: str = Field(
        ...,
        description="要调用的模型名称,如：qwen2.5-7b-instruct",
        examples=["qwen2.5-7b-instruct", "qwen2-vl-7b-instruct"]
    )
    messages: list[ChatSystemMessageModel | ChatUserMessageModel | ChatAssistantMessageModel | ChatToolMessageModel] = Field(
        ...,
        description="由历史对话组成的消息列表。按时间顺序排列",
        min_length=1,
        examples=["""[
    {
        "role": "system",
        "content": "你是一位超级厉害的导游，精通中国各个城市信息"
    },
    {
        "role": "user",
        "content": "北上广是哪里"
    }
    ]"""]
    )
    stream: bool | None = Field(
        default=False,
        description="是否启用流式输出， 默认值为 false。false：模型生成完所有内容后一次性返回结果。true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。您需要实时地逐个读取这些片段以获得完整的结果。",
        examples=[True]
    )
    stream_options: ChatStreamOptionsModel | None = Field(
        None,
        description="""流式输出选项。当 stream=true 时，可设置此参数控制流输出行为。
示例：
```json
{"stream_options": {"include_usage": true}}
```

- `include_usage: true`：在流的最后一行输出 token 使用统计
- `include_usage: false` 或不设置：不输出 token 使用情况

> 注意：此参数仅在 `stream=true` 时生效。
        """)
    temperature: float | None = Field(
        1.0,
        ge=0.0,
        le=2.0,
        description="采样温度，控制模型生成文本的多样性。temperature越高，生成的文本更多样，反之，生成的文本更确定。由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。",
        examples=[0.8]
    )
    top_p: float | None = Field(
        1.0,
        ge=0.0,
        le=1.0,
        description="核采样的概率阈值，控制模型生成文本的多样性。top_p越高，生成的文本更多样。反之，生成的文本更确定。由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。",
        examples=[0.95]
    )
    max_tokens: int | None = Field(
        default=None,
        ge=1,
        description="最大生成 token 数",
        examples=[8192]
    )
    presence_penalty: float | None = Field(
        default=None,
        ge=-2.0,
        le=2.0,
        description="控制生成文本的重复度。取值范围：[-2.0, 2.0]。正数减少重复（鼓励新话题），负数增加重复。适用于控制创造性或一致性。",
        examples=[0.0]
    )
    frequency_penalty: float | None = Field(
        default=None,
        ge=-2.0,
        le=2.0,
        description="控制生成文本中token的重复频率。取值范围：[-2.0, 2.0]。正数会根据token已出现的频率进行惩罚，减少重复用词；负数则鼓励重复。适用于避免机械重复或增强一致性。",
        examples=[0.0]
    )
    stop: None | str | list[str] = Field(
        None,
        description="使用stop参数后，当模型生成的文本即将包含指定的字符串或token_id时，将自动停止生成。您可以在stop参数中传入敏感词来控制模型的输出。stop为array类型时，不可以将token_id和字符串同时作为元素输入，比如不可以指定stop为[\"你好\",104307]。",
        examples=[None]
    )
    seed: int | None = Field(
        default=None,
        ge=0,
        le=2147483647,
        description="设置 seed 使文本生成更具确定性。传入相同的 seed 值且其他参数不变时，模型将尽可能返回相同结果。取值范围：0 到 2^31 - 1。",
        examples=[None]
    )
    