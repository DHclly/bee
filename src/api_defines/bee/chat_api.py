
from fastapi.responses import StreamingResponse
from httpx_sse import aconnect_sse

from services.http_service import http_clients
from services.log_service import logger
from services.module_load_service import load_chat_api
from services.sse_service import get_sse_message

from .models.chat_args import ChatArgs as BeeChatArgs,ChatStreamOptionsModel as BeeChatStreamOptionsModel
from .models.chat_result import ChatResult as BeeChatResult
from .models.error_result import APIErrorResult
import asyncio

chat_api=None
chat_api_initialized = False
chat_api_lock = asyncio.Lock()

async def chat(args:BeeChatArgs,token: str)->BeeChatResult | StreamingResponse | APIErrorResult:
    response_error_text=""
    global chat_api, chat_api_initialized
    try:
        if not chat_api_initialized:
            async with chat_api_lock:
                if not chat_api_initialized:
                    chat_api = load_chat_api()
                    await chat_api.init() # type: ignore
                    chat_api_initialized=True
                    
        request_url=await chat_api.get_request_url(args) # type: ignore
        request_headers =await chat_api.get_request_headers(token) # type: ignore
        request_args =await chat_api.get_request_args(pre_process_args(args)) # type: ignore
        client=http_clients.chat_client
        
        logger.info(f"发起问答对话请求,地址:{request_url}\n")
        logger.debug(f"请求头参数：{request_headers}\n")
        logger.debug(f"原始请求参数：{args.model_dump_json()}\n")
        logger.debug(f"修改后请求参数：{request_args}\n")
        
        if args.stream:
            # 定义流式生成器
            async def stream_generator():
                async with aconnect_sse(
                    client,
                    "POST",
                    url=request_url,
                    headers=request_headers,
                    json=request_args,
                ) as event_source:
                    if event_source.response.status_code != 200:
                        msg=(await event_source.response.aread()).decode(encoding="utf-8",errors="ignore")
                        logger.info("请求失败，错误信息："+msg)
                        api_error_json = APIErrorResult(code="000",message=msg).model_dump_json()
                        error_line=get_sse_message(api_error_json)
                        yield error_line
                    else:
                        async for line in event_source.aiter_sse():
                            if line.data is None:
                                continue
                            
                            # [DONE]
                            if line.data=="[DONE]":
                                yield get_sse_message(line.data)
                                logger.debug("停止流式输出\n")
                                continue
                                
                            line_data=line.json()
                            logger.debug(f"原始返回参数：{line_data}\n")
                            new_line_data=await chat_api.get_request_stream_chunk_result(line_data) # type: ignore
                            new_line_data_json=new_line_data.model_dump_json()
                            logger.debug(f"修改后返回参数：{new_line_data_json}\n")
                            new_line=get_sse_message(new_line_data_json)
                            yield new_line
                        
            return StreamingResponse(
                content=stream_generator(),
                status_code=200,
                headers={
                    "proxy-server":"bee"
                    },
                media_type="text/event-stream"
            )
        else:
            response = await client.post(
                url=request_url,
                headers=request_headers,
                json=request_args)
            response_error_text=",响应信息："+response.text
            
            response.raise_for_status()
            result_data = response.json()
            logger.debug(f"原始返回参数：{result_data}\n")
            result =await chat_api.get_request_result(result_data) # type: ignore
            logger.debug(f"修改后返回参数：{result.model_dump_json()}\n")
            logger.info("问答对话请求成功")
            return result
    except Exception as e:
        error_text=f"问答对话请求发生错误，异常类型：{str(type(e))},异常信息：{e} {response_error_text}"
        logger.error(error_text)
        return APIErrorResult(message=error_text)


def pre_process_args(args:BeeChatArgs)->BeeChatArgs:
    if args.stream:
        if args.stream_options is None:
            args.stream_options=BeeChatStreamOptionsModel(include_usage=False)
    return args



