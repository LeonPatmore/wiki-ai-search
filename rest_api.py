import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from search import WikiSearch


class RestHandler(BaseHTTPRequestHandler):

    wiki_search = None

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        msg = self.wiki_search.search(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(str.encode(msg))


class RestAPI:

    def __init__(self, port: int, wiki_search: WikiSearch):
        RestHandler.wiki_search = wiki_search
        self.web_server = HTTPServer(("0.0.0.0", port), RestHandler)

    def __call__(self):
        logging.info("Starting rest api")
        try:
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.web_server.server_close()
        logging.info("Rest api server closed")
