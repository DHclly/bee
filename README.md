# Bee

**Bee**, a lightweight LLM API proxy.

![bee](images/bee-200.png)

## 介绍

在大模型火热的今天，LLM + RAG 技术做知识库越来越火热，在项目开发中，往往会采用大模型,向量模型，重排模型的组合通过 LLM + RAG 实现智能知识库。

其中，向量模型用于对文本进行向量化，重排模型用于对向量进行排序，LLM 用于对文本进行语言模型预测，通过这三者的组合，实现基于知识库智能问答功能。

目前大多数实现中，对接的这三个模型的接口规范都是采用 OpenAI API 的接口风格（当然，OpenAI 没有提供重排接口文档，因此更多是采用类似的接口规范，比如 Gpustack 的定义就很 OpenAI），但是实际项目中，各个平台或者项目上部署的私有模型接口规范各种各样，因此，需要通过一个适配器把各种接口适配为统一的 OpenAI API 接口规范，才能实现统一的接口调用。

Bee 就是这样一个适配器，它可以把各种接口规范的模型适配为统一的 OpenAI API 接口规范，通过统一的接口调用，实现对接各个平台的私有模型。

Bee 提供了一个快速实现接口适配的方案，把适配过程简化为了 Python 字典数据转换，通过创建一个新的适配器，就可以快速把当前不规范的平台接口转换为统一的 OpenAI API 接口规范，提供给支持 OpenAI API 接口的客户端使用，比如 lobe chat。

## 接口规范文档

上层的接口规范参考了 OpenAI API 的接口规范和 Gpustack 的接口规范，文档地址如下：

- OpenAI 问答对话接口 API 文档：[/v1/chat/completions](https://platform.openai.com/docs/api-reference/chat/create)
- OpenAI 向量嵌入接口 API 文档：[/v1/embeddings](https://platform.openai.com/docs/api-reference/embeddings)
- Gpustack API 文档：[API Reference - GPUStack](https://docs.gpustack.ai/latest/api-reference/)

## 可配置的环境变量

| 环境变量名称         | 默认值                                 | 说明                                                      |
| -------------------- | -------------------------------------- | --------------------------------------------------------- |
| `bee_workers`        | `1`                                    | uvicorn 的 worker 数量，高并发场景建议设为 CPU 核心数     |
| `bee_auth_type`      | `Bearer`                               | 认证类型，用于接口鉴权（如 Bearer、APIKey 等）            |
| `bee_auth_key`       | `sk_123`                               | 认证密钥，用于验证请求合法性                              |
| `bee_embeddings_url` | `http://localhost/v1/embeddings`       | Embeddings 模型服务的地址（用于向量生成）                 |
| `bee_rerank_url`     | `http://localhost/v1/rerank`           | Rerank 模型服务的地址（用于结果重排序）                   |
| `bee_chat_url`       | `http://localhost/v1/chat/completions` | Chat 模型服务的地址（用于对话生成）                       |
| `bee_provider_type`  | `gpustack`                             | 后端模型提供方类型（如 gpustack、ollama、vllm 等）        |
| `bee_show_swagger`   | `true`                                 | 是否显示 Swagger UI 文档（`true`/`false`）                |
| `bee_show_redoc`     | `true`                                 | 是否显示 ReDoc 文档（`true`/`false`）                     |
| `bee_log_level`      | `info`                                 | 日志输出级别（如 `debug`, `info`, `warning`, `error` 等） |

如果只是 url 非标准，则 provider 默认用 gpustack 类型，填写对应的url即可。
