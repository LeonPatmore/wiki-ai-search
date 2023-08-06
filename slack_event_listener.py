import json
import logging
from http.server import BaseHTTPRequestHandler


class SlackHandler(BaseHTTPRequestHandler):

    wiki_search = None
    channel = None
    slack_client = None

    def respond_to_challenge(self, slack_data: dict):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(str.encode(slack_data["challenge"]))

    @staticmethod
    def is_not_root_message(slack_data: dict) -> bool:
        return "parent_user_id" in slack_data["event"]

    @staticmethod
    def is_bot_message(slack_data: dict):
        return "subtype" in slack_data["event"] and "bot_message" == slack_data["event"]["subtype"]

    def respond_to_event(self, slack_data: dict):
        if "text" not in slack_data["event"] or "channel" not in slack_data["event"] \
                or slack_data["event"]["channel"] != self.channel or self.is_not_root_message(slack_data) \
                or self.is_bot_message(slack_data):
            logging.info("Ignoring this message")
            self.send_response(200)
            self.end_headers()
            return
        msg = self.wiki_search.search(slack_data["event"]["text"])
        self.slack_client.chat_postMessage(channel=self.channel, text=msg, thread_ts=slack_data["event"]["ts"])

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        logging.info(f"Received [ {post_data} ] from Slack")
        slack_data = json.loads(post_data)

        if "challenge" in slack_data:
            self.respond_to_challenge(slack_data)
        else:
            self.respond_to_event(slack_data)
