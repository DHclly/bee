# Bee

**Bee**, a lightweight LLM API proxy.

![bee](images/bee-200.png)


## 介绍

在大模型火热的今天，LLM + RAG 技术做知识库越来越火热，在项目开发中，往往会采用大模型,向量模型，重排模型的组合通过 LLM + RAG 实现智能知识库。

其中，向量模型用于对文本进行向量化，重排模型用于对向量进行排序，LLM 用于对文本进行语言模型预测，通过这三者的组合，实现基于知识库智能问答功能。

目前大多数实现中，对接的这三个模型的接口规范都是采用 OpenAI API的接口风格（当然，OpenAI 没有提供重排接口文档，因此更多是采用类似的接口规范，比如Gpustack的定义就很OpenAI），但是实际项目中，各个平台或者项目上部署的私有模型接口规范各种各样，因此，需要通过一个适配器把各种接口适配为统一的OpenAI API接口规范，才能实现统一的接口调用。

Bee 就是这样一个适配器，它可以把各种接口规范的模型适配为统一的OpenAI API接口规范，通过统一的接口调用，实现对接各个平台的私有模型。

Bee 提供了一个快速实现接口适配的方案，把适配过程简化为了Python 字典数据转换，通过创建一个新的适配器，就可以快速把当前不规范的平台接口转换为统一的OpenAI API接口规范，提供给支持OpenAI API 接口的客户端使用，比如 lobe chat。

## 接口规范文档

上层的接口规范参考了 OpenAI API的接口规范和Gpustack的接口规范，文档地址如下：

- OpenAI 问答对话接口API文档：[/v1/chat/completions](https://platform.openai.com/docs/api-reference/chat/create)
- OpenAI 向量嵌入接口API文档：[/v1/embeddings](https://platform.openai.com/docs/api-reference/embeddings)
- Gpustack API文档：[API Reference - GPUStack](https://docs.gpustack.ai/latest/api-reference/)

