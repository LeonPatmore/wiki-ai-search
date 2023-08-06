import logging
import os

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
slack_web_server = WebServer("slack-server", BASE_PORT + 4, SlackHandler)

RestHandler.wiki_search = wiki_search
rest_api_server = WebServer("rest-api", BASE_PORT + 2, RestHandler)

web_interface = WebInterface(wiki_search, BASE_PORT)

slack_web_server.start()
rest_api_server.start()

try:
    web_interface.run()
except KeyboardInterrupt:
    pass
finally:
    slack_web_server.join(timeout=5)
    rest_api_server.join(timeout=5)
