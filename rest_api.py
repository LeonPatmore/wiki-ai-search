from http.server import BaseHTTPRequestHandler


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
