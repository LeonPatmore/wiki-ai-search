import gradio as gr
from langchain import OpenAI
from llama_index import ServiceContext, GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from llama_index.node_parser import SimpleNodeParser

parser = SimpleNodeParser()


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 500
    chunk_size_limit = 1024

    print("*" * 5, "Documents parsing initiated", "*" * 5)
    file_metadata = lambda x: {"filename": x}
    reader = SimpleDirectoryReader(directory_path, file_metadata=file_metadata)
    documents = reader.load_data()

    # nodes = parser.get_nodes_from_documents(documents)
    # index = GPTVectorStoreIndex(nodes)
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-4", max_tokens=num_outputs))

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # print("*"*5, "Index creation initiated", "*"*5)
    index = GPTVectorStoreIndex.from_documents(
        documents=documents, service_context=service_context
    )
    # print("*"*5, "Index created", "*"*5)
    index.storage_context.persist("./entire_docs")
    return index



construct_index("./docs")
storage_context = StorageContext.from_defaults(persist_dir="./entire_docs")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()


def ask_bot(input: str) -> str:
    return query_engine.query(input)


iface = gr.Interface(fn=ask_bot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

index = construct_index("docs")
iface.launch(share=False, server_name="0.0.0.0")

if __name__ == '__main__':
    pass
