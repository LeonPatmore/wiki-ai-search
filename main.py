import logging
import os
import sys
from threading import Thread

from slack_sdk import WebClient

from ai_search import construct_index, load_query_engine, AiSearch
from rest_api import RestHandler
from slack_event_listener import SlackHandler
from web_interface import WebInterface
from web_server import WebServer

logging.root.setLevel(logging.INFO)

BASE_PORT = int(os.environ.get("BASE_PORT", 8080))

construct_index("./docs")
query_engine = load_query_engine()

wiki_search = AiSearch(query_engine)

SlackHandler.wiki_search = wiki_search
SlackHandler.channel = os.environ.get("SLACK_CHANNEL")
SlackHandler.slack_client = WebClient(token=os.environ.get("SLACK_TOKEN"))
slack_web_server = WebServer(BASE_PORT + 4, SlackHandler)
slack_thread = Thread(target=slack_web_server)

RestHandler.wiki_search = wiki_search
rest_api_server = WebServer(BASE_PORT + 2, RestHandler)
rest_api_thread = Thread(target=rest_api_server)

web_interface = WebInterface(wiki_search, BASE_PORT)
web_interface_thread = Thread(target=web_interface)

try:
    slack_thread.start()
    rest_api_thread.start()
    # web_interface_thread.start()
except (KeyboardInterrupt, SystemExit):
    logging.info("Killing threads")
    slack_thread.join(timeout=5000)
    rest_api_thread.join(timeout=5000)
    sys.exit()

if __name__ == '__main__':
    pass
