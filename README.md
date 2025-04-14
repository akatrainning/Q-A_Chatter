# *SecuriAI* **安鉴无界**
本项目旨在利用检索增强生成（RAG）模型构建安全法律体系智能问答系统，用于实现法律法规、司法案例及原则性法理知识的高效检索、准确匹配与专业性答案生成，并适用于国家安全与个人数据保护等专业场景和普法场景。通过本模型，您可进行私有化部署与定制化法律助手开发，满足政府机构、企业和个人用户差异化需求。
 ## 🥰如何构建您的私人问答助手？ ##
 ### 本项目需要： ###
     获取Qwen API Key 
     安装LlamaIndex
     安装python3
     获取Zilliz Cloud账号
     virtualenv虚拟环境（可选）
### 步骤一 配置Qwen API key ###
项目使用通义千问作为底层大模型，开始搭建前，请在[config.yaml](./cfgs/config.yaml)文件中配置Qwen API key(格式类似于sk-xxxxxxxx)。如果没有，请参考[通义千问](https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api) 官方文档获取。参考配置如下：

    llm:
      name: "qwen-turbo-2024-09-19"
      temperature: 0.7
      api_key: "sk-xxxxxxxx"
### 步骤二 获取Zilliz Cloud的配置信息 ###
> ​Zilliz Cloud Pipelines 是 Zilliz 提供的一项服务，旨在简化非结构化数据（如文本、文档和图像）的处理流程，将其转换为可搜索的向量集合。该服务直接内置支持主流嵌入模型（如 OpenAI、Cohere、Hugging Face 等），自动完成向量化过程，无需自己部署、调用嵌入模型。与本地部署相比，Zilliz Cloud Pipelines服务提供了更好的伸缩弹性，免去了维护生产环境中复杂组件的麻烦，其召回质量会随着云上功能的迭代持续更新优化，并且支持召回方案的个性化配置。

注册[Zilliz Cloud](https://cloud.zilliz.com/signup?utm_source=partner&utm_medium=referral&utm_campaign=2024-01-18_product_zcp-demos_github&utm_content=history-rag)账号，获取相应project配置。您可以参考[这里](https://github.com/milvus-io/bootcamp/blob/master/bootcamp/RAG/zilliz_pipeline_rag.ipynb)了解更加详细的使用教程。
[![weibo-logo]](http://weibo.com/linpiaochen)
      
