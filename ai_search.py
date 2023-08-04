from langchain.chat_models import ChatOpenAI
from llama_index import ServiceContext, GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from llama_index.indices.query.base import BaseQueryEngine

from search import WikiSearch


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 500
    chunk_size_limit = 1024

    print("*" * 5, "Documents parsing initiated", "*" * 5)
    reader = SimpleDirectoryReader(directory_path)
    documents = reader.load_data()

    # nodes = parser.get_nodes_from_documents(documents)
    # index = GPTVectorStoreIndex(nodes)
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=1, model_name="gpt-4", max_tokens=num_outputs))

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTVectorStoreIndex.from_documents(documents=documents, service_context=service_context)
    index.storage_context.persist("./entire_docs")


def load_query_engine():
    storage_context = StorageContext.from_defaults(persist_dir="./entire_docs")
    loaded_index = load_index_from_storage(storage_context)
    return loaded_index.as_query_engine()


class AiSearch(WikiSearch):

    def __init__(self, query_engine: BaseQueryEngine):
        self.query_engine = query_engine

    def search(self, text_input: str):
        return str(self.query_engine.query(text_input))
