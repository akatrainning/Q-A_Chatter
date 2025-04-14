import argparse
import logging
import sys
import re
import os
import argparse

import requests
from pathlib import Path
from urllib.parse import urlparse

from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.core import set_global_service_context
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import FlatReader
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceWindowNodeParser

from llama_index.core import ChatPromptTemplate, PromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.indices.managed.zilliz import ZillizCloudPipelineIndex
from llama_index.core import QueryBundle
from llama_index.core.schema import BaseNode, ImageNode, MetadataMode

from custom.law_sentence_window import LawSentenceWindowNodeParser
from custom.llms.QwenLLM import QwenUnofficial
from custom.llms.GeminiLLM import Gemini
from custom.llms.proxy_model import ProxyModel
from pymilvus import MilvusClient

QA_PROMPT_TMPL_STR =  """
请根据以下法律知识库内容，以严谨专业的态度回答用户问题。按以下格式要求：
1. 直接明确的结论（是/否/构成XX罪等）
2. 逐条列出法律依据（按法律效力层级排序）
3. 司法解释需注明发布机关
---------------------
相关法律依据：
{context_str}
---------------------
问题：{query_str}
专业回答：
"""


QA_SYSTEM_PROMPT = """
你是一个专业严谨的法律智能助手，你的所有回答必须严格遵循以下原则：
1. 仅基于用户提供的法律知识库内容进行回答，禁止任何主观推测或自由发挥
2. 回答必须包含明确的法律依据，使用标准引用格式：《法律名称》第XX条
3. 当知识库中存在多个相关法条时，需全部列出并按法律效力层级排序
4. 若知识库中没有相关内容，必须明确回答'根据现有资料无法提供法律依据'
5. 所有司法解释引用需注明发文机关和文号
6. 回答需使用法言法语，保持专业性和准确性
"""


REFINE_PROMPT_TMPL_STR = """
你是一个法律回答优化专家，请按以下规则修正答案：
1. 检查每个法律引用是否与知识库内容完全一致
2. 确保法条序号、法律名称准确无误
3. 补充司法解释的发布年份和文号（例：法释〔2020〕XX号）
4. 删除任何假设性表述（如'可能'、'一般'等模糊用语）
5. 当新增内容来自知识库时，使用【新增依据】标注
6. 保持法条引用与问题的高度相关性
原始问题：{query_str}
现有答案：{existing_answer}
新增法律依据：{context_msg}
优化后的专业回答：
"""

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_github_folder_url(url):
    return url.startswith('https://github.com/') and '.' not in os.path.basename(url)


def get_branch_head_sha(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}"
    response = requests.get(url)
    data = response.json()
    sha = data['object']['sha']
    return sha


def get_github_repo_contents(repo_url):
    """支持多文件类型、递归获取子文件夹内容且增强错误处理的版本"""
    try:
        # 统一处理URL格式
        if "github.com" in repo_url and "/tree/" in repo_url:
            repo_url = repo_url.replace("github.com", "raw.githubusercontent.com").replace("/tree/", "/")

        path_parts = repo_url.replace("https://raw.githubusercontent.com/", "").split('/')
        if len(path_parts) < 4:
            raise ValueError("无效的GitHub路径格式")
        owner, repo, branch = path_parts[0], path_parts[1], path_parts[2]
        folder_path = '/'.join(path_parts[3:])

        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}?ref={branch}"
        response = requests.get(api_url)
        response.raise_for_status()  # 主动触发HTTP错误

        download_urls = []
        for item in response.json():
            if item['type'] == 'file' and item['name'].lower().endswith(('.txt', '.md', '.pdf')):
                download_urls.append(item['download_url'])
            elif item['type'] == 'dir':  # 如果是文件夹，递归获取内容
                subfolder_url = f"https://github.com/{owner}/{repo}/tree/{branch}/{item['path']}"
                download_urls.extend(get_github_repo_contents(subfolder_url))
        return download_urls
    except Exception as e:
        raise RuntimeError(f"获取GitHub内容失败: {str(e)}")

class Executor:
    def __init__(self, model):
        pass

    def build_index(self, path, overwrite):
        pass

    def build_query_engine(self):
        pass

    def delete_file(self, path):
        pass

    def query(self, question):
        pass


class MilvusExecutor(Executor):
    def __init__(self, config):
        self.index = None
        self.query_engine = None
        self.config = config
        self.node_parser = LawSentenceWindowNodeParser.from_defaults(
            sentence_splitter=lambda text: re.findall("[^,.;。？！]+[,.;。？！]?", text),
            window_size=config.milvus.window_size,
            window_metadata_key="window",
            original_text_metadata_key="original_text",)

        embed_model = HuggingFaceEmbedding(model_name=config.embedding.name)

        # 使用Qwen 通义千问模型
        if config.llm.name.find("qwen") != -1:
            llm = QwenUnofficial(temperature=config.llm.temperature, model=config.llm.name, max_tokens=2048)
        elif config.llm.name.find("gemini") != -1:
            llm = Gemini(temperature=config.llm.temperature, model_name=config.llm.name, max_tokens=2048)
        elif 'proxy_model' in config.llm:
            llm = ProxyModel(model_name=config.llm.name, api_base=config.llm.api_base, api_key=config.llm.api_key,
                             temperature=config.llm.temperature,  max_tokens=2048)
            print(f"使用{config.llm.name},PROXY_SERVER_URL为{config.llm.api_base},PROXY_API_KEY为{config.llm.api_key}")
        else:
            api_base = None
            if 'api_base' in config.llm:
                api_base = config.llm.api_base
            llm = OpenAI(api_base = api_base, temperature=config.llm.temperature, model=config.llm.name, max_tokens=2048)

        Settings.llm = llm
        Settings.embed_model = embed_model
        rerank_k = config.milvus.rerank_topk
        self.rerank_postprocessor = SentenceTransformerRerank(
            model=config.rerank.name, top_n=rerank_k)
        self._milvus_client = None
        self._debug = False

    def set_debug(self, mode):
        self._debug = mode

    def build_index(self, path, overwrite):
        config = self.config
        uri = f"http://{config.milvus.host}:{config.milvus.port}",
        vector_store = MilvusVectorStore(
            uri = f"http://{config.milvus.host}:{config.milvus.port}",
            collection_name = config.milvus.collection_name,
            overwrite=overwrite,
            dim=config.embedding.dim)
        self._milvus_client = vector_store._milvusclient

        if path.endswith('.txt'):
            if os.path.exists(path) is False:
                print(f'(rag) 没有找到文件{path}')
                return
            else:
                documents = FlatReader().load_data(Path(path))
                documents[0].metadata['file_name'] = documents[0].metadata['filename']
        elif os.path.isfile(path):
            print('(rag) 目前仅支持txt文件')
        elif os.path.isdir(path):
            if os.path.exists(path) is False:
                print(f'(rag) 没有找到目录{path}')
                return
            else:
                documents = SimpleDirectoryReader(path).load_data()
        else:
            return

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        nodes = self.node_parser.get_nodes_from_documents(documents)
        self.index = VectorStoreIndex(nodes, storage_context=storage_context, show_progress=True)

    def _get_index(self):
        config = self.config
        vector_store = MilvusVectorStore(
            uri = f"http://{config.milvus.host}:{config.milvus.port}",
            collection_name = config.milvus.collection_name,
            dim=config.embedding.dim,
        )
        self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        self._milvus_client = vector_store._milvusclient

    def build_query_engine(self):
        config = self.config
        if self.index is None:
            self._get_index()
        self.query_engine = self.index.as_query_engine(node_postprocessors=[
            self.rerank_postprocessor,
            MetadataReplacementPostProcessor(target_metadata_key="window")
        ])
        self.query_engine._retriever.similarity_top_k=config.milvus.retrieve_topk

        message_templates = [
            ChatMessage(content=QA_SYSTEM_PROMPT, role=MessageRole.SYSTEM),
            ChatMessage(
                content=QA_PROMPT_TMPL_STR,
                role=MessageRole.USER,
            ),
        ]
        chat_template = ChatPromptTemplate(message_templates=message_templates)
        self.query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": chat_template}
        )
        self.query_engine._response_synthesizer._refine_template.conditionals[0][1].message_templates[0].content = REFINE_PROMPT_TMPL_STR

    def delete_file(self, path):
        config = self.config
        if self._milvus_client is None:
            self._get_index()
        num_entities_prev = self._milvus_client.query(collection_name='law_rag',filter="",output_fields=["count(*)"])[0]["count(*)"]
        res = self._milvus_client.delete(collection_name=config.milvus.collection_name, filter=f"file_name=='{path}'")
        num_entities = self._milvus_client.query(collection_name='law_rag',filter="",output_fields=["count(*)"])[0]["count(*)"]
        print(f'(rag) 现有{num_entities}条，删除{num_entities_prev - num_entities}条数据')

    def query(self, question):
        if self.index is None:
            self._get_index()
        if question.endswith('?') or question.endswith('？'):
            question = question[:-1]
        if self._debug is True:
            contexts = self.query_engine.retrieve(QueryBundle(question))
            for i, context in enumerate(contexts):
                print(f'{question}', i)
                content = context.node.get_content(metadata_mode=MetadataMode.LLM)
                print(content)
            print('-------------------------------------------------------参考资料---------------------------------------------------------')
        response = self.query_engine.query(question)
        return response

class PipelineExecutor(Executor):
    def __init__(self, config):
        self.ZILLIZ_CLUSTER_ID = os.getenv("ZILLIZ_CLUSTER_ID")
        self.ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")
        self.ZILLIZ_PROJECT_ID = os.getenv("ZILLIZ_PROJECT_ID")
        self.ZILLIZ_CLUSTER_ENDPOINT = f"https://{self.ZILLIZ_CLUSTER_ID}.api.gcp-us-west1.zillizcloud.com"

        self.config = config
        if len(self.ZILLIZ_CLUSTER_ID) == 0:
            print('ZILLIZ_CLUSTER_ID 参数为空')
            exit()

        if len(self.ZILLIZ_TOKEN) == 0:
            print('ZILLIZ_TOKEN 参数为空')
            exit()

        self.config = config
        self._debug = False

        if config.llm.name.find("qwen") != -1:
            llm = QwenUnofficial(temperature=config.llm.temperature, model=config.llm.name, max_tokens=2048)
        elif config.llm.name.find("gemini") != -1:
            llm = Gemini(model_name=config.llm.name, temperature=config.llm.temperature, max_tokens=2048)
        else:
            api_base = None
            if 'api_base' in config.llm:
                api_base = config.llm.api_base
            llm = OpenAI(api_base = api_base, temperature=config.llm.temperature, model=config.llm.name, max_tokens=2048)

        Settings.llm = llm
        self._initialize_pipeline()


    def set_debug(self, mode):
        self._debug = mode

    def _initialize_pipeline(self):
        config = self.config
        try:
            pipeline_ids = self._list_pipeline_ids()
            self.pipeline_ids = pipeline_ids
            if len(pipeline_ids) == 0:
                ZillizCloudPipelineIndex.create_pipelines(
                    project_id = self.ZILLIZ_PROJECT_ID,
                    cluster_id=self.ZILLIZ_CLUSTER_ID,
                    api_key=self.ZILLIZ_TOKEN,
                    collection_name=config.pipeline.collection_name,
                    data_type = "doc",
                    language='CHINESE',
                    reranker= 'zilliz/bge-reranker-base',
                    embedding='zilliz/bge-base-zh-v1.5',
                    chunkSize=self.config.pipeline.chunk_size,
                    metadata_schema={"digest_from":"VarChar"}
                )
                pipeline_ids = self._list_pipeline_ids()
            self.index = ZillizCloudPipelineIndex(pipeline_ids=pipeline_ids, api_key=self.ZILLIZ_TOKEN)
        except Exception as e:
            print('(rag) zilliz pipeline 连接异常', str(e))
            exit()
        try:
            self._milvus_client = MilvusClient(
                uri=self.ZILLIZ_CLUSTER_ENDPOINT,
                token=self.ZILLIZ_TOKEN
            )
        except Exception as e:
            print('(rag) zilliz cloud 连接异常', str(e))

    def build_index(self, path, overwrite):
        config = self.config
        if not is_valid_url(path) or 'github' not in path:
            print('(rag) 不是一个合法的url，请尝试`https://raw.githubusercontent.com/akatrainning/Q-A_Chatter/refs/heads/main/hetongfa.txt`')
            return
        if overwrite == True:
            self._milvus_client.drop_collection(config.pipeline.collection_name)
            pipeline_ids = self._list_pipeline_ids()
            self._delete_pipeline_ids(pipeline_ids)

            self._initialize_pipeline(self.service_context)

        if is_github_folder_url(path):
            urls = get_github_repo_contents(path)
            for url in urls:
                print(f'(rag) 正在构建索引 {url}')
                self.build_index(url, False)  # already deleted original collection
        elif path.endswith('.txt'):
            self.index._insert_doc_url(
                url=path,
                metadata={"digest_from": LawSentenceWindowNodeParser.law_name(os.path.basename(path))},
            )
        else:
            print('(rag) 只有github上以txt结尾或文件夹可以被支持。')

    def build_query_engine(self):
        config = self.config
        self.query_engine = self.index.as_query_engine(
            search_top_k=config.pipeline.retrieve_topk)
        message_templates = [
            ChatMessage(content=QA_SYSTEM_PROMPT, role=MessageRole.SYSTEM),
            ChatMessage(
                content=QA_PROMPT_TMPL_STR,
                role=MessageRole.USER,
            ),
        ]
        chat_template = ChatPromptTemplate(message_templates=message_templates)
        self.query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": chat_template}
        )
        self.query_engine._response_synthesizer._refine_template.conditionals[0][1].message_templates[0].content = REFINE_PROMPT_TMPL_STR

    # ========== 新增方法：列出已导入文件 ==========
    def list_files(self):
        """获取Zilliz Pipeline中所有法律条文文件"""
        if self._milvus_client is None:
            self._get_index()  # 确保连接到Zilliz Cloud

        try:
            # 查询所有文档名称（自动去重）
            res = self._milvus_client.query(
                collection_name=self.config.pipeline.collection_name,
                filter="",
                output_fields=["doc_name"],
                group_by_field="doc_name"  # 按文件名分组
            )

            # 提取并返回文件名列表
            return [item["doc_name"] for item in res if "doc_name" in item]

        except Exception as e:
            print(f"(rag) 法律条文列表获取失败: {str(e)}")
            return []
        except KeyError as e:
            print("(rag) 元数据字段缺失，请检查doc_name是否存在")
        except ConnectionError as e:
            print("(rag) 连接Zilliz Cloud失败，请检查网络和API密钥")
    def delete_file(self, path):
        config = self.config
        if self._milvus_client is None:
            self._get_index()
        num_entities_prev = self._milvus_client.query(collection_name='law_rag',filter="",output_fields=["count(*)"])[0]["count(*)"]
        res = self._milvus_client.delete(collection_name=config.milvus.collection_name, filter=f"doc_name=='{path}'")
        num_entities = self._milvus_client.query(collection_name='law_rag',filter="",output_fields=["count(*)"])[0]["count(*)"]
        print(f'(rag) 现有{num_entities}条，删除{num_entities_prev - num_entities}条数据')

    def query(self, question):
        if self.index is None:
            self.get_index()
        if question.endswith("?") or question.endswith("？"):
            question = question[:-1]
        if self._debug is True:
            contexts = self.query_engine.retrieve(QueryBundle(question))
            for i, context in enumerate(contexts):
                print(f'{question}', i)
                content = context.node.get_content(metadata_mode=MetadataMode.LLM)
                print(content)
            print('-------------------------------------------------------参考资料---------------------------------------------------------')
        response = self.query_engine.query(question)
        return response

    def _list_pipeline_ids(self):
        url = f"https://controller.api.gcp-us-west1.zillizcloud.com/v1/pipelines?projectId={self.ZILLIZ_PROJECT_ID}"
        headers = {
            "Authorization": f"Bearer {self.ZILLIZ_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        collection_name = self.config.pipeline.collection_name
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(response.text)
        response_dict = response.json()
        if response_dict["code"] != 200:
            raise RuntimeError(response_dict)
        pipeline_ids = {}
        for pipeline in response_dict['data']:
            if collection_name in  pipeline['name']:
                pipeline_ids[pipeline['type']] = pipeline['pipelineId']

        return pipeline_ids

    def _delete_pipeline_ids(self, pipeline_ids):
        for pipeline_id in pipeline_ids:
            url = f"https://controller.api.gcp-us-west1.zillizcloud.com/v1/pipelines/{pipeline_id}/"
            headers = {
                "Authorization": f"Bearer {self.ZILLIZ_TOKEN}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }

            response = requests.delete(url, headers=headers)
            if response.status_code != 200:
                raise RuntimeError(response.text)


