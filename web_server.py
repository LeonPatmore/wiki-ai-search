import logging
from http.server import HTTPServer


class WebServer:

    def __init__(self, port: int, handler_class):
        self.web_server = HTTPServer(("0.0.0.0", port), handler_class)

    def __call__(self):
        logging.info("Starting web sever")
        try:
            self.web_server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.web_server.server_close()
        logging.info("Web server closed")
