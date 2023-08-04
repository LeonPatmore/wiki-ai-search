import logging

from ai_search import construct_index, load_query_engine, AiSearch
from rest_api import RestAPI
from web_interface import WebInterface

logging.root.setLevel(logging.INFO)

construct_index("./docs")
query_engine = load_query_engine()

wiki_search = AiSearch(query_engine)

rest_api = RestAPI(8080, wiki_search)()
# web_interface = WebInterface(wiki_search)()

if __name__ == '__main__':
    pass
