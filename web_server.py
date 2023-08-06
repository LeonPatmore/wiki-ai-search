import logging
from http.server import HTTPServer
from threading import Thread


class WebServer(Thread):

    def __init__(self, server_name: str, port: int, handler_class):
        super().__init__(name=server_name)
        self.server_name = server_name
        self.web_server = HTTPServer(("0.0.0.0", port), handler_class)

    def run(self):
        logging.info(f"Starting web sever [ {self.server_name} ]")
        self.web_server.serve_forever()

    def join(self, *args, **kwargs):
        logging.info(f"Closing web server [ {self.server_name} ]")
        self.web_server.server_close()
        Thread.join(self, *args, **kwargs)
